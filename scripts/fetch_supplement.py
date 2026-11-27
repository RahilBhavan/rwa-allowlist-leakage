"""Capture bounded holder, bridge and current non-EVM reads."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from urllib.request import Request, urlopen

from fetch_evm import TRANSFER, balance, read
from holder_audit import holder_type
from review_evidence import IMPLEMENTATION_SLOT

ROOT = Path(__file__).resolve().parents[1]
FEED = "https://public-feed.securitize.io/asset-info?symbol=BUIDL"
APTOS = "https://api.mainnet.aptoslabs.com/v1"
APTOS_ASSET = "0x50038be55be5b964cfa32cf128b5cf05f123959f286b4cc02b86cafd48945f89"
SOLANA = "https://api.mainnet-beta.solana.com"
MINTS = {
    "buidl": "GyWgeqpy5GueU2YbkE8xqUeVEokCMMCEeUrfbtMw6phr",
    "ustb": "CCz3SGVziFeLYk2xfEstkiqJfYkjaSWb2GCABYsVcjo2",
    "usyc": "7LWanZteUKtvFjv4MHYgKXXdAuCQYFPJysL9pxxdRQGn",
    "ousg": "i7u4r16TcsJTgq1kAG8opmVZyVnAKBwLKu6ZPMwzxNc",
    "benji": "5Tu84fKBpe9vfXeotjvfvWdWbAjy3hqsExvuHgFqFxA1",
}
INDEXES = {
    "arbitrum": "https://arbitrum.blockscout.com",
    "base": "https://base.blockscout.com",
    "optimism": "https://optimism.blockscout.com",
    "plume": "https://explorer.plume.org",
    "polygon": "https://polygon.blockscout.com",
    "tempo": "https://explore.tempo.xyz",
}
SMALL = (
    "buidl/arbitrum", "buidl/optimism", "buidl/polygon", "buidl/tempo",
    "benji/arbitrum", "benji/base", "benji/polygon", "ustb/plume",
)
ZERO = "0x" + "0" * 40


def fetch_json(url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    request = Request(url, data, {"Content-Type": "application/json", "User-Agent": "rwa-allowlist-study/1"})
    with urlopen(request, timeout=10) as response:
        return json.load(response), response.headers


def observation(url, method, params, call=read):
    row = {"url": url, "method": method, "params": params}
    try:
        row["result"] = call(url, method, params)
    except (OSError, ValueError, KeyError) as error:
        row["error"] = str(error)
    return row


def solana_observation(item):
    fund, mint = item
    params = [mint, {"commitment": "finalized"}]
    supply = observation(SOLANA, "getTokenSupply", params)
    attempts = []
    for url in (SOLANA, "https://solana.api.pocket.network", "https://solana-rpc.publicnode.com"):
        largest = observation(url, "getTokenLargestAccounts", params)
        attempts.append(largest)
        if "result" in largest:
            break
    return fund, {"supply": supply, "largest_attempts": attempts}


def aptos_view(url, method, params):
    result, headers = fetch_json(url, params if method == "POST" else None)
    return {"ledger_version": headers["x-aptos-ledger-version"], "value": result}


def scan(capture):
    chain = capture["target"]["chain"]
    token = capture["target"]["token"]
    url = capture["reads"]["supply"]["url"]
    pin = capture["block"]["number"]
    index = f"{INDEXES[chain]}/api/v2/tokens/{token}/holders"
    candidates = set()
    try:
        result, _ = fetch_json(index)
        candidates.update(row["address"]["hash"].lower() for row in result["items"][:12])
        index_status = {"url": index, "candidates": sorted(candidates)}
    except (OSError, ValueError, KeyError) as error:
        index_status = {"url": index, "error": str(error)}
    query = {"address": token, "topics": [TRANSFER],
             "fromBlock": hex(int(pin, 16) - 999), "toBlock": pin}
    logs = observation(url, "eth_getLogs", [query])
    if "result" in logs:
        logs["candidates"] = sorted({"0x" + topic[-40:].lower() for row in logs.pop("result")
                                     for topic in row["topics"][1:3]})
        candidates.update(logs["candidates"][:12])
    reads = {}
    for address in sorted(candidates - {ZERO}):
        to, data = balance(token, address)
        label = f"balance/{address}"
        reads[label] = observation(url, "eth_call", [{"to": to, "data": data}, pin])
        if int(reads[label].get("result", "0x0").removeprefix("0x") or "0", 16):
            code = observation(url, "eth_getCode", [address, pin])
            if "result" in code:
                result = code.pop("result")
                code.update(code_type=holder_type(result), sha256=sha256(bytes.fromhex(result[2:])).hexdigest())
            reads[f"code/{address}"] = code
    receipt_reads = {}
    if chain == "plume":
        for label, row in reads.items():
            if row.get("code_type") == "contract code":
                address = label.split("/")[1]
                receipt_reads[f"symbol/{address}"] = observation(
                    url, "eth_call", [{"to": address, "data": "0x95d89b41"}, pin])
    return {"index": index_status, "logs": logs, "reads": reads, "receipt_reads": receipt_reads}


def bridge_observations(targets):
    feed, _ = fetch_json(FEED)
    captures = {}
    for record in feed["data"]:
        bridge = (record["BridgeAddress"] or "").strip().lower()
        if not bridge:
            continue
        chain = {"bnb": "bsc"}.get(record["blockchain"], record["blockchain"])
        deployment = f'{record["symbol"].lower()}/{chain}'
        capture = targets[deployment]
        token = capture["target"]["token"]
        if token != record["TokenAddress"].lower():
            raise ValueError(f"issuer bridge listing token differs for {deployment}")
        pinned = capture["reads"]["supply"]
        to, data = balance(token, bridge)
        pin = capture["block"]["number"]
        captures[deployment] = {
            "address": bridge,
            "balance": observation(pinned["url"], "eth_call", [{"to": to, "data": data}, pin]),
            "implementation": observation(pinned["url"], "eth_getStorageAt", [bridge, IMPLEMENTATION_SLOT, pin]),
        }
    checks = {}
    path = "contracts/bridge/SecuritizeBridge.sol"
    for deployment, chain_id in (("buidl/ethereum", 1), ("buidl/bsc", 56)):
        slot = captures[deployment]["implementation"].get("result")
        if slot is None:
            continue
        source_url = f"https://sourcify.dev/server/v2/contract/{chain_id}/0x{slot[-40:]}?fields=sources"
        try:
            source, _ = fetch_json(source_url)
            content = source["sources"][path]["content"]
        except (OSError, ValueError, KeyError) as error:
            checks[deployment] = {"url": source_url, "error": str(error)}
        else:
            checks[deployment] = {"url": source_url, "path_in_compiler_input": path,
                                  "utf8_source_sha256": sha256(content.encode()).hexdigest()}
    return {"url": FEED, "deployments": captures, "source_checks": checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    targets = json.loads((ROOT / "evidence/holders-2026-09-30.json").read_text())["targets"]
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with ThreadPoolExecutor(max_workers=4) as pool:
        solana = dict(pool.map(solana_observation, MINTS.items()))
        small = dict(zip(SMALL, pool.map(scan, (targets[key] for key in SMALL))))
    aptos = {
        "supply": observation(f"{APTOS}/view", "POST", {
            "function": "0x1::fungible_asset::supply",
            "type_arguments": ["0x1::fungible_asset::Metadata"], "arguments": [APTOS_ASSET],
        }, aptos_view),
        "metadata": observation(f"{APTOS}/accounts/{APTOS_ASSET}/resource/0x1::fungible_asset::Metadata",
                                "GET", None, aptos_view),
    }
    if "result" in aptos["metadata"]:
        metadata = aptos["metadata"]["result"]
        metadata["value"] = {key: metadata["value"]["data"][key] for key in ("name", "symbol", "decimals")}
    output = {"as_of_utc": started, "solana": solana, "aptos": aptos,
              "issuer_bridge": bridge_observations(targets), "holder_probes": small}
    with args.output.open("x") as handle:
        handle.write(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
