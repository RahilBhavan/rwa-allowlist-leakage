"""Verify historical holder coverage and prove ranks from unaccounted supply."""
import argparse
from decimal import Decimal
import json
from pathlib import Path
import re

if __package__:
    from .fetch_evm import CUTOFF, TRANSFER, balance, decimals, supply
else:
    from fetch_evm import CUTOFF, TRANSFER, balance, decimals, supply

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-30"
ADDRESS = re.compile(r"0x[0-9a-f]{40}")
ZERO_ADDRESS = "0x" + "0" * 40
USUAL_TREASURY = "0xdd82875f0840aad58a455a70b88eed9f59cec7c7"
USYC_BNB_LARGEST = "0x87433fec6f8d9df13d1e17c4b11364ecd2e93a51"
USDC = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
OUSG_XRPL_ISSUER = "rHuiXXjHLpMP8ZE9sSQU5aADQVWDwv6h5p"
OUSG_XRPL_CURRENCY = "4F55534700000000000000000000000000000000"


def validate_pin(capture):
    block = capture["block"]
    successor = capture["successor"]
    if (
        not int(block["timestamp"], 16) <= CUTOFF < int(successor["timestamp"], 16)
        or successor["parentHash"] != block["hash"]
        or int(successor["number"], 16) != int(block["number"], 16) + 1
    ):
        raise ValueError("invalid month-end block bracket")
    return block["number"]


def pinned_read(capture, name, method, *args):
    row = capture["reads"].get(name)
    if row is None:
        return None
    if row["params"] != [*args, capture["block"]["number"]] or row["method"] != method:
        raise ValueError(f"{name} does not match pinned request")
    if method == "eth_getCode":
        return code_read_type(row)
    return row["result"]


def read_call(capture, name, token, data):
    result = pinned_read(capture, name, "eth_call", {"to": token, "data": data})
    return int(result, 16) if result is not None else None


def rank_balances(supply_raw, balances):
    """An omitted address can hold at most all of the residual."""
    observed = sum(balances.values())
    if min(balances.values(), default=0) < 0 or (supply_raw is not None and observed > supply_raw):
        raise ValueError("observed balances cannot reconcile to supply")
    residual = None if supply_raw is None else supply_raw - observed
    ranked = sorted(balances, key=lambda address: (-balances[address], address))
    rank = 0
    previous = None
    rows = []
    for index, address in enumerate(ranked, start=1):
        amount = balances[address]
        if amount != previous:
            rank = index
        verified = residual is not None and amount > residual
        rows.append((address, rank, rank if verified else None))
        previous = amount
    return residual, rows


def holder_type(code):
    if code is None:
        return "code unknown"
    if code == "0x":
        return "no runtime code"
    if len(code) == 48 and code.startswith("0xef0100"):
        return "delegated EOA"
    return "contract code"


def code_read_type(row):
    if "code_type" not in row:
        return holder_type(row["result"])
    code_type = row["code_type"]
    if code_type not in ("no runtime code", "delegated EOA", "contract code"):
        raise ValueError("invalid runtime code classification")
    return code_type


def audit(capture):
    target = capture["target"]
    if "block" not in capture:
        return {"rows": [], "supply_raw": None, "residual_raw": None, "candidate_count": 0,
                "supply_native": None, "residual_native": None}
    pin = validate_pin(capture)
    token = target["token"]
    supply_raw = read_call(capture, "supply", *supply(token))
    scale = read_call(capture, "decimals", *decimals(token))
    balances = {}
    code_types = {}
    candidates = capture["candidates"]
    if len(candidates) != len(set(candidates)):
        raise ValueError("duplicate candidate")
    unread = []
    for address in candidates:
        if not ADDRESS.fullmatch(address) or address == ZERO_ADDRESS:
            raise ValueError(f"invalid holder {address}")
        raw = read_call(capture, f"balance/{address}", *balance(token, address))
        if raw is None:
            unread.append(address)
        elif raw:
            balances[address] = raw
            code_types[address] = pinned_read(capture, f"code/{address}", "eth_getCode", address)
    def units(amount):
        if amount is None or scale is None:
            return None
        return Decimal(amount) / 10**scale

    residual, rankings = rank_balances(supply_raw, balances)
    return {
        "block": int(pin, 16), "token": token, "supply_raw": supply_raw,
        "supply_native": units(supply_raw), "residual_raw": residual, "residual_native": units(residual),
        "candidate_count": len(candidates), "unread": unread,
        "rows": [{
            "address": address, "raw": balances[address], "native": units(balances[address]),
            "candidate_rank": candidate_rank, "verified_rank": verified_rank,
            "address_type": code_types[address] or holder_type(None),
            "documented_role": target.get("leads", {}).get(address, "unresolved"),
        } for address, candidate_rank, verified_rank in rankings],
    }


