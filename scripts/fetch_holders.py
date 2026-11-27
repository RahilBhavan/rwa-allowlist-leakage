"""Discover candidate addresses and read their holdings at the September pin."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

from fetch_evm import CHAINS, CUTOFF, TRANSFER, balance, decimals, find_block, read, supply

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "evidence" / "holder-targets.json"
ZERO = "0x" + "0" * 40
PAGE_SIZE = 1000
MAX_LOG_PAGES = 6
INDEX_LIMIT = 25


def get(url):
    with urlopen(url, timeout=8) as response:
        return json.load(response)


def error_detail(error):
    if isinstance(error, HTTPError):
        return f"{error}: {error.read(400).decode(errors='replace')}"
    return str(error)


def indexed_candidates(target, base, height, output, log_pages, index_limit):
    addresses = set()
    index_url = f"{base}/erc20/{target['token']}/holders"
    try:
        page = get(index_url)
        items = page["items"][:index_limit]
        output["holder_index"] = {"url": index_url, "items": items}
        addresses.update(item["address"].lower() for item in items)
    except (OSError, ValueError, KeyError) as error:
        output["failures"]["holder_index"] = error_detail(error)

    # An explorer is a discovery tool. Its pagination or event semantics
    # cannot establish completeness. Historical balanceOf is authoritative.
    net = Counter()
    pages = []
    for page_number in range(1, log_pages + 1):
        url = f"{base}/etherscan/api?" + urlencode({
            "module": "logs", "action": "getLogs", "address": target["token"],
            "topic0": TRANSFER, "fromBlock": 0, "toBlock": height,
            "page": page_number, "offset": PAGE_SIZE,
        })
        try:
            response = get(url)
            rows = response["result"]
            if not isinstance(rows, list):
                raise ValueError(response["message"])
        except (OSError, ValueError, KeyError) as error:
            output["failures"]["indexed_logs"] = {"url": url, "error": error_detail(error)}
            break
        pages.append({"url": url, "rows": len(rows)})
        for row in rows:
            topics = row["topics"]
            data = row["data"]
            if len(topics) < 3 or topics[0].lower() != TRANSFER or len(data) != 66:
                continue
            source, dest = ("0x" + topic[-40:].lower() for topic in topics[1:3])
            units = int(data, 16)
            net[source] -= units
            net[dest] += units
        if len(rows) < PAGE_SIZE:
            break
    net.pop(ZERO, None)
    leads = [address for address, units in net.most_common(index_limit) if units > 0]
    output["indexed_logs"] = {"pages": pages, "net_positive_leads": leads}
    addresses.update(leads)
    return addresses


def capture(target, chain_options, log_pages=MAX_LOG_PAGES, index_limit=INDEX_LIMIT):
    chain, token = target["chain"], target["token"]
    height, endpoints = chain_options[chain]
    output = {"target": target, "reads": {}, "failures": {}}
    headers = {}
    for url in endpoints:
        try:
            block, successor = find_block(url, height)
        except (OSError, ValueError) as error:
            output["failures"][url] = error_detail(error)
            continue
        if "block" in output and (block != output["block"] or successor != output["successor"]):
            raise ValueError(f"conflicting {chain} pins")
        output.update(block=block, successor=successor)
        headers[url] = block["number"]
    if not headers:
        return output

    def probe(label, method, *args):
        failures = {}
        for url, block in headers.items():
            params = [*args, block]
            try:
                result = read(url, method, params)
                if method == "eth_call" and result == "0x":
                    raise ValueError("empty call result")
            except (OSError, ValueError) as error:
                failures[url] = error_detail(error)
            else:
                output["reads"][label] = dict(url=url, method=method, params=params, result=result)
                return result
        output["failures"][label] = failures
        return None

    def call(label, address, data):
        return probe(label, "eth_call", {"to": address, "data": data})

    call("supply", *supply(token))
    call("decimals", *decimals(token))
    addresses = set(target.get("leads", {}))
    network_id = target.get("routescan_id")
    if network_id is not None:
        base = f"https://api.routescan.io/v2/network/mainnet/evm/{network_id}"
        addresses.update(indexed_candidates(
            target, base, int(output["block"]["number"], 16), output, log_pages, index_limit
        ))
    addresses.discard(ZERO)
    output["candidates"] = sorted(addresses)
    for address in output["candidates"]:
        amount = call(f"balance/{address}", *balance(token, address))
        if amount is not None and int(amount, 16):
            probe(f"code/{address}", "eth_getCode", address)
    for label, spec in target.get("probes", {}).items():
        probe(label, *spec)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--target", action="append")
    parser.add_argument("--log-pages", type=int, choices=range(MAX_LOG_PAGES + 1), default=MAX_LOG_PAGES)
    parser.add_argument("--index-limit", type=int, choices=range(INDEX_LIMIT + 1), default=INDEX_LIMIT)
    parser.add_argument("--config", type=Path, default=CONFIG)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    options = {chain: (height, endpoints) for chain, (height, endpoints, _) in CHAINS.items()}
    options.update(config["chains"])
    targets = config["targets"]
    if args.target:
        unknown = set(args.target) - targets.keys()
        if unknown:
            parser.error(f"unknown targets: {', '.join(sorted(unknown))}")
        targets = {key: targets[key] for key in args.target}
    with ThreadPoolExecutor(max_workers=4) as executor:
        reports = executor.map(
            lambda target: capture(target, options, args.log_pages, args.index_limit), targets.values()
        )
        output = dict(zip(targets, reports))
    args.output.write_text(json.dumps({"cutoff": CUTOFF, "targets": output}, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
