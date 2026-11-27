"""Check the historical reserve, market and role reads added in the repair."""
from decimal import Decimal as D
import json

if __package__:
    from .fetch_evm import FRAX_BUIDL, FRAX_USTB, FRXUSD, USTB, BUIDL, balance, word
    from .holder_audit import USDC, pinned_read, validate_pin
else:
    from fetch_evm import FRAX_BUIDL, FRAX_USTB, FRXUSD, USTB, BUIDL, balance, word
    from holder_audit import USDC, pinned_read, validate_pin

MIDAS = "0x569d7dccbf6923350521ecbc28a555a500c4f0ec"
MTBILL = "0xdd629e5241cbc5919847783e6c96b2de4754e438"
STBL = "0x64bef4478942d8fd62be281707076442aa2d055e"
USST = "0xf9d82660828d8f5d121b14a9dc9c677d91f60065"
OUSG = "0x1b19c19393e2d034d8ff31ff34c81252fcbbee92"
STBL_POOL = "0x2877ece562057ee8b0a711bffa10987c3d6398e7"
POOL_MANAGER = "0x000000000004444c5dc75cb358380d2e3de08a90"
MTBILL_POOL_ID = "0x3852f242aca476f28fd5e8cf6c59347c1f92a51d5cb17232efa9db3fc7c2fd2e"
TEST_RECIPIENT = "0x000000000000000000000000000000000000dead"
IMPLEMENTATION_SLOT = "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
ADMIN_SLOT = "0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103"


def abi_words(value):
    if not value or not value.startswith("0x") or (len(value) - 2) % 64:
        raise ValueError("expected ABI words")
    return [int(value[i:i + 64], 16) for i in range(2, len(value), 64)]


def addr(value):
    return "0x" + value[-40:]


