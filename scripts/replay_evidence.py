"""Compare saved chain reads and source manifests against keyless live endpoints."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
from time import sleep
from urllib.error import HTTPError

if __package__:
    from .fetch_evm import TRANSFER, read
    from .fetch_supplement import fetch_json
    from .fetch_xrpl_holders import header, request
    from .holder_audit import OUSG_XRPL_CURRENCY, holder_type
    from .review_evidence import abi_words
else:
    from fetch_evm import TRANSFER, read
    from fetch_supplement import fetch_json
    from fetch_xrpl_holders import header, request
    from holder_audit import OUSG_XRPL_CURRENCY, holder_type
    from review_evidence import abi_words

ROOT = Path(__file__).resolve().parents[1]
PINNED = ("evm-2026-09-30", "holders-2026-09-30", "review-ethereum-2026-09-30",
          "buidl-avalanche-signer", "usyc-bnb-receipt-2026-09-25", "ousg-xrpl-2026-09-30",
          "round1-supplement", "round2-readbacks", "pinned-market-controls-2026-09-30")
DISCOVERY = ("review-contract-discovery", "usual-source-2026-09-30")
RPC_ALTERNATIVES = {
    "https://arbitrum.drpc.org": "https://arbitrum-one-rpc.publicnode.com",
    "https://arbitrum-one.public.blastapi.io": "https://arbitrum.drpc.org",
    "https://eth.drpc.org": "https://rpc.mevblocker.io",
    "https://optimism.drpc.org": "https://mainnet.optimism.io",
}


def fields(actual, expected):
    """Project a live object to the fields preserved by the public fixture."""
    return {key: actual[key] for key in expected}


def historical_read(url, method, params):
    try:
        return read(url, method, params)
    except (OSError, ValueError) as error:
        alternate = RPC_ALTERNATIVES.get(url)
        if not alternate:
            raise
        try:
            return read(alternate, method, params)
        except (OSError, ValueError) as fallback_error:
            raise ValueError(f"{url}: {error}; {alternate}: {fallback_error}") from fallback_error


def compare_rpc(row):
    actual = historical_read(row["url"], row["method"], row["params"])
    if "sha256" in row:
        code = bytes.fromhex(actual[2:])
        if holder_type(actual) != row["code_type"] or sha256(code).hexdigest() != row["sha256"]:
            return False
        if "normalized_sha256" in row:
            literal = bytes.fromhex(row["pool_literal"][2:])
            return (code.count(literal) == row["literal_count"]
                    and sha256(code.replace(literal, bytes(len(literal)))).hexdigest() == row["normalized_sha256"])
        return True
    for key in ("owner_count", "module_count"):
        if key in row:
            words = abi_words(actual)
            offset = 1 if key == "owner_count" else 2
            return (len(words) > offset and words[0] == 32 * offset
                    and len(words) == offset + 1 + words[offset] and words[offset] == row[key]
                    and ("additional_module_pages" not in row
                         or (words[1] != 1) == row["additional_module_pages"]))
    expected = row["result"]
    if row["method"] == "eth_getTransactionByHash":
        actual["signature_present"] = bool(int(actual["r"], 16) and int(actual["s"], 16))
        actual = fields(actual, expected)
    elif row["method"] == "eth_getLogs":
        # Some Ethereum RPCs add blockTimestamp. Compare the recorded log fields.
        if len(actual) != len(expected):
            return False
        actual = [fields(log, saved) for log, saved in zip(actual, expected)]
    return actual == expected


def evm_jobs(capture):
    for key, value in capture.items():
        if key in ("reads", "receipt_reads"):
            for label, row in value.items():
                if "error" not in row:
                    yield label, compare_rpc, (row,)
        elif key in ("chains", "targets"):
            for item, target in value.items():
                for label, check, args in evm_jobs(target):
                    yield f"{item}/{label}", check, args
    if "block" in capture and capture.get("reads"):
        url = next(iter(capture["reads"].values()))["url"]
        for label in ("block", "successor"):
            yield label, compare_block, (url, capture[label])


def compare_block(url, expected):
    actual = historical_read(url, "eth_getBlockByNumber", [expected["number"], False])
    return fields(actual, expected) == expected


def compare_bnb_receipt(fixture):
    row = fixture["transaction_receipt"]
    live = read(fixture["url"], "eth_getTransactionReceipt", row["params"])
    token = fixture["matched_logs"][0]["address"]
    live["logs"] = [
        fields(log, ("address", "topics", "data")) for log in live["logs"]
        if log["address"].lower() == token and log["topics"] and log["topics"][0] == TRANSFER
    ]
    return fields(live, row["result"]) == row["result"] and live["logs"] == fixture["matched_logs"]


def compare_xrpl(method, row):
    actual = request(method, row["params"])
    expected = row["result"]
    if method == "account_lines":
        actual["lines"] = [{**fields(line, ("account", "currency", "balance")),
                            **({"authorized": line["authorized"]} if "authorized" in line else {})}
                           for line in actual["lines"] if line["currency"] == OUSG_XRPL_CURRENCY]
    elif method == "account_info":
        actual["account_data"] = fields(actual["account_data"], expected["account_data"])
        actual["account_flags"] = fields(actual["account_flags"], expected["account_flags"])
    elif method == "gateway_balances":
        actual["obligations"] = fields(actual["obligations"], expected["obligations"])
    return fields(actual, expected) == expected and actual.get("marker") == expected.get("marker")


def compare_ledger(expected):
    return header(expected["index"]) == expected


def compare_discovery(url, expected):
    try:
        live, _ = fetch_json(url)
    except HTTPError as error:
        if error.code == 404 and expected["match"] is None:
            return True
        raise
    proxy = live.get("proxyResolution") or {}
    return {
        "reported_contract": (live.get("compilation") or {}).get("name"),
        "match": live.get("match"), "proxy": proxy.get("isProxy"),
        "implementations": [row["address"] for row in proxy.get("implementations") or []],
    } == expected


def compare_usual(row):
    live, _ = fetch_json(row["url"])
    source = live["result"][0]["SourceCode"]
    compiler_input = json.loads(source[1:-1] if source.startswith("{{") else source)
    content = compiler_input["sources"][row["path_in_compiler_input"]]["content"]
    return sha256(content.encode()).hexdigest() == row["utf8_source_sha256"]


def compare_bridge_source(row):
    live, _ = fetch_json(row["url"])
    content = live["sources"][row["path_in_compiler_input"]]["content"]
    return sha256(content.encode()).hexdigest() == row["utf8_source_sha256"]


def compare_explorer_source(row):
    live, _ = fetch_json(row["url"])
    return (live["name"] == row["name"]
            and sha256(live["source_code"].encode()).hexdigest() == row["source_utf8_sha256"]
            and sha256(bytes.fromhex(live["deployed_bytecode"][2:])).hexdigest() == row["deployed_bytecode_sha256"])


def jobs(name, fixture):
    if name == "review-contract-discovery":
        for address, row in fixture["contracts"].items():
            yield address, compare_discovery, (fixture["source"].format(address=address), row)
    elif name.startswith("usual-source"):
        for label, row in fixture.items():
            yield label, compare_usual, (row,)
    elif name.startswith("ousg-xrpl"):
        for label in ("ledger", "successor"):
            yield label, compare_ledger, (fixture[label],)
        for i, row in enumerate(fixture["pages"], start=1):
            yield f"account_lines/{i}", compare_xrpl, ("account_lines", row)
        for label in ("account_info", "gateway_balances"):
            yield label, compare_xrpl, (label, fixture[label])
    elif name.startswith("usyc-bnb-receipt"):
        yield "receipt", compare_bnb_receipt, (fixture,)
        for i, row in enumerate(fixture["supply_change"]):
            yield f"supply_change/{i}", compare_rpc, (row,)
    elif name == "buidl-avalanche-signer":
        yield "transaction", compare_rpc, (fixture,)
    elif name == "round2-readbacks":
        for deployment, probe in fixture["pinned_safes"].items():
            url = probe["calls"]["master_copy"][0]["url"]
            for label in ("block", "successor"):
                yield f"{deployment}/{label}", compare_block, (url, probe[label])
            for label, attempts in probe["calls"].items():
                for row in attempts:
                    if "error" not in row:
                        yield f"{deployment}/{label}", compare_rpc, (row,)
    elif name == "round1-supplement":
        for label, row in fixture["issuer_bridge"]["deployments"].items():
            for probe in ("balance", "implementation"):
                if "result" in row[probe]:
                    yield f"bridge/{label}/{probe}", compare_rpc, (row[probe],)
        for label, row in fixture["issuer_bridge"].get("source_checks", {}).items():
            if "error" not in row:
                yield f"bridge-source/{label}", compare_bridge_source, (row,)
        for label, probe in fixture["holder_probes"].items():
            for read_label, check, args in evm_jobs(probe):
                yield f"{label}/{read_label}", check, args
            if "result" in probe["logs"]:
                yield f"{label}/logs", compare_rpc, (probe["logs"],)
    elif name == "pinned-market-controls-2026-09-30":
        yield from evm_jobs(fixture)
        for vault, sources in fixture["nest_sources"].items():
            for label in ("share", "hook", "authority"):
                yield f"{vault}/source/{label}", compare_explorer_source, (sources[label],)
        yield "rooster-v2/source/swap_plugin", compare_explorer_source, (fixture["rooster_swap_plugin"]["verified_twin"],)
    else:
        yield from evm_jobs(fixture)


def run(job, pause):
    label, check, args = job
    if pause:
        sleep(pause)
    try:
        return label, "match" if check(*args) else "mismatch", None
    except (OSError, ValueError, KeyError, IndexError, TypeError) as error:
        return label, "error", str(error)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", choices=PINNED + DISCOVERY, action="append",
                        help="limit to a named fixture (repeatable)")
    parser.add_argument("--workers", type=int, choices=range(1, 5), default=3)
    parser.add_argument("--pause", type=float, default=0.2, help="seconds before each job per worker")
    parser.add_argument("--read", action="append", help="rerun an exact FIXTURE/LABEL from the error output")
    args = parser.parse_args()
    if not 0 <= args.pause <= 5:
        parser.error("--pause must be between 0 and 5 seconds")
    pending = set(args.read or [])
    any_differences = False
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for name in args.fixture or PINNED + DISCOVERY:
            fixture = json.loads((ROOT / "evidence" / f"{name}.json").read_text())
            planned = []
            for job in jobs(name, fixture):
                identifier = f"{name}/{job[0]}"
                if not args.read or identifier in pending:
                    planned.append(job)
                    pending.discard(identifier)
            if not planned:
                continue
            counts = Counter()
            for label, status, detail in pool.map(lambda job: run(job, args.pause), planned):
                counts[status] += 1
                if status != "match":
                    print(f"{name}/{label}: {status}" + (f" ({detail})" if detail else ""))
            print(f"{name}: {counts['match']} match, {counts['mismatch']} mismatch, {counts['error']} error",
                  flush=True)
            any_differences |= bool(counts["mismatch"] or counts["error"])
    if pending:
        parser.error(f"unrecognized replay read(s): {sorted(pending)}")
    return int(any_differences)


if __name__ == "__main__":
    raise SystemExit(main())
