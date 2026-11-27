"""Refresh small, keyless historical reads. Leave the offline manifest intact."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from urllib.request import Request, urlopen

CUTOFF = 1790812799
TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
ANCHORAGE = "0x2004F7f7B600d962170d7f28114Cc123c5e98451"
BUIDL = "0x7712c34205737192402172409a8f7ccef8aa2aec"
FRXUSD = "0xcacd6fd266af91b8aed52accc382b4e165586e29"
FRXUSD_POOL = "0x13e12bb0e6a2f1a3d6901a59a9d585e89a6243e1"
USTB = "0x43415eb6ff9db7e26a15b704e7a3edce97d31c4e"
USYC = "0x136471a34f6ef19fe571effc1ca711fdb8e49f2b"
USDTB = "0xc139190f447e929f090edeb554d95abb8b18ac1c"
CURVE = "0xc2921134073151490193ac7369313c8e0b08e1e7"
FRAX_BUIDL = "0xe827abf9f462ac4f147753d86bc5f91e186e4e9c"
FRAX_USTB = "0x5fbaa3a3b489199338fbd85f7e3d444dc0504f33"


def word(value):
    return f"{value:064x}"


def balance(token, owner):
    return token, "0x70a08231" + owner[2:].lower().zfill(64)


def supply(token):
    return token, "0x18160ddd"


def decimals(token):
    return token, "0x313ce567"


def coin(index, pool=CURVE):
    return pool, "0xc6610657" + word(index)


def quote(index_in, index_out, size, pool=CURVE):
    return pool, "0x5e0d443f" + word(index_in) + word(index_out) + word(size)


BSC_BUIDL = "0x2d5bdc96d9c8aabbdb38c9a27398513e7e5ef84f"
AVAX_BUIDL = "0x53fc82f14f009009b440a706e31c9021e1196a2f"
CHAINS = {
    "ethereum": (26093737, ["https://eth.drpc.org", "https://eth-mainnet.public.blastapi.io", "https://ethereum-rpc.publicnode.com"], {
        "buidl": supply(BUIDL),
        "buidl_i": supply("0x6a9da2d710bb9b700acde7cb81f10f1ff8c89041"),
        "buidl_decimals": decimals(BUIDL),
        "spark_alm_proxy_buidl_i": balance("0x6a9da2d710bb9b700acde7cb81f10f1ff8c89041", "0x1601843c5E9bC251A3272907010AFa41Fa18347E"),
        "spark_freezable_alm_proxy_buidl_i": balance("0x6a9da2d710bb9b700acde7cb81f10f1ff8c89041", "0xe5c6318456a7Cb6f74f93B4eee4616dB5fcef699"),
        "spark_deposit_buidl_i": balance("0x6a9da2d710bb9b700acde7cb81f10f1ff8c89041", "0xD1917664bE3FdAea377f6E8D5BF043ab5C3b1312"),
        "spark_redeem_buidl_i": balance("0x6a9da2d710bb9b700acde7cb81f10f1ff8c89041", "0x8780Dd016171B91E4Df47075dA0a947959C34200"),
        "buidl_i_decimals": decimals("0x6a9da2d710bb9b700acde7cb81f10f1ff8c89041"),
        "ustb": supply(USTB),
        "ustb_decimals": decimals(USTB),
        "usyc": supply(USYC),
        "usyc_decimals": decimals(USYC),
        "usyc_nav": ("0x4c48bcb2160f8e0adbf9d4f3b034f1e36d1f8b3e", "0xfeaf968c"),
        "usyc_nav_decimals": decimals("0x4c48bcb2160f8e0adbf9d4f3b034f1e36d1f8b3e"),
        "usdtb": supply(USDTB),
        "usdtb_decimals": decimals(USDTB),
        "curve_usdtb": balance(USDTB, CURVE),
        "curve_coin_0": coin(0),
        "curve_coin_1": coin(1),
        "curve_quote": quote(0, 1, 1_000_000),
        "usual_treasury_usyc": balance(USYC, "0xdd82875f0840aad58a455a70b88eed9f59cec7c7"),
        "usual_dao_usyc": balance(USYC, "0xde6e1f680c4816446c8d515989e2358636a38b04"),
        "usual_treasury_code": ("0xdd82875f0840aad58a455a70b88eed9f59cec7c7",),
        "usual_dao_code": ("0xde6e1f680c4816446c8d515989e2358636a38b04",),
        "curve_frxusd_coin_0": coin(0, FRXUSD_POOL),
        "curve_frxusd_coin_1": coin(1, FRXUSD_POOL),
        "curve_frxusd_quote": quote(1, 0, 10**18, FRXUSD_POOL),
        "curve_frxusd_balance": balance(FRXUSD, FRXUSD_POOL),
        "frax_buidl": balance(BUIDL, FRAX_BUIDL),
        "frax_ustb": balance(USTB, FRAX_USTB),
        "frax_buidl_code": (FRAX_BUIDL,),
        "frax_ustb_code": (FRAX_USTB,),
    }),
    "bsc": (125000754, ["https://bsc.drpc.org", "https://bsc-mainnet.public.blastapi.io", "https://bsc-rpc.publicnode.com"], {
        "buidl": supply(BSC_BUIDL),
        "buidl_decimals": decimals(BSC_BUIDL),
        "anchorage_buidl": balance(BSC_BUIDL, ANCHORAGE),
        "anchorage_code": (ANCHORAGE,),
        "usyc": supply("0x8d0fa28f221eb5735bc71d3a0da67ee5bc821311"),
        "usyc_decimals": decimals("0x8d0fa28f221eb5735bc71d3a0da67ee5bc821311"),
    }),
    "avalanche": (96488899, ["https://api.avax.network/ext/bc/C/rpc", "https://avalanche.drpc.org", "https://avalanche-c-chain-rpc.publicnode.com"], {
        "buidl": supply(AVAX_BUIDL),
        "buidl_decimals": decimals(AVAX_BUIDL),
        "anchorage_buidl": balance(AVAX_BUIDL, ANCHORAGE),
        "anchorage_code": (ANCHORAGE,),
    }),
    "polygon": (94738439, ["https://polygon.drpc.org", "https://polygon-bor-rpc.publicnode.com"], {
        "buidl": supply("0x2893ef551b6dd69f661ac00f11d93e5dc5dc0e99"),
        "buidl_decimals": decimals("0x2893ef551b6dd69f661ac00f11d93e5dc5dc0e99"),
    }),
    "optimism": (157607011, ["https://optimism.drpc.org", "https://optimism-rpc.publicnode.com"], {
        "buidl": supply("0xa1cdab15bba75a80df4089cafba013e376957cf5"),
        "buidl_decimals": decimals("0xa1cdab15bba75a80df4089cafba013e376957cf5"),
    }),
    "tempo": (42021929, ["https://rpc.tempo.xyz"], {
        "buidl": supply("0xb5ff12bd8010baef823d1bfa2ce6bdc0109cbb24"),
        "buidl_decimals": decimals("0xb5ff12bd8010baef823d1bfa2ce6bdc0109cbb24"),
    }),
    "arbitrum": (510496863, ["https://arbitrum-one.public.blastapi.io", "https://arbitrum.drpc.org", "https://arbitrum-one-rpc.publicnode.com"], {
        "buidl": supply("0xa6525ae43edcd03dc08e775774dcabd3bb925872"),
        "buidl_decimals": decimals("0xa6525ae43edcd03dc08e775774dcabd3bb925872"),
    }),
}


def read(url, method, params):
    body = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    request = Request(url, json.dumps(body).encode(), {"Content-Type": "application/json", "User-Agent": "rwa-allowlist-study/1"})
    with urlopen(request, timeout=6) as response:
        result = json.load(response)
    if result.get("result") is None:
        raise ValueError(result.get("error", "missing result"))
    return result["result"]


def find_block(url, candidate):
    for _ in range(6):
        block, successor = [
            read(url, "eth_getBlockByNumber", [hex(height), False])
            for height in (candidate, candidate + 1)
        ]
        if int(block["timestamp"], 16) > CUTOFF:
            candidate -= 1
        elif int(successor["timestamp"], 16) <= CUTOFF:
            candidate += 1
        else:
            keys = ("number", "timestamp", "hash", "parentHash")
            return [{key: header[key] for key in keys} for header in (block, successor)]

    raise ValueError("block locator did not bracket cutoff within six probes")


def capture(chain, config):
    candidate, endpoints, reads = config
    result = {"failures": [], "reads": {}}
    headers = None
    for url in endpoints:
        try:
            chain_headers = find_block(url, candidate)
        except (OSError, ValueError) as error:
            result["failures"].append({"url": url, "read": "block", "error": str(error)})
            continue
        if headers and headers != chain_headers:
            raise ValueError(f"{chain} block headers differ across endpoints")
        headers = chain_headers
        result.update(block=headers[0], successor=headers[1])
        for label, (address, *data) in reads.items():
            if label in result["reads"]:
                continue
            method = "eth_call" if data else "eth_getCode"
            args = [{"to": address, "data": data[0]} if data else address, headers[0]["number"]]
            try:
                value = read(url, method, args)
                if data and value == "0x":
                    raise ValueError("empty call result")
            except (OSError, ValueError) as error:
                result["failures"].append({"url": url, "read": label, "error": str(error)})
            else:
                result["reads"][label] = {"url": url, "method": method, "params": args, "result": value}
        if len(result["reads"]) == len(reads):
            break
    return chain, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--chain", action="append", choices=CHAINS)
    args = parser.parse_args()
    chains = [(name, CHAINS[name]) for name in (args.chain or CHAINS)]
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(lambda entry: capture(*entry), chains))
    args.output.write_text(json.dumps({"cutoff": CUTOFF, "chains": dict(rows)}, indent=2) + "\n")


if __name__ == "__main__":
    main()
