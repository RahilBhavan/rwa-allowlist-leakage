"""Compute the September 2026 five-fund cutoff from offline evidence."""
import argparse
from dataclasses import dataclass, replace
from decimal import Decimal as D
import json
from pathlib import Path

if __package__:
    from .fetch_evm import ANCHORAGE, CHAINS, CUTOFF, FRAX_BUIDL, FRAX_USTB, FRXUSD, USDTB, balance
    from .holder_audit import DATE, USDC, pinned_read, validate_pin
    from .review_evidence import abi_words
else:
    from fetch_evm import ANCHORAGE, CHAINS, CUTOFF, FRAX_BUIDL, FRAX_USTB, FRXUSD, USDTB, balance
    from holder_audit import DATE, USDC, pinned_read, validate_pin
    from review_evidence import abi_words

ROOT = Path(__file__).resolve().parents[1]
THRESHOLD = D("0.05")
ZERO = D(0)
DUST_FEE_PIPS = 100_000  # 10% in parts per million
DUST_MIN_QUOTED_USD = D(100)


@dataclass(frozen=True)
class Fund:
    ticker: str
    supply_floor_usd: D
    supply_ceiling_usd: D


@dataclass(frozen=True)
class Position:
    fund: str
    chain: str
    holder: str
    kind: str
    usd: D
    native: D
    strict_custody_exclusion: bool = False
    attested_only: bool = False
    dust_only: bool = False


def calculate(funds, positions, include_reserve_custody):
    funds_by_ticker = {fund.ticker: fund for fund in funds}
    if len(funds_by_ticker) != len(funds):
        raise ValueError("duplicate fund")
    if any(not ZERO < row.supply_floor_usd <= row.supply_ceiling_usd for row in funds):
        raise ValueError("invalid denominator bounds")

    seen = set()
    for row in positions:
        key = row.fund, row.chain, row.holder.lower() if row.holder.startswith("0x") else row.holder
        if key in seen:
            raise ValueError(f"duplicate underlying position: {key}")
        seen.add(key)
        if row.fund not in funds_by_ticker or row.usd <= ZERO:
            raise ValueError(f"invalid position: {key}")
        if row.kind not in {"wrapper_contract", "reserve_custody", "verified_non_wrapper"}:
            raise ValueError(f"unknown position kind: {row.kind}")

    results = []
    for fund in funds:
        rows = [row for row in positions if row.fund == fund.ticker]
        custody = sum((row.usd for row in rows if row.kind == "reserve_custody"), ZERO)
        contracts = sum((row.usd for row in rows if row.kind == "wrapper_contract"), ZERO)
        other_exclusions = sum((row.usd for row in rows if row.kind == "verified_non_wrapper"), ZERO)
        if custody + contracts + other_exclusions > fund.supply_ceiling_usd:
            raise ValueError(f"classified balances exceed denominator ceiling for {fund.ticker}")
        counted = contracts + custody if include_reserve_custody else contracts
        attested = sum((row.usd for row in rows if row.attested_only), ZERO) if include_reserve_custody else ZERO
        corroborated_custody = sum((row.usd for row in rows
                                    if row.kind == "reserve_custody" and row.strict_custody_exclusion), ZERO)
        excluded = ZERO if include_reserve_custody else corroborated_custody + other_exclusions
        floor = max(fund.supply_floor_usd, custody + contracts + other_exclusions)
        results.append({"fund": fund.ticker, "denominator_floor_usd": floor,
                        "denominator_slack_usd": fund.supply_ceiling_usd - floor,
                        "denominator_ceiling_usd": fund.supply_ceiling_usd,
                        "verified_usd": counted, "excluded_usd": excluded,
                        "onchain_backing_usd": counted - attested, "attested_only_backing_usd": attested,
                        "unclassified_at_ceiling_usd": fund.supply_ceiling_usd - counted - excluded,
                        "share_lower": counted / fund.supply_ceiling_usd,
                        "share_upper": (fund.supply_ceiling_usd - excluded) / fund.supply_ceiling_usd})

    ceiling = sum(row["denominator_ceiling_usd"] for row in results)
    floor = sum(row["denominator_floor_usd"] for row in results)
    verified = sum(row["verified_usd"] for row in results)
    excluded = sum(row["excluded_usd"] for row in results)
    lower = verified / ceiling
    upper = (ceiling - excluded) / ceiling
    if verified >= THRESHOLD * ceiling:
        verdict = "continue"
    elif ceiling - excluded < THRESHOLD * ceiling:
        verdict = "below_cutoff"
    else:
        verdict = "inconclusive"
    return {
        "funds": results,
        "denominator_floor_usd": floor, "denominator_ceiling_usd": ceiling,
        "verified_usd": verified, "excluded_usd": excluded,
        "onchain_backing_usd": sum(row["onchain_backing_usd"] for row in results),
        "attested_only_backing_usd": sum(row["attested_only_backing_usd"] for row in results),
        "unclassified_at_ceiling_usd": ceiling - verified - excluded,
        "denominator_slack_usd": ceiling - floor,
        "unclassified_at_floor_usd": floor - verified - excluded,
        "cutoff_usd_at_denominator_ceiling": THRESHOLD * ceiling,
        "shortfall_usd_to_cutoff": max(ZERO, THRESHOLD * ceiling - verified),
        "share_lower": lower, "share_upper": upper, "verdict": verdict,
    }


