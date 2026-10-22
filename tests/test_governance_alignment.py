import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GovernanceAlignmentTests(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_infra_uses_canonical_assignment_and_external_approval_record(self):
        text = self.read("agents/INFRA-ORCHESTRATOR.md")
        self.assertIn("canonical assignment envelope", text)
        self.assertIn("external approval-record ID", text)
        self.assertNotIn('"approval": {', text)

    def test_openclaw_loads_governance_and_does_not_replace_handoff(self):
        text = self.read("templates/OPENCLAW-PROJECT-MANAGER-PROMPT.md")
        self.assertIn("pinned GOVERNANCE.md", text)
        self.assertIn("canonical assignment", text)
        self.assertIn("exact canonical handoff sections", text)

    def test_qa_role_does_not_assert_independence(self):
        text = self.read("agents/QA-AUDITOR.md")
        self.assertIn("The role name does not establish independence", text)
        self.assertIn("fresh or inherited context", text)
        self.assertNotIn("an independent second-pass reviewer", text)


if __name__ == "__main__":
    unittest.main()
