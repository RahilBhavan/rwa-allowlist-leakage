"""Capture keyless holder indications and pinned Safe controls for round two."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal
import json
from pathlib import Path
from urllib.parse import urlencode

from fetch_supplement import MINTS, SOLANA, fetch_json, observation
from review_evidence import abi_words

ROOT = Path(__file__).resolve().parents[1]
ISSUER = "GBHNGLLIE3KWGKCHIKMHJ5HVZHYIK7WTBE4QF5PLAKL4CJGSEU7HZIW5"
HORIZON = "https://horizon.stellar.org"
SAFES = {
    "buidl_i/ethereum": "0x68a99f89e475a078645f4bac491360afe255dff1",
    "buidl/optimism": "0xd06fc8c16fa5ab9e32f1bb5e3a41bc2212342d29",
    "usyc/ethereum": "0xb1a6ac52a21435c744b5b4129b07e6c44bcd629b",
}


def stellar_accounts(max_pages):
    asset = "BENJI"
    params = {"asset": f"{asset}:{ISSUER}", "limit": 200, "order": "asc"}
    top = []
    scans = []
    seen = set()
    total = Decimal(0)
    for _ in range(max_pages):
        url = HORIZON + "/accounts?" + urlencode(params)
        try:
            data, headers = fetch_json(url)
            records = data["_embedded"]["records"]
            scans.append({"url": url, "records": len(records), "latest_ledger": headers.get("latest-ledger")})
        except (OSError, ValueError, KeyError) as error:
            scans.append({"url": url, "error": str(error)})
            break
        for account in records:
            address = account["account_id"]
            if address in seen:
                raise ValueError("duplicate account in Horizon traversal")
            seen.add(address)
            for row in account["balances"]:
                if row.get("asset_code") == asset and row.get("asset_issuer") == ISSUER:
                    amount = Decimal(row["balance"])
                    total += amount
                    if amount > 0:
                        top.append((amount, address, row["is_authorized"]))
        if len(records) < params["limit"]:
            break
        params["cursor"] = records[-1]["paging_token"]

    return {
        "asset": params["asset"], "pages": scans, "accounts_read": len(seen),
        "enumeration_finished": "records" in scans[-1] and scans[-1]["records"] < params["limit"],
        "total_of_observed_trust_lines": str(total), "positive_trust_lines_seen": len(top),
        "largest_observed": [{"account": address, "balance": str(amount), "authorized": authorized}
                             for amount, address, authorized in sorted(top, reverse=True)[:10]],
    }


def solana_ustb():
    params = [MINTS["ustb"], {"commitment": "finalized"}]
    attempts = []
    for url in (SOLANA, "https://solana-rpc.publicnode.com", "https://solana.drpc.org",
                "https://solana.api.pocket.network", "https://public-solana-mainnet.rpcnode.dev",
                "https://rpc.nodeflare.app/solana/public", "https://solana.leorpc.com",
                "https://rpc.ankr.com/solana"):
        row = observation(url, "getTokenLargestAccounts", params)
        attempts.append(row)
        if "result" in row:
            break
    return {"largest_attempts": attempts, "supply": observation(SOLANA, "getTokenSupply", params)}


def safe_observations():
    evm = json.loads((ROOT / "evidence/evm-2026-09-30.json").read_text())["chains"]
    calls = {"master_copy": "0xa619486e", "threshold": "0xe75235b8", "owners": "0xa0e67e2b",
             "modules": "0xcc2f8452" + f"{1:064x}{100:064x}"}
    endpoints = {
        "ethereum": ("https://eth.drpc.org", "https://rpc.mevblocker.io"),
        "optimism": ("https://optimism.drpc.org", "https://mainnet.optimism.io",
                     "https://optimism-rpc.publicnode.com"),
    }
    result = {}
    for deployment, safe in SAFES.items():
        chain = deployment.split("/")[1]
        block, successor = (evm[chain][key] for key in ("block", "successor"))
        reads = {}
        for label, selector in calls.items():
            attempts = []
            for url in endpoints[chain]:
                row = observation(url, "eth_call", [{"to": safe, "data": selector}, block["number"]])
                attempts.append(row)
                if "result" not in row:
                    continue
                if label in ("owners", "modules"):
                    try:
                        words = abi_words(row.pop("result"))
                        offset = 1 if label == "owners" else 2
                        if len(words) <= offset or words[0] != 32 * offset:
                            raise ValueError("unexpected dynamic-array offset")
                        count = words[offset]
                        if len(words) != offset + 1 + count:
                            raise ValueError("unexpected array length")
                    except ValueError as error:
                        row["error"] = f"Safe response decode: {error}"
                        continue
                    row[f"{label[:-1]}_count"] = count
                    if label == "modules":
                        row["additional_module_pages"] = words[1] != 1
                break
            reads[label] = attempts
        result[deployment] = {"block": block, "successor": successor, "calls": reads}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--stellar-pages", type=int, choices=range(1, 101), default=40,
                        metavar="1..100")
    args = parser.parse_args()
    started = datetime.now(timezone.utc).isoformat()
    with ThreadPoolExecutor(max_workers=3) as pool:
        safes = pool.submit(safe_observations)
        solana = pool.submit(solana_ustb)
        stellar = pool.submit(stellar_accounts, args.stellar_pages)
        results = {"started_current_reads_utc": started, "pinned_safes": safes.result(),
                   "solana_ustb": solana.result(), "stellar_benji": stellar.result(),
                   "finished_current_reads_utc": datetime.now(timezone.utc).isoformat()}
    args.output.write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
