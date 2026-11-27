from copy import deepcopy
from hashlib import sha256
import unittest
from unittest.mock import patch

from scripts import replay_evidence, verify_pdf_facts


class PdfFactsTest(unittest.TestCase):
    def setUp(self):
        chains = ["Solana", "BSC", "Avalanche", "Aptos"]
        self.facts = {
            "securitize_platform_value_display_usd": "4800000000",
            "circle_usyc_display_usd": "2400000000",
            "anchorage_total_buidl_usd": "10",
            "buidl_nav_usd": "1",
            "anchorage_ethereum_usdtb_redeemable": "50",
            "anchorage_total_usdtb_redeemable": "100",
            "anchorage_reserve_legs": [
                {"chain": chain.lower(), "buidl_usd": str(i), "custody_address": f"wallet{i}"}
                for i, chain in enumerate(chains, 1)
            ],
        }
        legs = [f"{chain} BUIDL ${i}\n{chain} BUIDL refers to the BUIDL held on {chain} at wallet{i}"
                for i, chain in enumerate(chains, 1)]
        self.texts = {
            "securitize": "total Tokenized Assets on Platform of $4.8 billion as of September 30, 2026 "
                          "across both funds and equities",
            "circle": "    $2.4B\n    USYC assets",
            "anchorage": "September 30, 2026\nTotal BUIDL $10\nCompany self-custodied 10 BUIDL\n"
                         "d. Total USDtb redeemable 50 50 100\n" + "\n".join(legs),
        }

    def test_matching_synthetic_publisher_text(self):
        self.assertEqual(verify_pdf_facts.verify(self.facts, self.texts), 15)

    def test_each_value_and_address_mismatch_is_rejected(self):
        cases = [
            ("securitize", "$4.8", "$4.9", "Securitize platform value"),
            ("circle", "$2.4B", "$2.5B", "Circle USYC assets"),
            ("anchorage", "Total BUIDL $10", "Total BUIDL $11", "Anchorage total BUIDL"),
            ("anchorage", "self-custodied 10", "self-custodied 11", "BUIDL fair value"),
            ("anchorage", "redeemable 50", "redeemable 60", r"USDtb redeemable \(ethereum\)"),
            ("anchorage", "50 50 100", "50 50 110", r"USDtb redeemable \(total\)"),
        ]
        for i, chain in enumerate(("Solana", "BSC", "Avalanche", "Aptos"), 1):
            cases.extend([
                ("anchorage", f"{chain} BUIDL ${i}", f"{chain} BUIDL $99", f"{chain} BUIDL value"),
                ("anchorage", f"at wallet{i}", "at wrongWallet", f"{chain} custody location"),
            ])
        for source, old, new, error in cases:
            with self.subTest(check=error):
                texts = {**self.texts, source: self.texts[source].replace(old, new)}
                with self.assertRaisesRegex(ValueError, error):
                    verify_pdf_facts.verify(self.facts, texts)

        facts = deepcopy(self.facts)
        facts["anchorage_reserve_legs"].pop()
        with self.assertRaisesRegex(ValueError, "Schedule II chain set"):
            verify_pdf_facts.verify(facts, self.texts)

    def test_missing_source_structure_is_rejected(self):
        cases = [
            ("securitize", "across both funds and equities", "structure"),
            ("circle", "USYC assets", "missing USYC assets column"),
            ("anchorage", "September 30, 2026", "structure"),
            ("anchorage", "Total USDtb redeemable", "structure"),
        ]
        for source, label, error in cases:
            with self.subTest(label=label):
                texts = {**self.texts, source: self.texts[source].replace(label, "")}
                with self.assertRaisesRegex(ValueError, error):
                    verify_pdf_facts.verify(self.facts, texts)


class ReplayTest(unittest.TestCase):
    def assert_comparisons(self, row, matching, different):
        args = row["url"], row["method"], row["params"]
        with patch.object(replay_evidence, "read", side_effect=[matching, different]) as read:
            self.assertTrue(replay_evidence.compare_rpc(row))
            self.assertFalse(replay_evidence.compare_rpc(row))
        self.assertEqual(read.call_count, 2)
        read.assert_called_with(*args)

    def test_replay_compares_values_and_reports_endpoint_errors(self):
        row = {"url": "https://eth.drpc.org", "method": "eth_call", "params": [{}, "0xa"], "result": "0x12"}
        self.assert_comparisons(row, "0x12", "0x13")
        with patch.object(replay_evidence, "read", side_effect=[OSError("primary failed"), "0x12"]) as read:
            self.assertTrue(replay_evidence.compare_rpc(row))
            read.assert_called_with("https://rpc.mevblocker.io", row["method"], row["params"])
        with patch.object(replay_evidence, "read", side_effect=OSError("offline")):
            label, status, detail = replay_evidence.run(("item", replay_evidence.compare_rpc, (row,)), 0)
        self.assertEqual((label, status), ("item", "error"))
        self.assertIn("offline", detail)

    def test_replay_checks_candidate_sets_and_saved_log_fields(self):
        base = {"url": "https://eth.drpc.org", "method": "eth_getLogs", "params": [{}]}
        words = ["0x" + f"{value:064x}" for value in (0, 1, 2)]
        log = {"topics": words, "data": "0x0"}
        candidate_row = {**base, "candidates": ["0x" + word[-40:] for word in words[1:]]}
        self.assert_comparisons(candidate_row, [log], [{**log, "topics": words[:2]}])
        saved_log = {**base, "result": [log]}
        self.assert_comparisons(saved_log, [{**log, "blockTimestamp": "0x1"}], [])
        self.assert_comparisons(saved_log, [log], [{**log, "data": "0x1"}])

    def test_replay_checks_code_bytes_and_type(self):
        row = {"url": "https://eth.drpc.org", "method": "eth_getCode", "params": ["0x01", "0xa"],
               "sha256": sha256(bytes.fromhex("6001")).hexdigest(), "code_type": "contract code"}
        self.assert_comparisons(row, "0x6001", "0x6002")
        with patch.object(replay_evidence, "read", return_value="0x6001"):
            self.assertFalse(replay_evidence.compare_rpc({**row, "code_type": "no runtime code"}))

    def test_replay_checks_safe_list_counts(self):
        base = {"url": "https://eth.drpc.org", "method": "eth_call", "params": [{}, "0xa"]}
        for count_key, offset in (("owner_count", [32]), ("module_count", [64, 1])):
            with self.subTest(count_key=count_key):
                one = "0x" + "".join(f"{word:064x}" for word in [*offset, 1, 3])
                empty = "0x" + "".join(f"{word:064x}" for word in [*offset, 0])
                self.assert_comparisons({**base, count_key: 1}, one, empty)
        last_page = "0x" + "".join(f"{word:064x}" for word in (64, 1, 1, 3))
        has_more = "0x" + "".join(f"{word:064x}" for word in (64, 3, 1, 3))
        self.assert_comparisons({**base, "module_count": 1, "additional_module_pages": False},
                                last_page, has_more)

    def test_replay_checks_transaction_signature(self):
        row = {"url": "https://eth.drpc.org", "method": "eth_getTransactionByHash", "params": ["0x12"],
               "result": {"hash": "0x12", "signature_present": True}}
        signed = {"hash": "0x12", "r": "0x1", "s": "0x2"}
        self.assert_comparisons(row, signed, {**signed, "r": "0x0"})


if __name__ == "__main__":
    unittest.main()
