from hashlib import sha256
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import check_post_card

ROOT = Path(__file__).resolve().parents[1]


class PostCardTest(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for folder in ("posts", "docs/figures", "evidence"):
            shutil.copytree(ROOT / folder, self.root / folder)
        patcher = patch.object(check_post_card, "ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.receipt_path = self.root / "posts/cards/usdtb-buidl.json"
        self.receipt = json.loads(self.receipt_path.read_text())
        self.draft = self.root / "posts/DRAFTS.md"

    def rewrite_copy(self, old, new):
        path = self.root / self.receipt["html"]["path"]
        source = path.read_text()
        self.assertIn(old, source)
        updated = source.replace(old, new, 1)
        path.write_text(updated)
        self.receipt["html"]["sha256"] = sha256(path.read_bytes()).hexdigest()
        self.receipt_path.write_text(json.dumps(self.receipt))

    def test_exact_artifacts_pass(self):
        self.assertEqual(check_post_card.check(), 12)

    def test_card_rejects_hash_verified_html_that_changes_visible_copy(self):
        # Same word count and amount. Only the receipt's exact copy check can reject this.
        self.rewrite_copy("Anchorage reserve report", "Anchorage reserve record")
        with self.assertRaisesRegex(ValueError, "card copy or word count"):
            check_post_card.check()

    def test_card_rejects_more_than_twenty_words_even_with_an_updated_receipt(self):
        extra = " one two three four five six seven eight nine"
        self.receipt["visible_text"] = self.receipt["visible_text"].replace(
            "Anchorage reserve report", "Anchorage reserve report" + extra)
        self.receipt["words"] = 21
        self.rewrite_copy("Anchorage reserve report", "Anchorage reserve report" + extra)
        with self.assertRaisesRegex(ValueError, "card copy or word count"):
            check_post_card.check()

    def test_card_rejects_changed_artifact_bytes(self):
        for artifact in ("html", "png"):
            with self.subTest(artifact=artifact):
                path = self.root / self.receipt[artifact]["path"]
                original = path.read_bytes()
                path.write_bytes(original + b"x")
                try:
                    with self.assertRaisesRegex(ValueError, f"{artifact} differs"):
                        check_post_card.check()
                finally:
                    path.write_bytes(original)

    def test_card_rejects_malformed_png_and_wrong_dimensions_with_updated_hash(self):
        path = self.root / self.receipt["png"]["path"]
        png = path.read_bytes()
        for altered, message in (
            (b"\x00" + png[1:], "PNG header"),
            (png[:16], "PNG header"),
            (png[:16] + (640).to_bytes(4, "big") + png[20:], "card size"),
        ):
            with self.subTest(message=message):
                path.write_bytes(altered)
                self.receipt["png"]["sha256"] = sha256(altered).hexdigest()
                self.receipt_path.write_text(json.dumps(self.receipt))
                with self.assertRaisesRegex(ValueError, message):
                    check_post_card.check()

    def test_card_requires_one_claim_in_the_usdtb_draft(self):
        draft = self.draft.read_text()
        claim = next(line for line in draft.splitlines() if line.startswith("> "))
        self.draft.write_text(draft.replace(claim, claim + "\n> Another claim.", 1))
        with self.assertRaisesRegex(ValueError, "single claim"):
            check_post_card.check()

    def test_card_rejects_missing_draft_links(self):
        original = self.draft.read_text()
        for key in ("publisher_url", "evidence_url", "png"):
            with self.subTest(link=key):
                url = "../" + self.receipt[key]["path"] if key == "png" else self.receipt[key]
                self.assertIn(url, original)
                self.draft.write_text(original.replace(url, ""))
                message = "does not reference the checked PNG" if key == "png" else "must link to the study"
                with self.assertRaisesRegex(ValueError, message):
                    check_post_card.check()

    def test_card_rejects_draft_amount_or_date_mismatch(self):
        original = self.draft.read_text()
        for old, new in (("$533M", "$534M"), ("September 30, 2026", "September 29, 2026")):
            with self.subTest(value=old):
                self.assertIn(old, original)
                self.draft.write_text(original.replace(old, new, 1))
                with self.assertRaisesRegex(ValueError, "transcribed amount and date"):
                    check_post_card.check()


if __name__ == "__main__":
    unittest.main()
