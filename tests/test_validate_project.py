import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_project import validate


SHA = "5d644751ef9b909d0ac792942c71491cd1ebde31"


def manifest(profile="lightweight"):
    files = {"project": "PROJECT.md", "state": "STATE.md", "progress": "PROGRESS.md"}
    if profile == "full":
        files.update(
            rules="RULES.md",
            tasks="TASKS.md",
            decisions="DECISIONS.md",
            checks="CHECKS.md",
        )
    return {
        "schema_version": 1,
        "project_id": "pilot-project",
        "profile": profile,
        "framework": {
            "version": "0.1",
            "repository": "https://github.com/bedriozgur/ai-work-framework",
            "commit": SHA,
        },
        "canonical_repository": "https://github.com/example/pilot-project",
        "files": files,
    }


class ValidatorTests(unittest.TestCase):
    def make_project(self, data):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "project.yaml").write_text(json.dumps(data), encoding="utf-8")
        for file_name in data.get("files", {}).values():
            (root / file_name).write_text("# test\n", encoding="utf-8")
        return temp, root

    def test_lightweight_manifest(self):
        temp, root = self.make_project(manifest())
        self.addCleanup(temp.cleanup)
        self.assertEqual(validate(root), [])

    def test_full_manifest(self):
        temp, root = self.make_project(manifest("full"))
        self.addCleanup(temp.cleanup)
        self.assertEqual(validate(root), [])

    def test_rejects_moving_ref(self):
        data = manifest()
        data["framework"]["commit"] = "main"
        temp, root = self.make_project(data)
        self.addCleanup(temp.cleanup)
        self.assertIn(
            "framework.commit must be an exact lowercase 40-character Git SHA",
            validate(root),
        )

    def test_rejects_missing_profile_file(self):
        temp, root = self.make_project(manifest("full"))
        self.addCleanup(temp.cleanup)
        (root / "CHECKS.md").unlink()
        self.assertIn("missing required file: CHECKS.md", validate(root))

    def test_rejects_parent_path(self):
        data = manifest()
        data["files"]["state"] = "../STATE.md"
        temp, root = self.make_project(data)
        self.addCleanup(temp.cleanup)
        self.assertIn("files.state must be a relative path inside the project", validate(root))


if __name__ == "__main__":
    unittest.main()
