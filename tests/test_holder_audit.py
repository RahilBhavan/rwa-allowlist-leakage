from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from scripts.holder_audit import add_holder_classes, audit, audit_xrpl, holder_type, load_holders, rank_balances, verify_bnb_discovery, verify_usual
from scripts.review_evidence import observations

EVIDENCE = Path(__file__).resolve().parents[1] / "evidence"


class HolderAuditTest(unittest.TestCase):
    def test_residual_certifies_only_strictly_larger_balances(self):
        self.assertEqual(
            rank_balances(100, {"a": 55, "b": 15, "c": 15}),
            (15, [("a", 1, 1), ("b", 2, None), ("c", 2, None)]),
        )
        self.assertEqual(rank_balances(100, {"a": 50, "b": 50}),
                         (0, [("a", 1, 1), ("b", 1, 1)]))
        self.assertIsNone(rank_balances(None, {"a": 55})[1][0][2])
        with self.assertRaisesRegex(ValueError, "reconcile"):
            rank_balances(100, {"a": 51, "b": 50})

    def test_delegated_eoa_is_neither_plain_no_code_nor_ordinary_contract(self):
        self.assertEqual(holder_type("0xef0100" + "a" * 40), "delegated EOA")
        self.assertEqual(holder_type("0x"), "no runtime code")
        self.assertEqual(holder_type(None), "code unknown")

    def test_balance_query_must_match_pin(self):
        captures, _ = load_holders(EVIDENCE)
        target = deepcopy(captures["usyc/bsc"])
        target["reads"]["supply"]["params"][-1] = "latest"
        with self.assertRaisesRegex(ValueError, "pinned request"):
            audit(target)

    def test_usual_requires_treasury_link_and_market_quote(self):
        captures, reports = load_holders(EVIDENCE)
        target = deepcopy(captures["usyc/ethereum"])
        target["reads"]["usual_dao_treasury"]["result"] = "0x" + "0" * 64
        with self.assertRaisesRegex(ValueError, "custody"):
            verify_usual(target, reports["usyc/ethereum"])
        target = deepcopy(captures["usyc/ethereum"])
        target["reads"]["usd0_pool_quote"]["result"] = "0x0"
        with self.assertRaisesRegex(ValueError, "route"):
            verify_usual(target, reports["usyc/ethereum"])

    def test_xrpl_scope_and_pagination(self):
        evidence = json.loads((EVIDENCE / "ousg-xrpl-2026-09-30.json").read_text())
        report = audit_xrpl(evidence)
        self.assertEqual(report["issuer_domain"], "ondo.finance")
        self.assertTrue(report["issuer_requires_authorization"])
        self.assertEqual(report["outstanding_native"], Decimal("1605617.7253523406"))
        self.assertEqual([row["verified_rank"] for row in report["rows"]], [1, 2, 3, 4, 5])
        evidence["pages"][-1]["result"]["marker"] = "unread-page"
        with self.assertRaisesRegex(ValueError, "pagination"):
            audit_xrpl(evidence)

    def test_successor_requires_parent_hash_match(self):
        captures, _ = load_holders(EVIDENCE)
        target = deepcopy(captures["ustb/ethereum"])
        target["successor"]["parentHash"] = "0x" + "0" * 64
        with self.assertRaisesRegex(ValueError, "block bracket"):
            audit(target)

    def test_usual_requires_usyc_eligibility_and_unpaused_usd0(self):
        captures, reports = load_holders(EVIDENCE)
        for label, value in (("usd0_paused", "0x1"), ("usual_usyc_eligible", "0x0")):
            with self.subTest(label=label):
                target = deepcopy(captures["usyc/ethereum"])
                target["reads"][label]["result"] = value
                with self.assertRaisesRegex(ValueError, "Usual custody"):
                    verify_usual(target, reports["usyc/ethereum"])

    def test_bnb_burn_must_match_supply_delta(self):
        _, reports = load_holders(EVIDENCE)
        evidence = json.loads((EVIDENCE / "usyc-bnb-receipt-2026-09-25.json").read_text())
        evidence["supply_change"][1]["result"] = evidence["supply_change"][0]["result"]
        with patch.object(Path, "read_text", return_value=json.dumps(evidence)):
            with self.assertRaisesRegex(ValueError, "receipt burn"):
                verify_bnb_discovery(EVIDENCE, reports["usyc/bsc"])

    def test_xrpl_obligations_must_reconcile(self):
        evidence = json.loads((EVIDENCE / "ousg-xrpl-2026-09-30.json").read_text())
        obligations = evidence["gateway_balances"]["result"]["obligations"]
        for currency in obligations:
            obligations[currency] = "0"
        with self.assertRaisesRegex(ValueError, "gateway obligations diverge"):
            audit_xrpl(evidence)

    def test_midas_and_stbl_require_a_historical_acquisition_route(self):
        captures, _ = load_holders(EVIDENCE)
        evidence = json.loads((EVIDENCE / "review-ethereum-2026-09-30.json").read_text())
        for label, error in (("midas_pool_eth/quote", "mTBILL acquisition"),
                             ("stbl/token_transfer_simulation", "STBL vault deposits")):
            with self.subTest(label=label):
                altered = deepcopy(evidence)
                altered["reads"][label]["result"] = "0x" + "0" * 128
                with patch.object(Path, "read_text", return_value=json.dumps(altered)):
                    with self.assertRaisesRegex(ValueError, error):
                        observations(EVIDENCE, captures["ustb/ethereum"])

    def test_holder_class_shares_reconcile_and_keep_unknown_visible(self):
        _, reports = load_holders(EVIDENCE)
        xrpl = json.loads((EVIDENCE / "ousg-xrpl-2026-09-30.json").read_text())
        reports["ousg/xrpl"] = audit_xrpl(xrpl)
        add_holder_classes(EVIDENCE, reports)
        for report in reports.values():
            shares = report["holder_class_share_of_supply"]
            if all(share is not None for share in shares.values()):
                self.assertAlmostEqual(sum(shares.values()), Decimal(1))
        self.assertEqual(reports["ousg/xrpl"]["holder_class_share_of_supply"]["unknown_control"], 1)
        for name in ("ustb/plume", "buidl/optimism"):
            self.assertEqual(reports[name]["residual_native"], 0)
            self.assertEqual([row["verified_rank"] for row in reports[name]["rows"]], [1, 2])
        self.assertEqual(reports["benji/base"]["holder_class_share_of_supply"]["unobserved"], 1)
        for name in ("buidl/avalanche", "buidl/bsc"):
            self.assertGreater(reports[name]["holder_class_share_of_supply"]["reserve_custody"], 0)
            self.assertEqual(reports[name]["holder_class_share_of_supply"]["issuer_ops"], 0)
        self.assertGreater(reports["buidl_i/ethereum"]["holder_class_share_of_supply"]["eoa"], 0)
