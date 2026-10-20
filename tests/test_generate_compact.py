import tempfile
import unittest
from pathlib import Path

from scripts.generate_compact_instructions import compact_block, source_commit_from_artifact


class CompactGenerationTests(unittest.TestCase):
    def test_extracts_marked_governance_block(self):
        source = "before\n<!-- COMPACT:START -->\nrequired\n<!-- COMPACT:END -->\nafter\n"
        self.assertEqual(compact_block(source), "required")

    def test_reads_source_commit_from_artifact(self):
        commit = "a" * 40
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "compact.md"
            path.write_text(f"Source commit: `{commit}`\n", encoding="utf-8")
            self.assertEqual(source_commit_from_artifact(path), commit)


if __name__ == "__main__":
    unittest.main()

