#!/usr/bin/env python3
"""Validate the project manifest, pinned framework contract, and control files.

The manifest uses JSON syntax saved as project.yaml. JSON is valid YAML 1.2 and
keeps this validator dependency-free. Validation resolves the pinned framework
commit from a local repository or a verified snapshot; it does not treat a
40-character string as proof that the framework revision exists.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


SHA40 = re.compile(r"^[0-9a-f]{40}$")
PLACEHOLDERS = {"replace-me", "https://github.com/owner/repository", "0" * 40}
EXPLICIT_TEMPLATE_MARKERS = (
    "<!--",
    "<stage/task>",
    "<Task>",
    "<Decision>",
    "RUN-YYYYMMDD",
    "YYYY-MM-DD",
)


class DuplicateKeyError(ValueError):
    """Raised when a JSON object repeats a key."""


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(text: str) -> object:
    return json.loads(text, object_pairs_hook=reject_duplicate_keys)


def contract_details(contract: object, source: str) -> tuple[dict[str, set[str]], str]:
    if not isinstance(contract, dict):
        raise RuntimeError(f"invalid framework contract {source}: root must be an object")
    if contract.get("schema_version") != 1 or not isinstance(contract.get("profiles"), dict):
        raise RuntimeError(f"invalid framework contract {source}: must define schema_version 1 and profiles")

    framework = contract.get("framework")
    version = framework.get("version") if isinstance(framework, dict) else None
    if not isinstance(version, str) or not version:
        raise RuntimeError(f"invalid framework contract {source}: framework.version is required")

    profiles: dict[str, set[str]] = {}
    for name, definition in contract["profiles"].items():
        keys = definition.get("required_file_keys") if isinstance(definition, dict) else None
        if not isinstance(keys, list) or not keys or not all(isinstance(key, str) and key for key in keys):
            raise RuntimeError(f"profile {name!r} must define non-empty required_file_keys")
        if len(keys) != len(set(keys)):
            raise RuntimeError(f"profile {name!r} contains duplicate required_file_keys")
        profiles[name] = set(keys)
    return profiles, version


def load_profiles() -> dict[str, set[str]]:
    """Load the contract from the current worktree for framework self-tests."""
    contract_path = Path(__file__).resolve().parents[1] / "framework.yaml"
    try:
        contract = parse_json(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise RuntimeError(f"invalid framework contract {contract_path}: {exc}") from exc
    return contract_details(contract, str(contract_path))[0]


def git_output(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "git command failed"
        raise RuntimeError(detail)
    return completed.stdout


def load_pinned_contract_from_git(repo: Path, commit: str) -> tuple[dict[str, set[str]], str, str]:
    repo = repo.resolve()
    try:
        resolved = git_output(repo, "rev-parse", "--verify", f"{commit}^{{commit}}").strip()
        if resolved != commit:
            raise RuntimeError(f"framework.commit resolved to {resolved}, expected {commit}")
        raw = git_output(repo, "show", f"{commit}:framework.yaml")
        contract = parse_json(raw)
    except (RuntimeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise RuntimeError(f"cannot resolve pinned framework commit {commit} in {repo}: {exc}") from exc
    profiles, version = contract_details(contract, f"{repo}@{commit}:framework.yaml")
    return profiles, raw, version


def load_pinned_contract_from_snapshot(snapshot: Path, repository: str, commit: str) -> tuple[dict[str, set[str]], str, str]:
    manifest_path = snapshot / "snapshot.json"
    contract_path = snapshot / "framework.yaml"
    try:
        metadata = parse_json(manifest_path.read_text(encoding="utf-8"))
        raw = contract_path.read_text(encoding="utf-8")
        contract = parse_json(raw)
    except (OSError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise RuntimeError(f"invalid framework snapshot {snapshot}: {exc}") from exc
    if not isinstance(metadata, dict):
        raise RuntimeError(f"invalid framework snapshot {snapshot}: snapshot.json root must be an object")
    if metadata.get("schema_version") != 1:
        raise RuntimeError("framework snapshot schema_version must be 1")
    expected_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    if metadata.get("repository") != repository:
        raise RuntimeError("framework snapshot repository does not match project.yaml")
    if metadata.get("commit") != commit:
        raise RuntimeError("framework snapshot commit does not match project.yaml")
    if metadata.get("framework_yaml_sha256") != expected_hash:
        raise RuntimeError("framework snapshot contract hash mismatch")
    profiles, version = contract_details(contract, str(contract_path))
    return profiles, raw, version


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def relative_file(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if "\\" in value or ":" in value or "\x00" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and path.name not in {"", "."}


def contains_unfilled_marker(text: str) -> str | None:
    for marker in EXPLICIT_TEMPLATE_MARKERS:
        if marker in text:
            return marker
    return None


def validate(root: Path, framework_repo: Path | None = None, framework_snapshot: Path | None = None) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    manifest_path = root / "project.yaml"
    if not manifest_path.is_file():
        return ["missing project.yaml"]

    try:
        data = parse_json(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, DuplicateKeyError) as exc:
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

    framework = data.get("framework")
    profiles: dict[str, set[str]] = {}
    contract_version: str | None = None
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
        else:
            try:
                if framework_snapshot is not None:
                    profiles, _, contract_version = load_pinned_contract_from_snapshot(
                        framework_snapshot.resolve(), framework.get("repository", ""), commit
                    )
                else:
                    source = (framework_repo or Path(__file__).resolve().parents[1]).resolve()
                    profiles, _, contract_version = load_pinned_contract_from_git(source, commit)
            except RuntimeError as exc:
                fail(errors, str(exc))
        if contract_version is not None and framework.get("version") != contract_version:
            fail(
                errors,
                f"framework.version {framework.get('version')!r} does not match pinned contract {contract_version!r}",
            )

    profile = data.get("profile")
    if profiles and profile not in profiles:
        fail(errors, "profile must be one of: " + ", ".join(sorted(profiles)))
    elif not isinstance(profile, str) or not profile:
        fail(errors, "profile is required")

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
            normalized = value.casefold()
            if normalized in seen:
                fail(errors, f"duplicate control-file path: {value}")
            seen.add(normalized)
            candidate = root / value
            if not candidate.is_file():
                fail(errors, f"missing required file: {value}")
                continue
            try:
                resolved = candidate.resolve(strict=True)
            except OSError as exc:
                fail(errors, f"cannot resolve required file {value}: {exc}")
                continue
            if not resolved.is_relative_to(root):
                fail(errors, f"required file escapes project root: {value}")
                continue
            try:
                marker = contains_unfilled_marker(candidate.read_text(encoding="utf-8"))
            except (OSError, UnicodeError) as exc:
                fail(errors, f"cannot read required file {value}: {exc}")
                continue
            if marker is not None:
                fail(errors, f"required file contains unfilled template marker {marker!r}: {value}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", nargs="?", default=".")
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--framework-repo",
        type=Path,
        help="local Git repository containing the pinned framework commit",
    )
    source.add_argument(
        "--framework-snapshot",
        type=Path,
        help="verified snapshot directory containing snapshot.json and framework.yaml",
    )
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    errors = validate(root, framework_repo=args.framework_repo, framework_snapshot=args.framework_snapshot)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {root / 'project.yaml'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
