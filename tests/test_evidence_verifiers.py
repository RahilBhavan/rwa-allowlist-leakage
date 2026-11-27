from copy import deepcopy
from contextlib import redirect_stderr, redirect_stdout
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import unittest
from urllib.error import HTTPError
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
            "circle": "    $2.4B\n    USYC assets\nSource: Company data as of September 30, 2026",
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
        facts = deepcopy(self.facts)
        facts["anchorage_reserve_legs"].append(facts["anchorage_reserve_legs"][0])
        with self.assertRaisesRegex(ValueError, "Schedule II chain set"):
            verify_pdf_facts.verify(facts, self.texts)

    def test_missing_source_structure_is_rejected(self):
        cases = [
            ("securitize", "across both funds and equities", "structure"),
            ("circle", "USYC assets", "missing USYC assets column"),
            ("circle", "September 30, 2026", "structure"),
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

    def test_replay_checks_exact_log_cardinality_and_recorded_fields(self):
        base = {"url": "https://eth.drpc.org", "method": "eth_getLogs", "params": [{}]}
        words = ["0x" + f"{value:064x}" for value in (0, 1, 2)]
        log = {"topics": words, "data": "0x0"}
        saved_log = {**base, "result": [log]}
        self.assert_comparisons(saved_log, [{**log, "blockTimestamp": "0x1"}], [])
        self.assert_comparisons(saved_log, [log], [{**log, "data": "0x1"}])
        self.assert_comparisons(saved_log, [log], [log, deepcopy(log)])
        other = {**log, "topics": words[:2]}
        self.assert_comparisons({**base, "result": [log, other]}, [log, other], [other, log])
        self.assert_comparisons({**base, "result": []}, [], [log])

    def test_replay_checks_code_bytes_and_type(self):
        row = {"url": "https://eth.drpc.org", "method": "eth_getCode", "params": ["0x01", "0xa"],
               "sha256": sha256(bytes.fromhex("6001")).hexdigest(), "code_type": "contract code"}
        self.assert_comparisons(row, "0x6001", "0x6002")
        with patch.object(replay_evidence, "read", return_value="0x6001"):
            self.assertFalse(replay_evidence.compare_rpc({**row, "code_type": "no runtime code"}))

    def test_replay_checks_normalized_plugin_code_and_literal_count(self):
        address = b"\x12" * 20
        code = b"\x73" + address + b"\x60\x00"
        row = {"url": "rpc", "method": "eth_getCode", "params": ["0x01", "0xa"],
               "sha256": sha256(code).hexdigest(), "code_type": "contract code",
               "normalized_sha256": sha256(b"\x73" + bytes(20) + b"\x60\x00").hexdigest(),
               "pool_literal": "0x" + address.hex(), "literal_count": 1}
        with patch.object(replay_evidence, "read", return_value="0x" + code.hex()):
            self.assertTrue(replay_evidence.compare_rpc(row))
            self.assertFalse(replay_evidence.compare_rpc({**row, "literal_count": 2}))
            self.assertFalse(replay_evidence.compare_rpc({**row, "normalized_sha256": row["sha256"]}))

    def test_replay_checks_safe_list_counts(self):
        base = {"url": "https://eth.drpc.org", "method": "eth_call", "params": [{}, "0xa"]}
        for count_key, offset in (("owner_count", [32]), ("module_count", [64, 1])):
            with self.subTest(count_key=count_key):
                one = "0x" + "".join(f"{word:064x}" for word in [*offset, 1, 3])
                empty = "0x" + "".join(f"{word:064x}" for word in [*offset, 0])
                self.assert_comparisons({**base, count_key: 1}, one, empty)
                self.assert_comparisons({**base, count_key: 1}, one, one[:-64])
        last_page = "0x" + "".join(f"{word:064x}" for word in (64, 1, 1, 3))
        has_more = "0x" + "".join(f"{word:064x}" for word in (64, 3, 1, 3))
        self.assert_comparisons({**base, "module_count": 1, "additional_module_pages": False},
                                last_page, has_more)

    def test_replay_checks_transaction_signature(self):
        row = {"url": "https://eth.drpc.org", "method": "eth_getTransactionByHash", "params": ["0x12"],
               "result": {"hash": "0x12", "signature_present": True}}
        signed = {"hash": "0x12", "r": "0x1", "s": "0x2"}
        self.assert_comparisons(row, signed, {**signed, "r": "0x0"})

    def test_block_and_ledger_compare_pinned_identity(self):
        block = {"number": "0x12", "hash": "0xcafe", "timestamp": "0x34"}
        url = "https://rpc.plume.org"
        with patch.object(replay_evidence, "read", side_effect=[
            {**block, "transactions": []}, {**block, "hash": "0xbeef"},
        ]) as read:
            self.assertTrue(replay_evidence.compare_block(url, block))
            self.assertFalse(replay_evidence.compare_block(url, block))
            read.assert_called_with(url, "eth_getBlockByNumber", ["0x12", False])
        ledger = {"index": 42, "hash": "AB"}
        with patch.object(replay_evidence, "header", side_effect=[ledger, {**ledger, "hash": "CD"}]) as head:
            self.assertTrue(replay_evidence.compare_ledger(ledger))
            self.assertFalse(replay_evidence.compare_ledger(ledger))
            head.assert_called_with(42)

    def test_bnb_receipt_retains_transfer_cardinality_and_receipt_fields(self):
        transfer = {"address": "0xabc", "topics": [replay_evidence.TRANSFER], "data": "0x01"}
        fixture = {"url": "rpc", "transaction_receipt": {"params": ["0x123"], "result": {"status": "0x1"}},
                   "matched_logs": [transfer]}
        cases = [
            ({"status": "0x1", "logs": [{**transfer, "index": "0x0"}, {**transfer, "address": "0xdef"}]}, True),
            ({"status": "0x1", "logs": [transfer, transfer]}, False),
            ({"status": "0x0", "logs": [transfer]}, False),
        ]
        for response, expected in cases:
            with self.subTest(expected=expected), patch.object(replay_evidence, "read", return_value=deepcopy(response)) as read:
                self.assertEqual(replay_evidence.compare_bnb_receipt(fixture), expected)
                read.assert_called_once_with("rpc", "eth_getTransactionReceipt", ["0x123"])

    def test_xrpl_projects_only_intended_fields_but_rejects_balance_and_marker_changes(self):
        currency = replay_evidence.OUSG_XRPL_CURRENCY
        line = {"account": "rHolder", "currency": currency, "balance": "-5", "authorized": True}
        cases = (
            ("account_lines", {"lines": [line]},
             {"lines": [{**line, "limit": "0"}, {**line, "currency": "USD"}]},
             {"lines": [line], "marker": "extra-page"}),
            ("account_lines", {"lines": [line], "marker": "next"},
             {"lines": [line], "marker": "next"}, {"lines": [{**line, "balance": "-6"}], "marker": "next"}),
            ("account_info", {"account_data": {"Domain": "AA"}, "account_flags": {"requireAuth": True}},
             {"account_data": {"Domain": "AA", "Sequence": 1},
              "account_flags": {"requireAuth": True, "globalFreeze": False}},
             {"account_data": {"Domain": "AA"}, "account_flags": {"requireAuth": False}}),
            ("gateway_balances", {"obligations": {currency: "5"}},
             {"obligations": {currency: "5", "USD": "8"}}, {"obligations": {currency: "6"}}),
        )
        for method, saved, matching, different in cases:
            row = {"params": [{"ledger_index": 42}], "result": saved}
            with self.subTest(method=method), patch.object(
                replay_evidence, "request", side_effect=[deepcopy(matching), deepcopy(different)]
            ) as request:
                self.assertTrue(replay_evidence.compare_xrpl(method, row))
                self.assertFalse(replay_evidence.compare_xrpl(method, row))
                request.assert_called_with(method, row["params"])

    def test_source_replay_distinguishes_unknown_contract_from_failed_request(self):
        url = "https://example.org/contract"
        expected = {"reported_contract": "Proxy", "match": "exact_match", "proxy": True,
                    "implementations": ["0x1"]}
        contract = {"compilation": {"name": "Proxy"}, "match": "exact_match",
                    "proxyResolution": {"isProxy": True, "implementations": [{"address": "0x1"}]}}
        with patch.object(replay_evidence, "fetch_json", side_effect=[
            (contract, {}), ({**contract, "proxyResolution": None}, {}),
        ]):
            self.assertTrue(replay_evidence.compare_discovery(url, expected))
            self.assertFalse(replay_evidence.compare_discovery(url, expected))
        for status, match, accepted in ((404, None, True), (404, "exact_match", False), (500, None, False)):
            error = HTTPError(url, status, "offline", None, None)
            with self.subTest(status=status, match=match), error, patch.object(
                replay_evidence, "fetch_json", side_effect=error
            ):
                if accepted:
                    self.assertTrue(replay_evidence.compare_discovery(url, {"match": match}))
                else:
                    with self.assertRaises(HTTPError):
                        replay_evidence.compare_discovery(url, {"match": match})

    def test_replay_hashes_source_text_instead_of_the_outer_json(self):
        program = "contract Audit {}\n"
        row = {"url": "https://example.org/source", "path_in_compiler_input": "Audit.sol",
               "utf8_source_sha256": sha256(program.encode()).hexdigest()}
        compiler = {"sources": {"Audit.sol": {"content": program}}}
        for check, body in (
            (replay_evidence.compare_usual, {"result": [{"SourceCode": "{" + json.dumps(compiler) + "}"}]}),
            (replay_evidence.compare_usual, {"result": [{"SourceCode": json.dumps(compiler)}]}),
            (replay_evidence.compare_bridge_source, compiler),
        ):
            with self.subTest(check=check.__name__), patch.object(replay_evidence, "fetch_json", return_value=(body, {})):
                self.assertTrue(check(row))
                self.assertFalse(check({**row, "utf8_source_sha256": sha256(program.rstrip().encode()).hexdigest()}))
        explorer = {"name": "Audit", "source_code": program, "deployed_bytecode": "0x6011", "verified_at": "today"}
        expected = {"url": row["url"], "name": "Audit", "source_utf8_sha256": row["utf8_source_sha256"],
                    "deployed_bytecode_sha256": sha256(bytes.fromhex("6011")).hexdigest()}
        with patch.object(replay_evidence, "fetch_json", return_value=(explorer, {})):
            self.assertTrue(replay_evidence.compare_explorer_source(expected))
            self.assertFalse(replay_evidence.compare_explorer_source({**expected, "name": "Other"}))
            self.assertFalse(replay_evidence.compare_explorer_source({**expected, "source_utf8_sha256": "0"}))
            self.assertFalse(replay_evidence.compare_explorer_source({**expected, "deployed_bytecode_sha256": "0"}))

    def test_dispatch_covers_special_fixtures_and_includes_only_replayable_reads(self):
        evidence = Path(replay_evidence.ROOT, "evidence")
        targets = {
            "buidl-avalanche-signer": ("transaction", replay_evidence.compare_rpc),
            "usyc-bnb-receipt-2026-09-25": ("receipt", replay_evidence.compare_bnb_receipt),
            "ousg-xrpl-2026-09-30": ("account_lines/1", replay_evidence.compare_xrpl),
            "round1-supplement": ("ustb/plume/logs", replay_evidence.compare_rpc),
            "round2-readbacks": ("usyc/ethereum/successor", replay_evidence.compare_block),
            "pinned-market-controls-2026-09-30": ("ethereum/flux/getAllMarkets()", replay_evidence.compare_rpc),
        }
        for name in replay_evidence.PINNED + replay_evidence.DISCOVERY:
            fixture = json.loads((evidence / f"{name}.json").read_text())
            plan = list(replay_evidence.jobs(name, fixture))
            with self.subTest(fixture=name):
                self.assertTrue(plan)
                if name in targets:
                    self.assertIn(targets[name], [(label, check) for label, check, _ in plan])
                for _, check, args in plan:
                    if check == replay_evidence.compare_rpc:
                        self.assertNotIn("error", args[0])

    def test_cli_returns_failure_for_mismatch_and_unknown_requested_read(self):
        args = ["replay", "--fixture", "buidl-avalanche-signer", "--pause", "0"]
        with patch("sys.argv", args), patch.object(replay_evidence, "compare_rpc", return_value=False), redirect_stdout(StringIO()) as output:
            self.assertEqual(replay_evidence.main(), 1)
        self.assertIn("buidl-avalanche-signer/transaction: mismatch", output.getvalue())
        with patch("sys.argv", [*args, "--read", "missing-job"]), redirect_stderr(StringIO()) as error:
            with self.assertRaises(SystemExit) as failure:
                replay_evidence.main()
        self.assertEqual(failure.exception.code, 2)
        self.assertIn("unrecognized replay read(s)", error.getvalue())


if __name__ == "__main__":
    unittest.main()
