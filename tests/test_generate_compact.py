import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.generate_compact_instructions import changed_sources, compact_block, source_commit_from_artifact


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

    def test_detects_canonical_source_changed_after_recorded_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("GOVERNANCE.md", "AGENT-OPERATING-PROTOCOL.md"):
                (root / name).write_text("recorded\n", encoding="utf-8")
            with patch(
                "scripts.generate_compact_instructions.source_at",
                return_value="recorded\n",
            ):
                self.assertEqual(changed_sources(root, "a" * 40), [])
                (root / "GOVERNANCE.md").write_text("changed\n", encoding="utf-8")
                self.assertEqual(changed_sources(root, "a" * 40), ["GOVERNANCE.md"])


if __name__ == "__main__":
    unittest.main()
