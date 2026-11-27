"""Verify the September transcriptions against hash-pinned publisher PDFs."""
from decimal import Decimal
import json
from pathlib import Path
import re

if __package__:
    from .fetch_sources import extract_pdf, fetch_source
else:
    from fetch_sources import extract_pdf, fetch_source

EVIDENCE = Path(__file__).resolve().parents[1] / "evidence"
MONEY = r"([0-9][0-9,]*(?:\.[0-9]+)?)"


def match(pattern, text):
    result = re.search(pattern, text)
    if result is None:
        raise ValueError(f"publisher text missing expected label or structure: {pattern}")
    return result


def number(value):
    return Decimal(value.replace(",", ""))


def equal(label, actual, expected):
    if actual != expected:
        raise ValueError(f"{label}: publisher {actual!r}, transcription {expected!r}")


def verify(facts, texts):
    count = 0

    def check(label, actual, expected):
        nonlocal count
        equal(label, actual, expected)
        count += 1

    securitize = " ".join(texts["securitize"].split())
    value = match(r"total Tokenized Assets on Platform of \$" + MONEY
                  + r" billion as of September 30, 2026", securitize)[1]
    check("Securitize platform value", number(value) * 10**9,
          Decimal(facts["securitize_platform_value_display_usd"]))
    match(r"across both funds and equities", securitize)

    # The slide is multicolumn. Find the amount directly above the USYC label.
    rows = texts["circle"].splitlines()
    for index, line in enumerate(rows):
        if "USYC assets" in line:
            start = line.index("USYC assets")
            value = match(r"\$" + MONEY + "B", rows[index - 1][start - 4:start + 15])[1]
            break
    else:
        raise ValueError("Circle slide 12 missing USYC assets column")
    check("Circle USYC assets", number(value) * 10**9, Decimal(facts["circle_usyc_display_usd"]))

    anchorage = texts["anchorage"]
    match(r"September 30, 2026", anchorage)
    total = match(r"Total BUIDL\s+\$" + MONEY, anchorage)[1]
    check("Anchorage total BUIDL", number(total), Decimal(facts["anchorage_total_buidl_usd"]))
    units = match(r"Company self-custodied " + MONEY + " BUIDL", anchorage)[1]
    check("BUIDL fair value per reserved unit", number(total) / number(units), Decimal(facts["buidl_nav_usd"]))
    ethereum, published_total = match(r"d\.\s+Total USDtb redeemable\s+" + MONEY
                                      + r"\s+[\d,]+\s+" + MONEY, anchorage).groups()
    for key, value in (("ethereum", ethereum), ("total", published_total)):
        check(f"USDtb redeemable ({key})", number(value), Decimal(facts[f"anchorage_{key}_usdtb_redeemable"]))
    chains = {"solana": "Solana", "bsc": "BSC", "avalanche": "Avalanche", "aptos": "Aptos"}
    check("Schedule II chain set", {row["chain"] for row in facts["anchorage_reserve_legs"]}, set(chains))
    for row in facts["anchorage_reserve_legs"]:
        chain = chains[row["chain"]]
        value = match(rf"{chain} BUIDL\S*[^\S\n]+\$" + MONEY, anchorage)[1]
        address = match(rf"{chain} BUIDL refers to the BUIDL held on {chain} at ([A-Za-z0-9]+)", anchorage)[1]
        check(f"{chain} BUIDL value", number(value), Decimal(row["buidl_usd"]))
        check(f"{chain} custody location", address, row["custody_address"])
    return count


def main():
    facts = json.loads((EVIDENCE / "primary-transcriptions-2026-09-30.json").read_text())
    texts = {source: extract_pdf(source, fetch_source(source)[0]).decode()
             for source in ("securitize", "circle", "anchorage")}
    print(f"{verify(facts, texts)} PDF transcription checks passed (three publisher PDF hashes verified).")


if __name__ == "__main__":
    main()
