"""Retrieve cited publisher files and extract the relevant PDF pages under data/upstream/."""
import argparse
from hashlib import sha256
from pathlib import Path
import subprocess
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, build_opener

OUTPUT = Path(__file__).resolve().parents[1] / "data" / "upstream"
MAX_BYTES = 25 * 1024 * 1024
SOURCES = {
    "anchorage": (
        "https://learn.anchorage.com/09.30.26_USDtb-Stablecoin-Attestation-Report-signed.pdf",
        "anchorage-usdtb-2026-09-30.pdf",
        "11225e1c5994cd6ef65098c721a7aa8b6f564e9f395a5d1bc468b8405b6bb99f",
    ),
    "circle": (
        "https://s206.q4cdn.com/265218871/files/doc_earnings/2026/q3/presentation/3Q26-Earnings-Presentation.pdf",
        "circle-q3-2026.pdf",
        "c4e66ce5b002b1add783d7b3781b76fcbb9d332ef8217e7bba67cdcba2380ce6",
    ),
    "securitize": (
        "https://s21.q4cdn.com/825684987/files/content_files/SECZ-3Q26-Earnings-Press-Release_vF.pdf",
        "securitize-q3-2026.pdf",
        "9d0e4f1a2e7041cc0f3f3bc2ab14f0fc7a4f4114af9bbceadbd99b4b87dca921",
    ),
    "curve": (
        "https://api.curve.finance/v1/getPools/ethereum/factory-stable-ng", "curve-registry.json", None,
    ),
    "superstate": (
        "https://api.superstate.com/v2/funds/1/data?lookback=90&include_holdings=false",
        "superstate-ustb-recent.json", None,
    ),
    "superstate-deployments": (
        "https://api.superstate.com/v3/funds/USTB", "superstate-ustb-deployments.json", None,
    ),
    "ondo": ("https://ondo.finance/ousg", "ondo-ousg.html", None),
    "franklin": (
        "https://www.sec.gov/Archives/edgar/data/1786958/000207169126023634/primary_doc.xml",
        "franklin-2026-09-30.xml", None,
    ),
    "usual-dao": (
        "https://api.routescan.io/v2/network/mainnet/evm/1/etherscan/api?module=contract&action=getsourcecode&address=0x0eec861d49f15f585d6bb4301fc4f89bce22af4e",
        "usual-dao-source.json", None,
    ),
    "usual-usd0": (
        "https://api.routescan.io/v2/network/mainnet/evm/1/etherscan/api?module=contract&action=getsourcecode&address=0xae12f6f805842e6dafe71a6d2b41b28ba5fc821e",
        "usual-usd0-source.json", None,
    ),
}


class SameHostRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urlsplit(newurl)
        if (target.scheme != "https" or target.netloc != urlsplit(req.full_url).netloc):
            raise ValueError("redirect to another origin")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", choices=tuple(SOURCES))
    parser.add_argument("--extract", action="store_true", help="extract verified PDF text using pdftotext")
    args = parser.parse_args()
    url, filename, expected_hash = SOURCES[args.source]
    if args.extract and expected_hash is None:
        parser.error("--extract requires a pinned PDF source")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT / filename
    try:
        if destination.exists():
            with destination.open("rb") as existing:
                body = existing.read(MAX_BYTES + 1)
        else:
            with build_opener(SameHostRedirect()).open(url, timeout=30) as response:
                body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError("source exceeded the download limit")
        digest = sha256(body).hexdigest()
        if expected_hash and (digest != expected_hash or not body.startswith(b"%PDF-")):
            raise ValueError("publisher file differs from the pinned PDF")
        if not destination.exists():
            with destination.open("xb") as output:
                output.write(body)
        if args.extract:
            pages = ["-f", "12", "-l", "12"] if args.source == "circle" else []
            extracted = subprocess.check_output(["pdftotext", "-layout", *pages, str(destination), "-"])
            destination.with_suffix(".txt").write_bytes(extracted)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{args.source}: {error}\n")

    print(f"{digest}  data/upstream/{filename}")


if __name__ == "__main__":
    main()