def load_evidence(directory):
    def load(name):
        return json.loads((directory / name).read_text(), parse_float=D)

    facts = load(f"primary-transcriptions-{DATE}.json")
    ustb_history = load(f"superstate-ustb-{DATE}.json")["historical_data"]
    ondo_history = load(f"ondo-ousg-{DATE}.json")
    ondo, = [row for row in ondo_history if row["timestamp"] == f"{DATE}T00:00:00Z"]
    rpc = load(f"evm-{DATE}.json")
    chains = rpc["chains"]
    if facts["date"] != DATE or rpc["cutoff"] != CUTOFF:
        raise ValueError("mixed snapshot dates")
    for capture in chains.values():
        validate_pin(capture)

    def result(chain, label):
        target, *calldata = CHAINS[chain][2][label]
        method, args = ("eth_call", [{"to": target, "data": calldata[0]}]) if calldata else (
            "eth_getCode", [target])
        value = pinned_read(chains[chain], label, method, *args)
        if value is None:
            raise ValueError(f"missing pinned read {chain}/{label}")
        return value

    def units(chain, label, scale):
        return D(int(result(chain, label), 16)).scaleb(-int(result(chain, scale), 16))

    def deposit(fund, label, scale, nav, dest):
        native = units("ethereum", label, scale)
        code_type = result("ethereum", f"{label}_code")
        if code_type not in ("contract code", "delegated EOA"):
            raise ValueError(f"missing verified contract at {dest}")
        return Position(fund, "ethereum", dest, "wrapper_contract", native * nav, native)

    ustb_nav, = [D(row["value"]) for row in ustb_history["nav"] if row["date"] == DATE]
    ustb_aum, = [D(row["value"]) for row in ustb_history["aum"] if row["date"] == DATE]
    buidl_nav = D(facts["buidl_nav_usd"])
    if buidl_nav <= ZERO or ustb_nav <= ZERO:
        raise ValueError("invalid fund NAV")
    reported_ethereum_usdtb = D(facts["anchorage_ethereum_usdtb_redeemable"])
    ethereum_usdtb = units("ethereum", "usdtb", "usdtb_decimals")
    def market(token, prefix, balance_read, output_index, expected_coins):
        pool, = load(f"curve-{token}-pool.json")
        if tuple(coin["address"].lower() for coin in pool["coins"]) != expected_coins:
            raise ValueError(f"{token} market assets mismatch")
        for index, coin in enumerate(pool["coins"]):
            label = f"{prefix}_coin_{index}"
            call = chains["ethereum"]["reads"][label]["params"][0]
            if (
                call["to"].lower() != pool["address"].lower()
                or result("ethereum", label)[-40:].lower() != coin["address"][2:].lower()
            ):
                raise ValueError(f"{token} market assets mismatch")
        native_decimals = int(pool["coins"][output_index]["decimals"])
        inventory = D(int(result("ethereum", balance_read), 16)).scaleb(-native_decimals)
        quote = D(int(result("ethereum", f"{prefix}_quote"), 16)).scaleb(-native_decimals)
        if not ZERO < quote <= inventory:
            raise ValueError(f"{token} secondary route has no verified inventory or quote")
        return inventory, quote

    pool_usdtb, pool_quote = market("usdtb", "curve", "curve_usdtb", 1, (USDC, USDTB))
    pool_frxusd, frax_quote = market("frxusd", "curve_frxusd", "curve_frxusd_balance", 0, (
        FRXUSD, "0xf939e0a03fb07f59a73314e73794be0e57ac1b4e"))
    if abs(ethereum_usdtb - reported_ethereum_usdtb) > D(1) or pool_usdtb > ethereum_usdtb:
        raise ValueError("USDtb token supply does not corroborate attestation")

    reserve = [
        Position("BUIDL", row["chain"], row["custody_address"], "reserve_custody",
                 D(row["buidl_usd"]), D(row["buidl_usd"]) / buidl_nav)
        for row in facts["anchorage_reserve_legs"]
    ]
    reserve_total = sum(row.usd for row in reserve)
    if (sorted(row.chain for row in reserve) != ["aptos", "avalanche", "bsc", "solana"]
            or any(row.usd <= 1 for row in reserve)
            or reserve_total != D(facts["anchorage_total_buidl_usd"])):
        raise ValueError("attested reserve legs do not reconcile")

    buidl_frax = deposit("BUIDL", "frax_buidl", "buidl_decimals", buidl_nav, FRAX_BUIDL)
    ustb_frax = deposit("USTB", "frax_ustb", "ustb_decimals", ustb_nav, FRAX_USTB)

    # The platform and USYC totals are rounded publisher disclosures. The
    # transcriptions include a full displayed $0.1B increment as headroom.
    # Avoid treating a sum of bridge-connected deployments as a supply floor.
    buidl_total = D(facts["securitize_platform_value_display_usd"])
    buidl_headroom = D(facts["securitize_rounding_allowance_usd"])
    buidl_visible = {}
    for chain, data in chains.items():
        for label in ("buidl", "buidl_i"):
            if label in data["reads"] and f"{label}_decimals" in data["reads"]:
                buidl_visible[f"{chain}/{label}"] = units(chain, label, f"{label}_decimals")

    usyc_total = D(facts["circle_usyc_display_usd"])
    usyc_headroom = D(facts["circle_rounding_allowance_usd"])
    round_id, answer, started_at, usyc_oracle_updated, answered_in_round = abi_words(result("ethereum", "usyc_nav"))
    usyc_nav = D(answer).scaleb(-int(result("ethereum", "usyc_nav_decimals"), 16))
    if (not 0 < answer < 2**255 or not 0 < started_at <= usyc_oracle_updated
            <= int(chains["ethereum"]["block"]["timestamp"], 16)
            or not 0 < round_id <= answered_in_round):
        raise ValueError("invalid USYC oracle round")
    benji_value = D(facts["franklin_benji_net_assets_usd"])
    filing = load(f"franklin-filing-readback-{DATE}.json")
    if (filing["report_period"] != DATE or filing["series"] != "S000067043"
            or filing["class"] != "C000215714"
            or filing["item_8_share_classes"] != 1
            or D(filing["item_b4_net_assets_usd"]) != benji_value
            or D(filing["item_b5_shares"]) != D(facts["franklin_benji_shares"])):
        raise ValueError("Franklin filing readback does not match denominator transcription")
    funds = [
        Fund("BUIDL", max(reserve_total + buidl_frax.usd, max(buidl_visible.values()) * buidl_nav),
             buidl_total + buidl_headroom),
        Fund("USTB", units("ethereum", "ustb", "ustb_decimals") * ustb_nav, ustb_aum),
        Fund("USYC", usyc_total - usyc_headroom, usyc_total + usyc_headroom),
        Fund("BENJI", benji_value, benji_value),
    ]
    positions = [*reserve, buidl_frax, ustb_frax]

    observations = {
        "buidl_supply_reads_native": buidl_visible,
        "ustb_ethereum_native": units("ethereum", "ustb", "ustb_decimals"),
        "ustb_nav_usd": ustb_nav,
        "usyc_ethereum_native": units("ethereum", "usyc", "usyc_decimals"),
        "usyc_bsc_native": units("bsc", "usyc", "usyc_decimals"),
        "usyc_nav_usd": usyc_nav,
        "usyc_oracle_updated_at_unix": usyc_oracle_updated,
        "ousg_daily_mark_usd": ondo["asset"]["tvlUsd"]["total"],
        "ousg_price_usd": ondo["asset"]["priceUsd"],
        "benji_shares": D(facts["franklin_benji_shares"]),
        "ethereum_usdtb_native": ethereum_usdtb,
        "curve_usdtb_balance": pool_usdtb,
        "curve_quote_1_usdc_to_usdtb": pool_quote,
        "curve_frxusd_balance": pool_frxusd,
        "curve_quote_1_crvusd_to_frxusd": frax_quote,
        "usual_collateral_treasury_usyc": units("ethereum", "usual_treasury_usyc", "usyc_decimals"),
        "usual_collateral_treasury_usd_at_nav": units("ethereum", "usual_treasury_usyc", "usyc_decimals") * usyc_nav,
        "usual_dao_collateral_usyc": units("ethereum", "usual_dao_usyc", "usyc_decimals"),
        "anchorage_evm": {
            chain: {"buidl_native": units(chain, "anchorage_buidl", "buidl_decimals"),
                    "code_present": result(chain, "anchorage_code") in ("contract code", "delegated EOA")}
            for chain in ("bsc", "avalanche")
        },
    }
    for row in reserve:
        corroboration = observations["anchorage_evm"].get(row.chain)
        if corroboration and (row.holder.lower() != ANCHORAGE.lower()
                              or abs(corroboration["buidl_native"] * buidl_nav - row.usd) > D(1)):
            raise ValueError(f"{row.chain} attestation and RPC diverge outside rounding")
    return funds, positions, observations


