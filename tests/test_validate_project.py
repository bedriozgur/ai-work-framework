import json
import os
import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.validate_project import load_profiles, parse_json, validate


SHA = "1f38b4943792466a68f882ef3886f35791438e8a"


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
    def test_framework_profile_contract(self):
        self.assertEqual(load_profiles()["lightweight"], {"project", "state", "progress"})
        self.assertEqual(
            load_profiles()["full"],
            {"project", "rules", "state", "tasks", "progress", "decisions", "checks"},
        )

    def make_project(self, data, create_files=True):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "project.yaml").write_text(json.dumps(data), encoding="utf-8")
        if create_files:
            for file_name in data.get("files", {}).values():
                if isinstance(file_name, str) and "/" not in file_name and "\\" not in file_name:
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

    def test_rejects_unresolved_commit(self):
        data = manifest()
        data["framework"]["commit"] = "f" * 40
        temp, root = self.make_project(data)
        self.addCleanup(temp.cleanup)
        self.assertTrue(
            any("cannot resolve pinned framework commit" in error for error in validate(root))
        )

    def test_rejects_version_mismatch_with_pinned_contract(self):
        data = manifest()
        data["framework"]["version"] = "9.9"
        temp, root = self.make_project(data)
        self.addCleanup(temp.cleanup)
        self.assertIn(
            "framework.version '9.9' does not match pinned contract '0.1'",
            validate(root),
        )

    def test_invalid_framework_field_types_return_errors_without_crashing(self):
        cases = (
            ("repository", 123),
            ("commit", 123),
            ("version", ["0.1"]),
        )
        for field, value in cases:
            with self.subTest(field=field):
                data = manifest()
                data["framework"][field] = value
                temp, root = self.make_project(data)
                try:
                    errors = validate(root)
                    self.assertTrue(any(f"framework.{field} is required" in error for error in errors))
                finally:
                    temp.cleanup()

    def test_invalid_profile_type_returns_error_without_crashing(self):
        data = manifest()
        data["profile"] = []
        temp, root = self.make_project(data)
        self.addCleanup(temp.cleanup)
        self.assertIn("profile is required", validate(root))

    def test_rejects_repository_identity_mismatch(self):
        data = manifest()
        data["framework"]["repository"] = "https://github.com/example/not-the-framework"
        temp, root = self.make_project(data)
        self.addCleanup(temp.cleanup)
        self.assertTrue(
            any("does not match local origin" in error for error in validate(root))
        )

    def test_rejects_duplicate_json_keys(self):
        raw = json.dumps(manifest()).replace(
            '"profile": "lightweight",',
            '"profile": "lightweight", "profile": "full",',
        )
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / "project.yaml").write_text(raw, encoding="utf-8")
        self.assertTrue(any("duplicate JSON key: profile" in error for error in validate(root)))

    def test_parse_json_rejects_duplicate_contract_keys(self):
        with self.assertRaises(ValueError):
            parse_json('{"profiles": {}, "profiles": {}}')

    def test_rejects_windows_and_backslash_paths(self):
        invalid = [r"..\STATE.md", r"C:\Windows\win.ini", r"D:STATE.md", r"\\server\share\STATE.md"]
        for value in invalid:
            with self.subTest(value=value):
                data = manifest()
                data["files"]["state"] = value
                temp, root = self.make_project(data)
                try:
                    self.assertIn(
                        "files.state must be a relative path inside the project",
                        validate(root),
                    )
                finally:
                    temp.cleanup()

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unavailable")
    def test_rejects_symlink_escape(self):
        temp, root = self.make_project(manifest())
        self.addCleanup(temp.cleanup)
        outside = Path(temp.name).parent / f"outside-{Path(temp.name).name}.md"
        outside.write_text("# outside\n", encoding="utf-8")
        self.addCleanup(outside.unlink)
        (root / "STATE.md").unlink()
        (root / "STATE.md").symlink_to(outside)
        self.assertIn("required file escapes project root: STATE.md", validate(root))

    def test_rejects_unfilled_control_template(self):
        temp, root = self.make_project(manifest())
        self.addCleanup(temp.cleanup)
        (root / "PROJECT.md").write_text(
            "# Project\n\n## Objective\n<!-- What outcome is required? -->\n",
            encoding="utf-8",
        )
        self.assertIn(
            "required file contains unfilled template marker '<!--': PROJECT.md",
            validate(root),
        )

    def test_duplicate_control_paths_are_case_insensitive(self):
        data = manifest()
        data["files"]["state"] = "PROJECT.md"
        temp, root = self.make_project(data)
        self.addCleanup(temp.cleanup)
        self.assertIn("duplicate control-file path: PROJECT.md", validate(root))

    def test_verified_snapshot_accepts_matching_contract(self):
        data = manifest()
        temp, root = self.make_project(data)
        self.addCleanup(temp.cleanup)
        snapshot = root / "snapshot"
        snapshot.mkdir()
        repository_root = Path(__file__).resolve().parents[1]
        contract = subprocess.run(
            ["git", "-C", str(repository_root), "show", f"{SHA}:framework.yaml"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        (snapshot / "framework.yaml").write_text(contract, encoding="utf-8")
        metadata_raw = json.dumps(
            {
                "schema_version": 1,
                "repository": data["framework"]["repository"],
                "commit": SHA,
                "framework_yaml_sha256": hashlib.sha256(contract.encode("utf-8")).hexdigest(),
            }
        )
        (snapshot / "snapshot.json").write_text(metadata_raw, encoding="utf-8")
        metadata_hash = hashlib.sha256(metadata_raw.encode("utf-8")).hexdigest()
        self.assertEqual(
            validate(
                root,
                framework_snapshot=snapshot,
                framework_snapshot_sha256=metadata_hash,
            ),
            [],
        )

    def test_verified_snapshot_requires_out_of_band_metadata_hash(self):
        data = manifest()
        temp, root = self.make_project(data)
        self.addCleanup(temp.cleanup)
        snapshot = root / "snapshot"
        snapshot.mkdir()
        (snapshot / "framework.yaml").write_text("{}", encoding="utf-8")
        (snapshot / "snapshot.json").write_text("{}", encoding="utf-8")
        self.assertTrue(
            any(
                "--framework-snapshot-sha256 is required" in error
                for error in validate(root, framework_snapshot=snapshot)
            )
        )

    def test_snapshot_contract_rejects_empty_profiles_without_failing_open(self):
        data = manifest()
        data["profile"] = "invented"
        data["files"] = {}
        temp, root = self.make_project(data)
        self.addCleanup(temp.cleanup)
        snapshot = root / "snapshot"
        snapshot.mkdir()
        contract = json.dumps(
            {
                "schema_version": 1,
                "framework": {"version": "0.1"},
                "profiles": {},
            }
        )
        (snapshot / "framework.yaml").write_text(contract, encoding="utf-8")
        metadata_raw = json.dumps(
            {
                "schema_version": 1,
                "repository": data["framework"]["repository"],
                "commit": SHA,
                "framework_yaml_sha256": hashlib.sha256(contract.encode("utf-8")).hexdigest(),
            }
        )
        (snapshot / "snapshot.json").write_text(metadata_raw, encoding="utf-8")
        metadata_hash = hashlib.sha256(metadata_raw.encode("utf-8")).hexdigest()
        errors = validate(
            root,
            framework_snapshot=snapshot,
            framework_snapshot_sha256=metadata_hash,
        )
        self.assertTrue(any("profiles must not be empty" in error for error in errors))

    def test_verified_snapshot_rejects_hash_mismatch(self):
        data = manifest()
        temp, root = self.make_project(data)
        self.addCleanup(temp.cleanup)
        snapshot = root / "snapshot"
        snapshot.mkdir()
        (snapshot / "framework.yaml").write_text('{"schema_version": 1, "profiles": {}}', encoding="utf-8")
        metadata_raw = json.dumps(
            {
                "schema_version": 1,
                "repository": data["framework"]["repository"],
                "commit": SHA,
                "framework_yaml_sha256": "0" * 64,
            }
        )
        (snapshot / "snapshot.json").write_text(metadata_raw, encoding="utf-8")
        metadata_hash = hashlib.sha256(metadata_raw.encode("utf-8")).hexdigest()
        self.assertTrue(
            any(
                "framework snapshot contract hash mismatch" in error
                for error in validate(
                    root,
                    framework_snapshot=snapshot,
                    framework_snapshot_sha256=metadata_hash,
                )
            )
        )

    def test_snapshot_creator_rejects_false_repository_identity(self):
        repository_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    "python3",
                    str(repository_root / "scripts/create_framework_snapshot.py"),
                    str(Path(directory) / "snapshot"),
                    "--repo",
                    str(repository_root),
                    "--repository-url",
                    "https://github.com/example/fake-framework",
                    "--commit",
                    SHA,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not match local origin", result.stderr)

    def test_snapshot_creator_and_validator_round_trip(self):
        repository_root = Path(__file__).resolve().parents[1]
        data = manifest()
        temp, root = self.make_project(data)
        self.addCleanup(temp.cleanup)
        snapshot = root / "snapshot"
        result = subprocess.run(
            [
                "python3",
                str(repository_root / "scripts/create_framework_snapshot.py"),
                str(snapshot),
                "--repo",
                str(repository_root),
                "--repository-url",
                data["framework"]["repository"],
                "--commit",
                SHA,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        digest_line = next(
            line for line in result.stdout.splitlines() if line.startswith("SNAPSHOT_JSON_SHA256: ")
        )
        digest = digest_line.split(": ", 1)[1]
        self.assertEqual(
            validate(
                root,
                framework_snapshot=snapshot,
                framework_snapshot_sha256=digest,
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
