from decimal import Decimal as D
from pathlib import Path
import json
import shutil
from tempfile import TemporaryDirectory
import unittest

from scripts.holder_audit import load_holders
from scripts.kill_test import (
    Fund, Position, calculate, eligible_no_code, gated_receipt, load_revised_evidence, ousg_model, sensitivity,
)

EVIDENCE = Path(__file__).resolve().parents[1] / "evidence"


class KillTest(unittest.TestCase):
    def setUp(self):
        self.funds = [Fund("A", D(100), D(200)), Fund("B", D(500), D(800))]

    def test_weights_by_usd_and_continues_at_exact_cutoff(self):
        positions = [Position("A", "x", "0xabcd", "wrapper_contract", D(50), D(5))]
        result = calculate(self.funds, positions, False)
        self.assertEqual(result["share_lower"], D("0.05"))
        self.assertEqual(result["funds"][0]["share_lower"], D("0.25"))
        self.assertEqual(result["verdict"], "continue")

    def test_reserve_custody_moves_between_verified_and_excluded(self):
        positions = [Position("A", "x", "0xabcd", "reserve_custody", D(50), D(50), True)]
        broad = calculate(self.funds, positions, True)
        strict = calculate(self.funds, positions, False)
        self.assertEqual(broad["verified_usd"], D(50))
        self.assertEqual(strict["verified_usd"], D(0))
        self.assertEqual(strict["excluded_usd"], D(50))
        self.assertEqual(strict["share_upper"], D("0.95"))
        self.assertEqual(strict["verdict"], "inconclusive")

    def test_unknown_is_not_zero_and_upper_must_be_strictly_below_threshold(self):
        funds = [Fund("A", D(100), D(100))]
        self.assertEqual(calculate(funds, [], False)["share_upper"], D(1))
        for excluded, verdict in [(95, "inconclusive"), (96, "below_cutoff")]:
            with self.subTest(excluded=excluded):
                rows = [Position("A", "x", "0xabcd", "verified_non_wrapper", D(excluded), D(excluded))]
                self.assertEqual(calculate(funds, rows, False)["verdict"], verdict)

    def test_duplicate_position_is_rejected_but_same_address_on_other_chain_is_distinct(self):
        first = Position("A", "x", "0xAbCd", "reserve_custody", D(5), D(5))
        same = Position("A", "x", "0xabcd", "wrapper_contract", D(5), D(5))
        other = Position("A", "y", "0xabcd", "reserve_custody", D(5), D(5))
        with self.assertRaisesRegex(ValueError, "duplicate underlying"):
            calculate(self.funds, [first, same], True)
        self.assertEqual(calculate(self.funds, [first, other], True)["verified_usd"], D(10))

    def test_five_fund_snapshot_and_both_verdicts(self):
        funds, positions, observed = load_revised_evidence(EVIDENCE)
        self.assertEqual([fund.ticker for fund in funds], ["BUIDL", "USTB", "USYC", "OUSG", "BENJI"])
        strict = calculate(funds, positions, False)
        broad = calculate(funds, positions, True)
        self.assertEqual(broad["denominator_ceiling_usd"], D("9179057896.15"))
        self.assertEqual(broad["verified_usd"].quantize(D("0.01")), D("619366062.06"))
        self.assertEqual(strict["verified_usd"].quantize(D("0.01")), D("86669353.88"))
        self.assertTrue(D("0.6219") < strict["share_upper"] < D("0.6220"))
        self.assertEqual(strict["unclassified_at_ceiling_usd"],
                         strict["denominator_slack_usd"] + strict["unclassified_at_floor_usd"])
        self.assertEqual({row["minted_frxusd"] for row in observed["frax_pinned"].values()}, {D(0)})
        scenarios = sensitivity(funds, positions, observed)
        self.assertGreater(scenarios["frax_documentary_reserve_attribution"]["direct"]["share_lower"],
                           strict["share_lower"])
        self.assertLess(scenarios["without_solana_aptos_attestation"]["custody_inclusive_lower"], D("0.05"))
        self.assertEqual(observed["flux_pinned"]["fousg"], {"mint_paused": False, "borrow_paused": True})
        self.assertEqual(observed["flux_pinned"]["fusdc"], {"mint_paused": False, "borrow_paused": False})
        self.assertLess(strict["share_lower"], D("0.05"))
        self.assertGreaterEqual(broad["share_lower"], D("0.05"))
        self.assertEqual(strict["verdict"], "inconclusive")
        self.assertEqual(broad["verdict"], "continue")
        self.assertEqual(set(observed["anchorage_evm"]), {"bsc", "avalanche"})
        for row in observed["anchorage_evm"].values():
            self.assertFalse(row["code_present"])
        custody = {row.chain: row.strict_custody_exclusion for row in positions if row.kind == "reserve_custody"}
        self.assertEqual(custody, {"solana": False, "aptos": False, "bsc": True, "avalanche": True})
        self.assertEqual(observed["usual_usd0_verified"]["usyc_native"], D("12320132.708463"))
        self.assertEqual(observed["usyc_bsc_top_holder"]["verified_rank"], 1)
        self.assertGreater(observed["curve_frxusd_balance"], D(5_000_000))
        self.assertTrue(D("0.99") < observed["curve_quote_1_crvusd_to_frxusd"] < D("1.01"))
        self.assertGreater(observed["curve_usdtb_balance"], D(10_000_000))
        self.assertTrue(D("0.99") < observed["curve_quote_1_usdc_to_usdtb"] < D("1.01"))

    def test_separate_attested_and_dust_only_sensitivities(self):
        funds, positions, observed = load_revised_evidence(EVIDENCE)
        custody = calculate(funds, positions, True)
        self.assertEqual(custody["attested_only_backing_usd"], D(377434279))
        self.assertEqual(custody["onchain_backing_usd"].quantize(D("0.01")), D("241931783.06"))
        scenarios = sensitivity(funds, positions, observed)
        dust = scenarios["without_dust_only_routes"]
        self.assertEqual(dust["direct_backing_usd"].quantize(D("0.01")), D("15032143.93"))
        self.assertGreater(dust["custody_inclusive_lower"], D("0.05"))
        self.assertEqual(dust["direct"]["share_upper"], calculate(funds, positions, False)["share_upper"])
        model = observed["buidl_deployment_scenario"]
        self.assertEqual(model["non_evm_allowance_native"]["aptos"], D("145511027"))
        self.assertEqual(model["non_evm_allowance_native"]["solana"], D("380840998.07"))
        self.assertEqual(model["pinned_evm_sum_native"], D("1136079649.177649"))
        scenario = scenarios["buidl_deployment_ceiling"]
        self.assertEqual(scenario["denominator_ceiling_usd"], D("5941489570.397649"))
        self.assertLess(scenario["direct"]["share_lower"], D("0.05"))
        self.assertGreater(scenario["direct"]["share_upper"], D("0.05"))

    def test_guards_reject_corrupt_copied_evidence(self):
        facts = "primary-transcriptions-2026-09-30"
        review = "review-ethereum-2026-09-30"
        cases = [
            ("franklin-filing-readback-2026-09-30", ("item_b4_net_assets_usd",), "1", "Franklin filing readback"),
            (facts, ("date",), "2026-10-01", "mixed snapshot dates"),
            (facts, ("anchorage_ethereum_usdtb_redeemable",), "496571144", "USDtb token supply"),
            (facts, ("anchorage_total_buidl_usd",), "532696710", "reserve legs do not reconcile"),
            ("evm-2026-09-30", ("chains", "bsc", "reads", "anchorage_buidl", "result"),
             hex(111_424_960 * 10**6), "attestation and RPC diverge"),
            (review, ("reads", "mtbill/totalSupply()", "result"), hex(50_000_000 * 10**18),
             "mTBILL Ethereum NAV and supply"),
            (facts, ("circle_usyc_display_usd",), "2200000000", "classified balances exceed denominator"),
        ]
        with TemporaryDirectory() as temporary:
            directory = Path(temporary) / "evidence"
            shutil.copytree(EVIDENCE, directory)
            for name, keys, value, error in cases:
                with self.subTest(guard=error):
                    path = directory / f"{name}.json"
                    original = path.read_text()
                    fixture = json.loads(original)
                    cursor = fixture
                    for key in keys[:-1]:
                        cursor = cursor[key]
                    cursor[keys[-1]] = value
                    path.write_text(json.dumps(fixture))
                    try:
                        with self.assertRaisesRegex(ValueError, error):
                            funds, positions, _ = load_revised_evidence(directory)
                            calculate(funds, positions, False)
                    finally:
                        path.write_text(original)

    def test_nonzero_frax_counter_caps_credited_inventory(self):
        with TemporaryDirectory() as temporary:
            directory = Path(temporary) / "evidence"
            shutil.copytree(EVIDENCE, directory)
            path = directory / "review-ethereum-2026-09-30.json"
            fixture = json.loads(path.read_text())
            fixture["reads"]["frax/buidl/frxUSDMinted()"]["result"] = hex(250_000 * 10**18)
            fixture["reads"]["frax/ustb/frxUSDMinted()"]["result"] = hex(40_000_000 * 10**18)
            path.write_text(json.dumps(fixture))
            funds, positions, observed = load_revised_evidence(directory)
        buidl, = [row for row in positions if row.fund == "BUIDL" and row.kind == "wrapper_contract"]
        self.assertEqual((buidl.native, buidl.usd), (D(250_000), D(250_000)))
        ustb, = [row for row in positions if row.fund == "USTB" and row.kind == "wrapper_contract" and not row.dust_only]
        self.assertEqual(ustb.native, D("1729693.761124"))
        self.assertEqual(ustb.usd, ustb.native * observed["ustb_nav_usd"])
        self.assertEqual(observed["frax_unattributed_reserves"], [])
        self.assertGreater(calculate(funds, positions, False)["verified_usd"], D(100_000_000))

    def test_no_code_exclusions_reject_delegation_and_failed_code_reads(self):
        for address_type in ("delegated EOA", "code unknown", "contract code"):
            self.assertFalse(eligible_no_code({"address_type": address_type}))
        self.assertTrue(eligible_no_code({"address_type": "no runtime code"}))

    def test_ousg_uses_low_price_and_newer_mark_for_conservative_bounds(self):
        marks = json.loads((EVIDENCE / "ondo-ousg-2026-09-30.json").read_text(), parse_float=D)
        adjacent = json.loads((EVIDENCE / "ondo-ousg-adjacent-2026-10.json").read_text(), parse_float=D)
        model = ousg_model(marks, adjacent, D("1132837.419415"), D("1605617.7253523406"))
        self.assertEqual(model["direct_exclusion_nav_usd"], D("116.719343"))
        self.assertEqual(model["pinned_floor_usd"], model["pinned_native_units"] * D("116.719343"))
        self.assertGreater(model["ceiling_basis_usd"], D("319694932.23"))
        self.assertEqual(model["ceiling_usd"], D("356225753.39"))
        with self.assertRaisesRegex(ValueError, "invalid OUSG"):
            ousg_model(marks, adjacent, D(0), D(1))

    def test_gated_receipt_requires_runtime_code(self):
        captures, reports = load_holders(EVIDENCE)
        deployment = "ousg/ethereum"
        address = "0x1dd7950c266fb1be96180a8fdb0591f70200e018"
        row, = [row for row in reports[deployment]["rows"] if row["address"] == address]
        for address_type in ("no runtime code", "delegated EOA", "code unknown"):
            row["address_type"] = address_type
            with self.assertRaisesRegex(ValueError, "gated receipt code"):
                gated_receipt(captures[deployment], reports[deployment], address,
                              "flux_underlying", "0x6f307dc3")


if __name__ == "__main__":
    unittest.main()
