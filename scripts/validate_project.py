#!/usr/bin/env python3
"""Validate the v0.1 project manifest and required control files.

The manifest uses JSON syntax saved as project.yaml. JSON is valid YAML 1.2 and
keeps this validator dependency-free. This deliberately validates structure,
not the truth of project claims or the availability of remote repositories.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath


SHA40 = re.compile(r"^[0-9a-f]{40}$")
PLACEHOLDERS = {"replace-me", "https://github.com/owner/repository", "0" * 40}


def load_profiles() -> dict[str, set[str]]:
    contract_path = Path(__file__).resolve().parents[1] / "framework.yaml"
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"invalid framework contract {contract_path}: {exc}") from exc

    if contract.get("schema_version") != 1 or not isinstance(contract.get("profiles"), dict):
        raise RuntimeError("framework.yaml must define schema_version 1 and profiles")

    profiles: dict[str, set[str]] = {}
    for name, definition in contract["profiles"].items():
        keys = definition.get("required_file_keys") if isinstance(definition, dict) else None
        if not isinstance(keys, list) or not keys or not all(isinstance(key, str) and key for key in keys):
            raise RuntimeError(f"profile {name!r} must define non-empty required_file_keys")
        if len(keys) != len(set(keys)):
            raise RuntimeError(f"profile {name!r} contains duplicate required_file_keys")
        profiles[name] = set(keys)
    return profiles


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def relative_file(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        profiles = load_profiles()
    except RuntimeError as exc:
        return [str(exc)]
    manifest_path = root / "project.yaml"
    if not manifest_path.is_file():
        return ["missing project.yaml"]

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"project.yaml must use valid JSON/YAML-1.2 syntax: {exc}"]

    if not isinstance(data, dict):
        return ["project.yaml root must be an object"]
    if data.get("schema_version") != 1:
        fail(errors, "schema_version must be 1")

    project_id = data.get("project_id")
    if not isinstance(project_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", project_id):
        fail(errors, "project_id must use lowercase letters, digits, dot, underscore, or hyphen")
    elif project_id in PLACEHOLDERS:
        fail(errors, "project_id placeholder must be replaced")

    profile = data.get("profile")
    if profile not in profiles:
        fail(errors, "profile must be one of: " + ", ".join(sorted(profiles)))

    framework = data.get("framework")
    if not isinstance(framework, dict):
        fail(errors, "framework must be an object")
    else:
        for field in ("version", "repository", "commit"):
            if not isinstance(framework.get(field), str) or not framework[field]:
                fail(errors, f"framework.{field} is required")
        commit = framework.get("commit", "")
        if not SHA40.fullmatch(commit):
            fail(errors, "framework.commit must be an exact lowercase 40-character Git SHA")
        elif commit in PLACEHOLDERS:
            fail(errors, "framework.commit placeholder must be replaced")

    canonical = data.get("canonical_repository")
    if not isinstance(canonical, str) or not canonical:
        fail(errors, "canonical_repository is required")
    elif canonical in PLACEHOLDERS:
        fail(errors, "canonical_repository placeholder must be replaced")

    files = data.get("files")
    if not isinstance(files, dict):
        fail(errors, "files must be an object")
    elif profile in profiles:
        expected = profiles[profile]
        missing_keys = sorted(expected - files.keys())
        extra_keys = sorted(files.keys() - expected)
        if missing_keys:
            fail(errors, "files is missing profile keys: " + ", ".join(missing_keys))
        if extra_keys:
            fail(errors, "files has unsupported profile keys: " + ", ".join(extra_keys))
        seen: set[str] = set()
        for key, value in files.items():
            if not relative_file(value):
                fail(errors, f"files.{key} must be a relative path inside the project")
                continue
            if value in seen:
                fail(errors, f"duplicate control-file path: {value}")
            seen.add(value)
            if not (root / value).is_file():
                fail(errors, f"missing required file: {value}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {root / 'project.yaml'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
