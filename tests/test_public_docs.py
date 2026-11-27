from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def cells(line):
    return re.split(r"(?<!\\)\|", line.strip().strip("|"))


class PublicDocsTest(unittest.TestCase):
    def test_markdown_tables_have_consistent_column_counts(self):
        delimiter = re.compile(r"\s*:?-{3,}:?\s*")
        paths = [*ROOT.glob("*.md"), *ROOT.glob("docs/**/*.md"), *ROOT.glob("posts/**/*.md")]
        for path in paths:
            lines = path.read_text().splitlines()
            for index, line in enumerate(lines[1:], 1):
                if not line.startswith("|") or not all(delimiter.fullmatch(cell) for cell in cells(line)):
                    continue
                with self.subTest(file=path.relative_to(ROOT), line=index + 1):
                    count = len(cells(line))
                    self.assertTrue(lines[index - 1].startswith("|"))
                    self.assertEqual(len(cells(lines[index - 1])), count)
                    for row in lines[index + 1:]:
                        if not row.startswith("|"):
                            break
                        self.assertEqual(len(cells(row)), count, row)

    def test_standalone_draft_count_and_character_limit(self):
        drafts = [line[2:] for line in (ROOT / "posts/DRAFTS.md").read_text().splitlines()
                  if line.startswith("> ")]
        self.assertIn(len(drafts), range(3, 6))
        for draft in drafts:
            self.assertLessEqual(len(draft), 280)


if __name__ == "__main__":
    unittest.main()
