"""Check the exact USDtb card, visible copy and numeric receipt offline."""
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]


class CardText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_card = False
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.in_card = True
        elif self.in_card:
            self.text.append(" ")

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_card = False

    def handle_data(self, data):
        if self.in_card:
            self.text.append(data)


def check():
    receipt = json.loads((ROOT / "posts/cards/usdtb-buidl.json").read_text())
    files = {}
    for name in ("html", "png"):
        path = ROOT / receipt[name]["path"]
        files[name] = path.read_bytes()
        if sha256(files[name]).hexdigest() != receipt[name]["sha256"]:
            raise ValueError(f"{name} differs from the inspected card")
    png = files["png"]
    if png[:16] != b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR":
        raise ValueError("card lacks a valid PNG header")
    if list(struct.unpack(">II", png[16:24])) != receipt["size_px"]:
        raise ValueError("card size differs from the inspected export")

    parser = CardText()
    parser.feed(files["html"].decode())
    copy = " ".join("".join(parser.text).split())
    words = sum(any(char.isalnum() for char in word) for word in copy.split())
    if not 0 < words <= 20 or words != receipt["words"] or copy != receipt["visible_text"]:
        raise ValueError("card copy or word count differs from the receipt")
    source = json.loads((ROOT / "evidence/primary-transcriptions-2026-09-30.json").read_text())
    millions = (Decimal(source["anchorage_total_buidl_usd"]) / 10**6).quantize(
        Decimal(1), rounding=ROUND_HALF_UP)
    when = date.fromisoformat(source["date"])
    number = f"${millions}M"
    written_date = f"{when:%B} {when.day}, {when.year}"
    drafts = (ROOT / "posts/DRAFTS.md").read_text()
    _, heading, section = drafts.partition("\n## USDtb reserves\n")
    if not heading:
        raise ValueError("missing USDtb draft")
    draft = section.split("\n## ", 1)[0]
    claims = [line[2:] for line in draft.splitlines() if line.startswith("> ")]
    for value in (number, written_date):
        if value not in copy or len(claims) != 1 or value not in claims[0]:
            raise ValueError("the card and draft must carry the transcribed amount and date")
    if receipt["evidence_url"] not in draft or receipt["publisher_url"] not in draft:
        raise ValueError("the draft must link to the study evidence and the primary report")
    if f"(../{receipt['png']['path']})" not in draft:
        raise ValueError("the draft does not reference the checked PNG")
    return words


if __name__ == "__main__":
    print(f"USDtb card verified: {check()} words, evidence receipts, exact HTML and PNG hashes.")