def verify_usual(capture, snapshot):
    """Require pin-level custody, collateral eligibility and secondary inventory."""
    validate_pin(capture)
    specs = capture["target"]["probes"]

    def get(name):
        value = pinned_read(capture, name, *specs[name])
        if value is None:
            raise ValueError(f"missing Usual read {name}")
        return value

    usyc = capture["target"]["token"]
    dao = specs["usual_dao_impl"][1]
    usd0 = specs["usd0_impl"][1]
    mapping = specs["usual_usyc_eligible"][1]["to"]
    state_address = lambda label: "0x" + get(label)[-40:]
    if (
        state_address("usual_dao_impl") != "0x0eec861d49f15f585d6bb4301fc4f89bce22af4e"
        or state_address("usd0_impl") != "0xae12f6f805842e6dafe71a6d2b41b28ba5fc821e"
        or state_address("usual_dao_treasury") != USUAL_TREASURY
        or state_address("usual_dao_token_mapping") != mapping
        or state_address("usual_dao_usd0") != usd0
        or state_address("usd0_pool_coin_0") != usd0
        or state_address("usd0_pool_coin_1") != USDC
        or int(get("usual_usyc_eligible"), 16) != 1
        or int(get("usd0_paused"), 16) != 0
    ):
        raise ValueError("Usual custody or USD0 pool identity mismatch")
    expected_allowance = "0xdd62ed3e" + USUAL_TREASURY[2:].zfill(64) + dao[2:].zfill(64)
    expected_eligibility = "0xf84e817c" + usyc[2:].zfill(64)
    if specs["usual_treasury_usyc_allowance"][1] != {"to": usyc, "data": expected_allowance}:
        raise ValueError("unexpected Usual allowance request")
    if specs["usual_usyc_eligible"][1]["data"] != expected_eligibility:
        raise ValueError("unexpected Usual eligibility request")
    row, = [row for row in snapshot["rows"] if row["address"] == USUAL_TREASURY]
    if (
        row["address_type"] != "contract code"
        or int(get("usual_treasury_usyc_allowance"), 16) < row["raw"]
        or not 0 < int(get("usd0_pool_quote"), 16) <= int(get("usd0_pool_inventory"), 16)
        or int(get("usd0_pool_inventory"), 16) > int(get("usd0_supply"), 16)
    ):
        raise ValueError("Usual balance lacks a corroborated USD0 route")
    return {
        "usyc_native": row["native"],
        "usd0_supply": Decimal(int(get("usd0_supply"), 16)).scaleb(-18),
        "pool_usd0_inventory": Decimal(int(get("usd0_pool_inventory"), 16)).scaleb(-18),
        "pool_quote_1_usdc_to_usd0": Decimal(int(get("usd0_pool_quote"), 16)).scaleb(-18),
    }