def ousg_model(marks, adjacent, ethereum_native, xrpl_native):
    if sorted(row["timestamp"] for row in marks) != [
        f"{date}T00:00:00Z" for date in ("2026-09-29", "2026-09-30", "2026-10-01")
    ] or sorted(row["timestamp"] for row in adjacent) != [
        f"2026-10-0{day}T00:00:00Z" for day in (2, 3, 4)
    ]:
        raise ValueError("missing or duplicate OUSG daily marks")
    # Ethereum canonical ERC-20 and XRPL direct issuer obligations are distinct
    # by the native-issuance assumption. Wrappers such as rOUSG are omitted.
    prices = [row["asset"]["priceUsd"] for row in marks + adjacent]
    values = [row["asset"]["tvlUsd"]["total"] for row in marks + adjacent]
    low, high = min(prices), max(prices)
    if low <= ZERO or min(values) <= ZERO or min(ethereum_native, xrpl_native) <= ZERO:
        raise ValueError("invalid OUSG native supply, TVL or NAV")
    units = ethereum_native + xrpl_native
    basis = max(units * high, max(values))
    return {
        "pinned_native_units": units, "direct_exclusion_nav_usd": low, "high_nav_usd": high,
        "pinned_floor_usd": units * low, "pinned_high_nav_usd": units * high,
        "largest_single_chain_floor_usd": max(ethereum_native, xrpl_native) * low,
        "maximum_observed_mark_usd": max(values), "ceiling_basis_usd": basis,
        "time_allowance_usd": D(10_000_000), "unknown_chain_allowance_usd": D(25_000_000),
        "ceiling_usd": basis + D(10_000_000) + D(25_000_000),
    }