def observations(directory, ethereum):
    capture = json.loads((directory / "review-ethereum-2026-09-30.json").read_text())
    validate_pin(capture)
    if any(capture[key] != ethereum[key] for key in ("block", "successor")):
        raise ValueError("review evidence uses a different Ethereum pin")

    def get(label, method, *args):
        value = pinned_read(capture, label, method, *args)
        if value is None:
            raise ValueError(f"missing review evidence: {label}")
        return value

    def call(label, target, data, sender=None):
        request = {"to": target, "data": data}
        if sender is not None:
            request["from"] = sender
        return get(label, "eth_call", request)

    def storage(label, target, slot=IMPLEMENTATION_SLOT):
        return addr(get(label, "eth_getStorageAt", target, slot))

    frax = {}
    for label, reserve, fund in (("frax/buidl", FRAX_BUIDL, BUIDL), ("frax/ustb", FRAX_USTB, USTB)):
        frxusd = addr(call(f"{label}/frxUSD()", reserve, "0x3b1c4f4a"))
        token = addr(call(f"{label}/custodianTkn()", reserve, "0x32d361df"))
        if frxusd != FRXUSD or token != fund:
            raise ValueError("Frax custodian asset link mismatch")
        frax[fund] = {
            "frxusd": frxusd, "custodian_token": token,
            "implementation": storage(f"{label}/implementation", reserve),
            "minted_frxusd": D(int(call(f"{label}/frxUSDMinted()", reserve, "0xce16e3b6"), 16)).scaleb(-18),
        }

    admin = storage("midas/proxy_admin", MIDAS, ADMIN_SLOT)
    helper = addr(call("midas/ustbRedemption()", MIDAS, "0xfabe60dc"))
    access = addr(call("midas/accessControl()", MIDAS, "0x13007d55"))
    burn_role = call("mtbill/M_TBILL_BURN_OPERATOR_ROLE()", MTBILL, "0x60348156")
    if (
        storage("midas/implementation", MIDAS) != "0x489a797714708cf088d158714a376d8ff740d701"
        or storage("mtbill/implementation", MTBILL) != "0xd4998cc1ba435298c521f250b81856b1f25c8455"
        or addr(call("midas/mToken()", MIDAS, "0xc3b6f939")) != MTBILL
        or addr(call("midas_redemption/SUPERSTATE_TOKEN()", helper, "0x11e2e8f7")) != USTB
        or addr(call("midas_redemption/USDC()", helper, "0x89a30271")) != USDC
        or addr(call("mtbill/accessControl()", MTBILL, "0x13007d55")) != access
        or int(call("midas_role/vault_burn", access, "0x91d14854" + burn_role[2:] + MIDAS[2:].zfill(64)), 16) != 1
        or int(call("mtbill/paused()", MTBILL, "0x5c975abb"), 16)
        or int(call("midas/paused()", MIDAS, "0x5c975abb"), 16)
    ):
        raise ValueError("Midas vault does not establish a live mTBILL backing link")

    init = capture["reads"]["midas_pool_eth/initialization"]
    log, = init["result"]
    event = "0xdd466e674ea557f56295e2d0218a125ea4b4f0f6f3307b95f85e6110838d6438"
    topics = [event, MTBILL_POOL_ID, "0x" + word(0), "0x" + MTBILL[2:].zfill(64)]
    query, = init["params"]
    if (
        init["method"] != "eth_getLogs" or query["address"] != POOL_MANAGER
        or query["topics"] != topics[:2] or log["address"] != POOL_MANAGER or log["topics"] != topics
        or log["removed"] or not int(query["fromBlock"], 16) <= int(log["blockNumber"], 16)
        <= int(query["toBlock"], 16) < int(capture["block"]["number"], 16)
        or abi_words(log["data"])[2] != 0
    ):
        raise ValueError("mTBILL pool identity or no-hook route mismatch")
    pool_key = topics[2][2:] + topics[3][2:] + log["data"][2:194]
    quoter = "0x52f0e24d1c21c8a0cb1e5a5dd6198556bd9e1203"
    if addr(call("midas_pool_eth/quoter_manager", quoter, "0xdc4c90d3")) != POOL_MANAGER:
        raise ValueError("mTBILL quoter uses a different pool manager")
    quote_input_wei = 10**14
    quote, _ = abi_words(call(
        "midas_pool_eth/quote", quoter,
        "0xaa9d21cb" + word(32) + pool_key + word(1) + word(quote_input_wei) + word(8 * 32) + word(0),
    ))
    manager_inventory = int(call("midas_pool_eth/manager_inventory", *balance(MTBILL, POOL_MANAGER)), 16)
    view = "0x7ffe42c4a5deea5b0fec41c94c136cf115597227"
    liquidity = int(call(f"midas_pool/{MTBILL_POOL_ID[2:]}/getLiquidity(bytes32)",
                         view, "0xfa6793d5" + MTBILL_POOL_ID[2:]), 16)
    slot = abi_words(call(f"midas_pool/{MTBILL_POOL_ID[2:]}/getSlot0(bytes32)",
                          view, "0xc815641c" + MTBILL_POOL_ID[2:]))
    transfer = "0xa9059cbb" + TEST_RECIPIENT[2:].zfill(64) + word(10**18)
    greenlist_role = "0x91d14854d2576bd6a4c5558421de15cb8ecdf4eb3282aac06b94d4f004e8cd0d00f3ebd8"
    if (int(call("midas_role/test_greenlisted", access, greenlist_role + TEST_RECIPIENT[2:].zfill(64)), 16)
            or not 0 < quote <= manager_inventory or not liquidity or not slot[0]
            or int(call("midas_pool_eth/token_transfer_simulation", MTBILL, transfer, POOL_MANAGER), 16) != 1):
        raise ValueError("no historical mTBILL acquisition route")
    feed = addr(call("midas/mTokenDataFeed()", MIDAS, "0x6254afb6"))
    midas = {
        "proxy_admin_owner": addr(call("midas/proxyAdminOwner", admin, "0x8da5cb5b")),
        "access_control": access, "ustb_redemption": helper, "quote_mtbill": D(quote).scaleb(-18),
        "quote_input_eth": D(quote_input_wei).scaleb(-18), "active_liquidity": liquidity, "pool_fee_pips": slot[3],
        "ethereum_mtbill_supply": D(int(call("mtbill/totalSupply()", MTBILL, "0x18160ddd"), 16)).scaleb(-18),
        "mtbill_nav": D(int(call("midas/nav", feed, "0x63692905"), 16)).scaleb(-18),
    }

    registry = addr(call("stbl/fetchRegistry()", STBL, "0xdd0b9ff0"))
    asset_id = int(call("stbl/fetchAssetID()", STBL, "0x04834711"), 16)
    registration = abi_words(call("stbl/fetchAssetData", registry, "0x08c9f4f2" + word(asset_id)))
    vault_data = abi_words(call("stbl/fetchVaultData()", STBL, "0x93adbb8c"))
    inventory = int(call("stbl/ussts_pool", *balance(USST, STBL_POOL)), 16)
    usst_supply = int(call("stbl/ussts_total", USST, "0x18160ddd"), 16)
    usst_quote = int(call("stbl/quote_from_1", STBL_POOL, "0x5e0d443f" + word(1) + word(0) + word(10**6)), 16)
    if (
        storage("stbl/implementation", STBL) != "0xcfeae702a0d93f0fc39be3d45178969751954f7e"
        or registry != "0xa58b634c10df2665a3de1680675d5bb9065847d2"
        or registration[9] != int(OUSG, 16)
        or registration[10] != int("f8acf255854c8d36010c849f1702eb350c8c4087", 16)
        or registration[13] != int(STBL, 16)
        or not 0 <= vault_data[4] < vault_data[5] or not 0 < vault_data[7] <= vault_data[6]
        or addr(call("stbl/pool_coin_0", STBL_POOL, "0xc6610657" + word(0))) != USST
        or addr(call("stbl/pool_coin_1", STBL_POOL, "0xc6610657" + word(1))) != USDC
        or not 0 < usst_quote <= inventory <= usst_supply
        or int(call("stbl/token_transfer_simulation", USST, transfer, STBL_POOL), 16) != 1
    ):
        raise ValueError("STBL vault deposits or USST acquisition route mismatch")
    stbl = {
        "asset_id": asset_id, "deposit_value_usd": D(vault_data[5]).scaleb(-18),
        "recorded_net_stable_value_usd": D(vault_data[5] - vault_data[4]).scaleb(-18),
        "net_deposits_ousg": D(vault_data[7]).scaleb(-18),
        "pool_usst": D(inventory).scaleb(-18), "quote_usst": D(usst_quote).scaleb(-18),
        "ethereum_usst": D(usst_supply).scaleb(-18),
    }

    flux_address = "0x95af143a021df745bc78e845b54591c53a8b3a51"
    flux = {
        "admin": addr(call("flux/admin()", flux_address, "0xf851a440")),
        "pause_guardian": addr(call("flux/pauseGuardian()", flux_address, "0x24a3d622")),
        "implementation": addr(call("flux/comptrollerImplementation()", flux_address, "0xbb82aa5e")),
    }
    for name, market in (("fousg", "0x1dd7950c266fb1be96180a8fdb0591f70200e018"),
                         ("fusdc", "0x465a5a630482f3abd6d3b84b39b29b07214d19e5")):
        flux[name] = {
            "mint_paused": bool(int(call(f"flux/{name}/mintGuardianPaused(address)",
                                        flux_address, "0x731f0c2b" + market[2:].zfill(64)), 16)),
            "borrow_paused": bool(int(call(f"flux/{name}/borrowGuardianPaused(address)",
                                          flux_address, "0x6d154ea5" + market[2:].zfill(64)), 16)),
        }
    return {"frax_pinned": frax, "midas_mtbill": midas, "stbl_usst": stbl, "flux_pinned": flux}
