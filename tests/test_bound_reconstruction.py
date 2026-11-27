"""Recompute the published bounds from raw observations without the model helpers."""
from decimal import Decimal as D
import json
from pathlib import Path
import unittest

from scripts.kill_test import calculate, load_revised_evidence, sensitivity

EVIDENCE = Path(__file__).resolve().parents[1] / "evidence"


def read(name):
    return json.loads((EVIDENCE / f"{name}.json").read_text(), parse_float=D)


def units(capture, label):
    rows = capture["reads"]
    return D(int(rows[label]["result"], 16)) / 10**int(rows["decimals"]["result"], 16)


def no_code(capture):
    return sum(units(capture, "balance/" + key.split("/")[1])
               for key, row in capture["reads"].items()
               if key.startswith("code/") and row.get("code_type") == "no runtime code")


class ReconstructionTest(unittest.TestCase):
    def test_floor_ceiling_and_changes_in_coverage(self):
        holders = read("holders-2026-09-30")["targets"]
        supplements = read("round1-supplement")
        plume = supplements["holder_probes"]["ustb/plume"]["reads"]
        evm = read("evm-2026-09-30")["chains"]
        facts = read("primary-transcriptions-2026-09-30")
        dated = read("superstate-ustb-2026-09-30")["historical_data"]
        filing = read("franklin-filing-readback-2026-09-30")
        nav, aum = (next(D(r["value"]) for r in dated[key] if r["date"] == "2026-09-30")
                    for key in ("nav", "aum"))
        benji = D(filing["item_b4_net_assets_usd"])
        benji_excluded = no_code(holders["benji/ethereum"]) * benji / D(filing["item_b5_shares"])

        # Avalanche's Anchorage leg is already in its no-code total.
        attested = sum(D(r["buidl_usd"]) - 1 for r in facts["anchorage_reserve_legs"]
                       if r["chain"] in ("solana", "aptos"))
        bnb_custody = D(int(evm["bsc"]["reads"]["anchorage_buidl"]["result"], 16)) / 10**6
        avalanche_custody = D(int(evm["avalanche"]["reads"]["anchorage_buidl"]["result"], 16)) / 10**6
        buidl_excluded = bnb_custody + no_code(holders["buidl/avalanche"])
        buidl_floor = buidl_excluded + attested
        buidl_cap = D(facts["securitize_platform_value_display_usd"]) + 100_000_000

        usyc_oracle = evm["ethereum"]["reads"]["usyc_nav"]["result"]
        usyc_nav = D(int(usyc_oracle[66:130], 16)) / 10**8
        usyc_backing = units(holders["usyc/ethereum"], "balance/0xdd82875f0840aad58a455a70b88eed9f59cec7c7") * usyc_nav
        usyc_excluded = (units(holders["usyc/bsc"], "balance/0x87433fec6f8d9df13d1e17c4b11364ecd2e93a51")
                         + D(100)) * usyc_nav
        usyc_floor = usyc_backing + usyc_excluded
        usyc_cap = D(facts["circle_usyc_display_usd"]) + 100_000_000

        ustb_eth = holders["ustb/ethereum"]
        ustb_floor = units(ustb_eth, "supply") * nav
        ustb_excluded = (no_code(ustb_eth) + units(ustb_eth, "balance/0x4e58a2e433a739726134c83d2f07b2562e8dfdb3")) * nav
        m_tbill = units(ustb_eth, "balance/0x569d7dccbf6923350521ecbc28a555a500c4f0ec") * nav
        n_tbill, n_basis = (D(int(plume["balance/" + address]["result"], 16)) / 10**6 * nav
                            for address in ("0xe72fe64840f4ef80e3ec73a1c749491b5c938cb9",
                                            "0x11113ff3a60c2450f4b22515cb760417259ee94b"))

        prices = read("ondo-ousg-2026-09-30") + read("ondo-ousg-adjacent-2026-10")
        low = min(r["asset"]["priceUsd"] for r in prices)
        high = max(r["asset"]["priceUsd"] for r in prices)
        xrpl = read("ousg-xrpl-2026-09-30")
        (xrpl_native,) = xrpl["gateway_balances"]["result"]["obligations"].values()
        ousg_eth = holders["ousg/ethereum"]
        ousg_native = units(ousg_eth, "supply") + D(xrpl_native)
        ousg_floor = ousg_native * low
        published_max = max(r["asset"]["tvlUsd"]["total"] for r in prices)
        self.assertGreater(published_max, ousg_native * high)
        ousg_cap = published_max + 10_000_000 + 25_000_000
        ousg_excluded = (no_code(ousg_eth) + units(ousg_eth, "balance/0x1dd7950c266fb1be96180a8fdb0591f70200e018")) * low
        vault_return = read("review-ethereum-2026-09-30")["reads"]["stbl/fetchVaultData()"]["result"][2:]
        # The independent binding candidate on this snapshot is deposited stable
        # value less cumulative haircuts (fifth and sixth return words).
        net_value = D(int(vault_return[320:384], 16) - int(vault_return[256:320], 16)) / 10**18
        stbl = net_value * low / high

        floor = buidl_floor + ustb_floor + usyc_floor + ousg_floor + benji
        cap = buidl_cap + aum + usyc_cap + ousg_cap + benji
        direct_usd = m_tbill + n_tbill + n_basis + usyc_backing + stbl
        excluded = buidl_excluded + ustb_excluded + usyc_excluded + ousg_excluded + benji_excluded
        broad_usd = direct_usd + attested + bnb_custody + avalanche_custody

        funds, positions, observations = load_revised_evidence(EVIDENCE)
        direct = calculate(funds, positions, False)
        broad = calculate(funds, positions, True)
        for actual, independent in (
            (direct["denominator_floor_usd"], floor),
            (direct["denominator_ceiling_usd"], cap),
            (direct["denominator_slack_usd"], cap - floor),
            (direct["unclassified_at_floor_usd"], floor - excluded - direct_usd),
            (direct["verified_usd"], direct_usd),
            (direct["excluded_usd"], excluded),
            (direct["shortfall_usd_to_cutoff"], cap / 20 - direct_usd),
            (broad["verified_usd"], broad_usd),
            (broad["shortfall_usd_to_cutoff"], D(0)),
        ):
            self.assertEqual(actual.quantize(D("0.01")), independent.quantize(D("0.01")))
        self.assertEqual(direct["share_upper"].quantize(D("0.000001")),
                         (1 - excluded / cap).quantize(D("0.000001")))
        scenarios = sensitivity(funds, positions, observations)
        dust_excluded = scenarios["without_dust_only_routes"]
        self.assertEqual(dust_excluded["direct_backing_usd"].quantize(D("0.01")),
                         (n_basis + usyc_backing + stbl).quantize(D("0.01")))

        # Reproduce the floor coverage reviewed in round three before adding Nest.
        self.assertEqual((floor - excluded - (direct_usd - n_tbill - n_basis)).quantize(D("0.01")),
                         D("1350866876.34"))
        deployments = sum(units(capture, "supply") for name, capture in holders.items()
                          if name.split("/")[0] in ("buidl", "buidl_i"))
        solana = supplements["solana"]["buidl"]["supply"]["result"]["value"]
        solana_supply = D(solana["amount"]).scaleb(-solana["decimals"])
        aptos = supplements["aptos"]
        aptos_supply = D(aptos["supply"]["result"]["value"][0]["vec"][0]).scaleb(
            -aptos["metadata"]["result"]["value"]["decimals"])
        self.assertGreater(solana_supply, D("231923254"))
        self.assertLess(aptos_supply, D("145511027"))
        deployment_cap = cap - buidl_cap + deployments + solana_supply + D("145511027")
        scenario = scenarios["buidl_deployment_ceiling"]
        self.assertEqual(scenario["denominator_ceiling_usd"], deployment_cap)
        self.assertEqual(scenario["direct_shortfall_usd_to_cutoff"].quantize(D("0.01")),
                         (deployment_cap / 20 - direct_usd).quantize(D("0.01")))

    def test_october_and_november_readbacks_are_comparable_only_as_a_discrepancy(self):
        sept = read("franklin-filing-readback-2026-09-30")
        octo = read("franklin-filing-readback-2026-10-31")
        for field in ("series", "class", "ticker", "item_8_share_classes"):
            self.assertEqual(sept[field], octo[field])
        self.assertEqual(octo["report_period"], "2026-10-31")
        census = read("round2-readbacks")["stellar_benji"]
        identification = read("stellar-benji-identification-2026-11-27")
        toml = identification["issuer_toml"]
        self.assertEqual(census["asset"], toml["asset_code"] + ":" + toml["asset_issuer"])
        units_seen = D(census["total_of_observed_trust_lines"])
        top = census["largest_observed"][:3]
        self.assertEqual([r["account"] for r in top], [r["account"] for r in identification["accounts"]])
        self.assertEqual({r["sponsor"] for r in identification["accounts"]}, {identification["sponsor"]["account"]})
        top_units = sum(D(r["balance"]) for r in top)
        for ratio, expected in (
            (top_units * 100 / units_seen, "58.69"),
            (units_seen / D(sept["item_b5_shares"]), "1.98"),
            (units_seen / D(octo["item_b5_shares"]), "1.59"),
            (units_seen - D(octo["item_b5_shares"]), "491613406.91"),
        ):
            self.assertEqual(ratio.quantize(D("0.01")), D(expected))
        summary = identification["asset_summary"]
        self.assertEqual(sum(summary["accounts"].values()), census["accounts_read"])
        self.assertEqual(sum(map(D, summary["balances"].values())) - units_seen, D(6600))