def eligible_no_code(row):
    return row["address_type"] == "no runtime code"


def gated_receipt(capture, report, address, label, selector):
    result = pinned_read(capture, label, "eth_call", {"to": address, "data": selector})
    if result is None or result[-40:] != report["token"][2:]:
        raise ValueError("gated receipt does not identify its underlying at the pin")
    row, = [row for row in report["rows"] if row["address"] == address]
    if row["address_type"] != "contract code":
        raise ValueError("gated receipt code missing")
    return row["native"]


def load_revised_evidence(directory):
    if __package__:
        from .review_evidence import MARKET_CONTROLS, MIDAS, STBL, nest_routes, observations as review_observations
        from .holder_audit import (
            USUAL_TREASURY, USYC_BNB_LARGEST, audit_xrpl, load_holders, verify_bnb_discovery, verify_usual,
        )
    else:
        from review_evidence import MARKET_CONTROLS, MIDAS, STBL, nest_routes, observations as review_observations
        from holder_audit import (
            USUAL_TREASURY, USYC_BNB_LARGEST, audit_xrpl, load_holders, verify_bnb_discovery, verify_usual,
        )

    funds, positions, observations = load_evidence(directory)
    captures, reports = load_holders(directory)
    observations.update(review_observations(directory, captures["ustb/ethereum"]))
    xrpl = audit_xrpl(json.loads((directory / f"ousg-xrpl-{DATE}.json").read_text()))
    ondo_marks = json.loads((directory / f"ondo-ousg-{DATE}.json").read_text(), parse_float=D)
    adjacent = json.loads((directory / "ondo-ousg-adjacent-2026-10.json").read_text(), parse_float=D)
    model = ousg_model(ondo_marks, adjacent, reports["ousg/ethereum"]["supply_native"], xrpl["outstanding_native"])
    observations["ousg_denominator"] = model
    funds.insert(3, Fund("OUSG", model["pinned_floor_usd"], model["ceiling_usd"]))
    usual = verify_usual(captures["usyc/ethereum"], reports["usyc/ethereum"])
    observations["usual_usd0_verified"] = usual
    nav = observations["usyc_nav_usd"]
    usual_native = usual["usyc_native"]
    if usual_native != observations["usual_collateral_treasury_usyc"]:
        raise ValueError("Usual balance differs between pinned captures")

    revised = []
    frax_candidates = []
    for row in positions:
        if row.kind == "wrapper_contract":
            fund_token = reports[f"{row.fund.lower()}/ethereum"]["token"]
            minted = observations["frax_pinned"][fund_token]["minted_frxusd"]
            if minted:
                # The counter is a route-local liability cap at this pin.
                revised.append(replace(row, usd=min(row.usd, minted),
                                       native=min(row.native, row.native * minted / row.usd)))
            else:
                frax_candidates.append(row)
            continue
        evm = observations["anchorage_evm"].get(row.chain)
        if evm is None:
            # Schedule II displays whole dollars. Allow a full increment.
            revised.append(Position(row.fund, row.chain, row.holder, row.kind,
                                    row.usd - D(1), row.native - D(1), attested_only=True))
        else:
            exact = evm["buidl_native"] * row.usd / row.native
            revised.append(Position(row.fund, row.chain, row.holder, row.kind,
                                    exact, evm["buidl_native"], not evm["code_present"]))

    bnb = reports["usyc/bsc"]
    verify_bnb_discovery(directory, bnb)
    largest, = [row for row in bnb["rows"] if row["address"] == USYC_BNB_LARGEST]
    if largest["verified_rank"] != 1 or largest["address_type"] != "no runtime code":
        raise ValueError("BNB Chain USYC exclusion has no pinned rank or code corroboration")
    revised.extend([
        Position("USYC", "ethereum", USUAL_TREASURY, "wrapper_contract", usual_native * nav, usual_native),
        Position("USYC", "bsc", USYC_BNB_LARGEST, "verified_non_wrapper",
                 largest["native"] * nav, largest["native"]),
    ])
    observations["usyc_bsc_top_holder"] = largest

    observations["frax_unattributed_reserves"] = [vars(row) for row in frax_candidates]
    ousg_exclusion_nav = model["direct_exclusion_nav_usd"]
    midas, = [row for row in reports["ustb/ethereum"]["rows"] if row["address"] == MIDAS]
    stbl, = [row for row in reports["ousg/ethereum"]["rows"] if row["address"] == STBL]
    if any(row["address_type"] != "contract code" for row in (midas, stbl)):
        raise ValueError("qualifying vault runtime code missing")
    midas_usd = midas["native"] * observations["ustb_nav_usd"]
    mtbill = observations["midas_mtbill"]
    if not 0 < midas_usd <= mtbill["ethereum_mtbill_supply"] * mtbill["mtbill_nav"]:
        raise ValueError("mTBILL Ethereum NAV and supply do not support the vault allocation")
    mtbill["quoted_output_usd"] = mtbill["quote_mtbill"] * mtbill["mtbill_nav"]
    dust_only = (mtbill["pool_fee_pips"] >= DUST_FEE_PIPS
                 or mtbill["quoted_output_usd"] < DUST_MIN_QUOTED_USD)
    usst = observations["stbl_usst"]
    stbl_native = min(stbl["native"], usst["net_deposits_ousg"],
                      usst["recorded_net_stable_value_usd"] / model["high_nav_usd"],
                      usst["ethereum_usst"] / model["high_nav_usd"])
    revised.extend([
        Position("USTB", "ethereum", MIDAS, "wrapper_contract", midas_usd, midas["native"], dust_only=dust_only),
        Position("OUSG", "ethereum", STBL, "wrapper_contract", stbl_native * ousg_exclusion_nav, stbl_native),
    ])
    plume = json.loads((directory / MARKET_CONTROLS).read_text())["chains"]["plume"]
    nest = nest_routes(plume, captures["ustb/plume"])
    observations["nest_pinned"] = nest
    for name, route in nest.items():
        share = route["share"]
        row, = [row for row in reports["ustb/plume"]["rows"] if row["address"] == share]
        native = row["native"]
        usd = native * observations["ustb_nav_usd"]
        if row["address_type"] != "contract code" or not 0 < usd <= route["share_supply"] / route["quotes"][1]["output"]:
            raise ValueError(f"Nest share supply does not support the observed USTB allocation: {name}")
        dust_only = (max(quote["fee_pips"] for quote in route["quotes"].values()) >= DUST_FEE_PIPS
                     or route["quoted_output_at_small_quote_usd"] < DUST_MIN_QUOTED_USD)
        revised.append(Position("USTB", "plume", share, "wrapper_contract", usd, native, dust_only=dust_only))
    benji_nav = next(row.supply_floor_usd for row in funds if row.ticker == "BENJI") / observations["benji_shares"]
    exclusion_mark = {
        "buidl/avalanche": D(1),
        "ustb/ethereum": observations["ustb_nav_usd"],
        "ousg/ethereum": ousg_exclusion_nav,
        "benji/ethereum": benji_nav,
    }
    # Limit anonymous no-code exclusions to a single corroborated deployment
    # per fund. Anchorage's BNB reserve is separately itemized and represents a
    # distinct native share class. Non-EVM custody remains unresolved here.
    already_classified = {(row.fund, row.chain, row.holder.lower()) for row in revised}
    exclusion_reasons = {"no_code": [], "gated_receipt": []}
    for deployment, price in exclusion_mark.items():
        kind, chain = deployment.split("/")
        fund = kind.upper()
        for row in reports[deployment]["rows"]:
            address = row["address"]
            if not eligible_no_code(row) or (fund, chain, address) in already_classified:
                continue
            native = row["native"]
            revised.append(Position(fund, chain, address, "verified_non_wrapper", native * price, native))
            exclusion_reasons["no_code"].append({"deployment": deployment, "address": address})

    exclusion_mark["usyc/ethereum"] = nav
    # These receipts are gated or non-transferable under their protocol rules.
    # The pool's stablecoin lenders can still carry indirect credit exposure.
    gated_receipts = [
        ("ustb/ethereum", "0x4e58a2e433a739726134c83d2f07b2562e8dfdb3",
         "horizon_underlying", "0xb16a19de"),
        ("usyc/ethereum", "0xc167932ac4eec2b65844ef00d31b4550250536a5",
         "horizon_underlying", "0xb16a19de"),
        ("ousg/ethereum", "0x1dd7950c266fb1be96180a8fdb0591f70200e018",
         "flux_underlying", "0x6f307dc3"),
    ]
    for deployment, address, label, selector in gated_receipts:
        fund, chain = deployment.split("/")
        native = gated_receipt(captures[deployment], reports[deployment], address, label, selector)
        revised.append(Position(fund.upper(), chain, address, "verified_non_wrapper",
                                native * exclusion_mark[deployment], native))
        exclusion_reasons["gated_receipt"].append({"deployment": deployment, "address": address})
    observations["additional_strict_exclusions"] = exclusion_reasons
    supplement = json.loads((directory / "round1-supplement.json").read_text())
    observations["buidl_deployment_scenario"] = buidl_deployment_model(supplement, captures, reports, positions)
    small_marks = {"buidl": D(1), "ustb": observations["ustb_nav_usd"], "benji": benji_nav}
    observations["small_deployments_supply_usd"] = {
        name: reports[name]["supply_native"] * small_marks[name.split("/")[0]]
        for name in supplement["holder_probes"]
    }
    return funds, revised, observations