def load_holders(directory):
    evidence = json.loads((directory / f"holders-{DATE}.json").read_text())
    config = json.loads((directory / "holder-targets.json").read_text())
    if evidence["cutoff"] != CUTOFF or evidence["targets"].keys() != config["targets"].keys():
        raise ValueError("holder capture uses an unexpected snapshot or target set")
    captures = evidence["targets"]
    for name, capture in captures.items():
        if capture["target"] != config["targets"][name]:
            raise ValueError(f"captured target differs from inventory: {name}")
    supplement = json.loads((directory / "round1-supplement.json").read_text())
    for name, probe in supplement["holder_probes"].items():
        capture = captures[name]
        candidates = capture["candidates"]
        for label, row in probe["reads"].items():
            kind, address = label.split("/")
            if kind == "balance" and address not in candidates:
                candidates.append(address)
            if "error" not in row:
                previous = capture["reads"].setdefault(label, row)
                if previous != row:
                    raise ValueError(f"conflicting supplemental holder read for {name}/{label}")
        capture["candidates"] = sorted(candidates)
    return captures, {name: audit(capture) for name, capture in captures.items()}


def verify_bnb_discovery(directory, snapshot):
    evidence = json.loads((directory / "usyc-bnb-receipt-2026-09-25.json").read_text())
    receipt = evidence["transaction_receipt"]["result"]
    tx_hash, = evidence["transaction_receipt"]["params"]
    height = int(receipt["blockNumber"], 16)
    if (
        receipt["transactionHash"] != tx_hash
        or receipt["from"] != USYC_BNB_LARGEST
        or receipt["status"] != "0x1"
        or height >= snapshot["block"]
    ):
        raise ValueError("USYC discovery receipt does not precede the supply pin")
    token = snapshot["token"]
    transfers = [log for log in receipt["logs"]
                 if log["address"] == token and log["topics"][0] == TRANSFER]
    if transfers != evidence["matched_logs"] or not any(
        log["topics"][1][-40:] == USYC_BNB_LARGEST[2:] for log in transfers
    ):
        raise ValueError("USYC discovery receipt does not identify the leading holder")
    before, after = evidence["supply_change"]
    for row, expected in ((before, height - 1), (after, height)):
        if row["method"] != "eth_call" or row["params"] != [
            {"to": token, "data": "0x18160ddd"}, hex(expected),
        ]:
            raise ValueError("USYC discovery supply change does not bracket the receipt")
    burned = sum(int(log["data"], 16) for log in transfers if log["topics"][2][-40:] == ZERO_ADDRESS[2:])
    if not burned or int(before["result"], 16) - int(after["result"], 16) != burned:
        raise ValueError("USYC supply change does not reconcile to the receipt burn")


def audit_xrpl(evidence):
    pin, successor = evidence["ledger"], evidence["successor"]
    if (
        evidence["cutoff"] != CUTOFF
        or successor["index"] != pin["index"] + 1
        or successor["parent"] != pin["hash"]
        or not pin["timestamp"] <= CUTOFF < successor["timestamp"]
    ):
        raise ValueError("invalid XRPL month-end ledger bracket")
    marker = None
    seen = set()
    rows = []
    pages = evidence["pages"]
    if not pages:
        raise ValueError("missing XRPL trust-line pages")
    for i, page in enumerate(pages, start=1):
        request, result = page["params"], page["result"]
        if (
            result["ledger_hash"] != pin["hash"]
            or request["ledger_hash"] != pin["hash"]
            or result["account"] != OUSG_XRPL_ISSUER
            or request["account"] != OUSG_XRPL_ISSUER
            or request.get("marker") != marker
            or not result["validated"]
        ):
            raise ValueError("wrong XRPL issuer, ledger, or page marker")
        marker = result.get("marker")
        if (marker is None) != (i == len(pages)):
            raise ValueError("XRPL pagination is incomplete or has trailing pages")
        for line in result["lines"]:
            if line["currency"] != OUSG_XRPL_CURRENCY:
                continue
            address = line["account"]
            if address in seen:
                raise ValueError("duplicate OUSG trust line")
            seen.add(address)
            amount = -Decimal(line["balance"])
            if amount > 0:
                rows.append({"address": address, "native": amount,
                             "issuer_authorized": line.get("authorized", False),
                             "address_type": "XRPL trust-line account, control unknown"})
    rows.sort(key=lambda row: (-row["native"], row["address"]))
    for index, row in enumerate(rows):
        row["verified_rank"] = (
            rows[index - 1]["verified_rank"] if index and row["native"] == rows[index - 1]["native"]
            else index + 1
        )
    issuer_params = {"account": OUSG_XRPL_ISSUER, "ledger_hash": pin["hash"]}
    for key in ("account_info", "gateway_balances"):
        if evidence[key]["params"] != issuer_params or evidence[key]["result"]["ledger_hash"] != pin["hash"]:
            raise ValueError("XRPL issuer corroboration uses another ledger")
    info = evidence["account_info"]["result"]
    obligations = Decimal(evidence["gateway_balances"]["result"]["obligations"][OUSG_XRPL_CURRENCY])
    outstanding = sum(row["native"] for row in rows)
    if abs(obligations - outstanding) > Decimal("0.00000001"):
        raise ValueError("XRPL trust-line balances and gateway obligations diverge")
    return {
        "ledger": pin["index"], "issuer": OUSG_XRPL_ISSUER, "currency": OUSG_XRPL_CURRENCY,
        "trust_lines": len(seen), "outstanding_native": outstanding,
        "issuer_domain": bytes.fromhex(info["account_data"]["Domain"]).decode(),
        "issuer_requires_authorization": info["account_flags"]["requireAuthorization"],
        "rows": rows,
    }


