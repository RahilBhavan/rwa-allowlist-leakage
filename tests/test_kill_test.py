from decimal import Decimal as D
from pathlib import Path
import json
import unittest

from scripts.holder_audit import load_holders
from scripts.kill_test import Fund, Position, calculate, eligible_no_code, gated_receipt, load_revised_evidence, ousg_model, sensitivity

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
