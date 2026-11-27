"""Read OUSG trust lines at the September month-end XRP Ledger pin."""
import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen

from fetch_evm import CUTOFF

URL = "https://s2.ripple.com:51234/"
ISSUER = "rHuiXXjHLpMP8ZE9sSQU5aADQVWDwv6h5p"
RIPPLE_EPOCH = 946684800


def request(method, params):
    query = Request(URL, json.dumps({"method": method, "params": [params]}).encode(),
                    {"Content-Type": "application/json"})
    with urlopen(query, timeout=6) as response:
        result = json.load(response)["result"]
    if result["status"] != "success":
        raise ValueError(f"{method} {params}: {result}")
    return result


def header(index):
    result = request("ledger", {"ledger_index": index})
    ledger = result["ledger"]
    return {"index": int(result["ledger_index"]), "hash": ledger["ledger_hash"],
            "parent": ledger["parent_hash"], "timestamp": ledger["close_time"] + RIPPLE_EPOCH}


def capture():
    # The average close interval is just a locator. Verify the adjacent
    # trusted ledger headers before taking any state.
    high = header("validated")
    low = header(max(1, high["index"] - 4_000_000))
    if not low["timestamp"] <= CUTOFF < high["timestamp"]:
        raise ValueError("ledger locator did not bracket cutoff")
    while high["index"] - low["index"] > 1:
        middle = header((high["index"] + low["index"]) // 2)
        if middle["timestamp"] <= CUTOFF:
            low = middle
        else:
            high = middle
    if high["parent"] != low["hash"]:
        raise ValueError("headers are not adjacent")
    pages = []
    params = {"account": ISSUER, "ledger_hash": low["hash"], "limit": 400}
    for _ in range(20):
        page = request("account_lines", params)
        pages.append({"params": params.copy(), "result": page})
        if "marker" not in page:
            output = {"url": URL, "cutoff": CUTOFF, "ledger": low, "successor": high, "pages": pages}
            issuer_params = {"account": ISSUER, "ledger_hash": low["hash"]}
            for method in ("account_info", "gateway_balances"):
                output[method] = {"params": issuer_params, "result": request(method, issuer_params)}
            return output
        params["marker"] = page["marker"]
    raise ValueError("trust line query exceeded the page ceiling")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(capture(), indent=2) + "\n")