def add_holder_classes(directory, reports):
    """Report mutually exclusive location classes against each deployment supply."""
    avax = json.loads((directory / "buidl-avalanche-signer.json").read_text())
    signer = "0x76a38a6ab201b1d6fa8617352538a7260df65377"
    avax_report = reports["buidl/avalanche"]
    tx = avax["result"]
    signature_present = tx.get("signature_present")
    if "signature_present" not in tx:
        signature_present = bool(int(tx["r"], 16) and int(tx["s"], 16))
    if (
        avax["method"] != "eth_getTransactionByHash" or avax["params"] != [tx["hash"]]
        or tx["from"] != signer or tx["to"] != avax_report["token"]
        or int(tx["blockNumber"], 16) >= avax_report["block"]
        or signature_present is not True
    ):
        raise ValueError("Avalanche holder signer evidence does not precede the pin")
    verify_bnb_discovery(directory, reports["usyc/bsc"])
    anchorage = "0x2004f7f7b600d962170d7f28114cc123c5e98451"
    reserve = {("buidl/avalanche", anchorage), ("buidl/bsc", anchorage)}
    operations = {
        ("usyc/ethereum", "0x5c73e1cfdd85b7f1d608f7f7736fc8c653513b7a"),
    }
    signers = {("buidl/avalanche", signer), ("usyc/bsc", USYC_BNB_LARGEST)}
    for deployment, report in reports.items():
        if deployment == "ousg/xrpl":
            supply_native, residual = report["outstanding_native"], Decimal(0)
        else:
            supply_native, residual = report["supply_native"], report["residual_native"]
        totals = dict.fromkeys(("issuer_ops", "reserve_custody", "contract", "eoa", "no_code", "unknown_control", "unobserved"),
                               Decimal(0))
        for row in report["rows"]:
            key = deployment, row["address"]
            kind = row["address_type"]
            if key in reserve:
                location = "reserve_custody"
                row["documented_role"] = "Anchorage USDtb reserve custody"
            elif key in operations:
                location = "issuer_ops"
            elif kind == "delegated EOA" or (kind == "no runtime code" and key in signers):
                location = "eoa"
            else:
                location = {"contract code": "contract", "no runtime code": "no_code"}.get(kind, "unknown_control")
            row["holder_class"] = location
            totals[location] += row["native"]
        totals["unobserved"] = residual
        report["holder_class_native"] = totals
        report["holder_class_share_of_supply"] = {
            key: amount / supply_native if amount is not None and supply_native else None
            for key, amount in totals.items()
        }



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=ROOT / "evidence")
    args = parser.parse_args()
    _, reports = load_holders(args.evidence)
    xrpl = json.loads((args.evidence / f"ousg-xrpl-{DATE}.json").read_text())
    reports["ousg/xrpl"] = audit_xrpl(xrpl)
    add_holder_classes(args.evidence, reports)
    print(json.dumps(reports, indent=2, default=str))


if __name__ == "__main__":
    main()