def buidl_deployment_model(capture, captures, reports, positions):
    solana = capture["solana"]["buidl"]["supply"]["result"]["value"]
    aptos = capture["aptos"]
    recent = {
        "solana": D(solana["amount"]).scaleb(-solana["decimals"]),
        "aptos": D(aptos["supply"]["result"]["value"][0]["vec"][0]).scaleb(
            -aptos["metadata"]["result"]["value"]["decimals"]),
    }
    # Neither a later point nor a custody balance proves September chain supply.
    custody = {row.chain: row for row in positions if row.kind == "reserve_custody"}
    reported = {chain: custody[chain].native for chain in recent}
    allowances = {chain: max(current, reported[chain]) for chain, current in recent.items()}
    nav = custody["solana"].usd / custody["solana"].native
    pinned = {name: report["supply_native"] for name, report in reports.items()
              if name.startswith(("buidl/", "buidl_i/"))}
    evm_sum = sum(pinned.values())
    bridge_balances = {}
    for name, observation in capture["issuer_bridge"]["deployments"].items():
        token, calldata = balance(reports[name]["token"], observation["address"])
        bridge = {"block": captures[name]["block"], "reads": {"balance": observation["balance"]}}
        balance_hex = pinned_read(bridge, "balance", "eth_call", {"to": token, "data": calldata})
        bridge_balances[name] = int(balance_hex, 16)
        if bridge_balances[name] != 0:
            raise ValueError(f"nonzero issuer bridge balance at {name}; deployment scenario requires review")
    # A modeled ceiling only if the included deployments and allowances cover the pin.
    return {"pinned_evm_native": pinned, "pinned_evm_sum_native": evm_sum,
            "recent_native": recent, "reported_custody_native": reported,
            "bridge_balances_raw": bridge_balances, "non_evm_allowance_native": allowances,
            "ceiling_usd": (evm_sum + sum(allowances.values())) * nav}



def sensitivity(funds, positions, observed):
    model = observed["ousg_denominator"]
    scenarios = {
        "frax_documentary_reserve_attribution": (
            funds, [*positions, *(Position(**row) for row in observed["frax_unattributed_reserves"])],
        ),
        "without_dust_only_routes": (funds, [row for row in positions if not row.dust_only]),
        "without_solana_aptos_attestation": (
            funds, [row for row in positions if not (
                row.kind == "reserve_custody" and row.chain in {"solana", "aptos"})],
        ),
    }
    buidl_ceiling = observed["buidl_deployment_scenario"]["ceiling_usd"]
    buidl_funds = [replace(fund, supply_ceiling_usd=buidl_ceiling) if fund.ticker == "BUIDL" else fund
                   for fund in funds]
    scenarios["buidl_deployment_ceiling"] = (buidl_funds, positions)
    scenarios["buidl_deployment_ceiling_without_dust"] = (
        buidl_funds, [row for row in positions if not row.dust_only])
    for label, ceiling in (
        ("ousg_pinned_high_or_published_max", model["ceiling_basis_usd"]),
        ("ousg_double_allowances", model["ceiling_basis_usd"] +
         2 * (model["time_allowance_usd"] + model["unknown_chain_allowance_usd"])),
        ("ousg_double_modeled_ceiling", 2 * model["ceiling_usd"]),
    ):
        scenarios[label] = ([replace(fund, supply_ceiling_usd=ceiling) if fund.ticker == "OUSG" else fund
                             for fund in funds], positions)
    outcomes = {}
    for label, (scenario_funds, rows) in scenarios.items():
        direct = calculate(scenario_funds, rows, include_reserve_custody=False)
        broad = calculate(scenario_funds, rows, include_reserve_custody=True)
        outcomes[label] = {
            "direct": {key: direct[key] for key in ("share_lower", "share_upper")},
            "custody_inclusive_lower": broad["share_lower"],
            "denominator_ceiling_usd": direct["denominator_ceiling_usd"],
            "direct_backing_usd": direct["verified_usd"],
            "direct_shortfall_usd_to_cutoff": direct["shortfall_usd_to_cutoff"],
            "custody_inclusive_backing_usd": broad["verified_usd"],
        }
    return outcomes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=ROOT / "evidence")
    args = parser.parse_args()
    funds, positions, observations = load_revised_evidence(args.evidence)
    print(json.dumps({
        "date": DATE, "threshold": THRESHOLD, "observations": observations,
        "positions": [vars(row) for row in positions],
        "sensitivity": sensitivity(funds, positions, observations),
        "economic_exposure": calculate(funds, positions, include_reserve_custody=True),
        "direct_contract_holdings": calculate(funds, positions, include_reserve_custody=False),
    }, indent=2, default=str))


if __name__ == "__main__":
    main()
