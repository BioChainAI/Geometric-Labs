#!/usr/bin/env python3
"""Cryptographic_Research registry: validate items, list them, scaffold new ones.

    python3 tools/registry.py check
    python3 tools/registry.py list
    python3 tools/registry.py new --slug merkle-signature --title "Merkle signatures"

``check`` enforces VERSIONING.md: unique sequential IDs, folder names, stage
and status agreement, semantic versions, a CHANGELOG section for the current
version, a research log, a pinned 40-hex upstream commit and no unregistered
item folders. Standard library only.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = "REGISTRY.json"
TEMPLATE = Path("templates") / "experiment"
STAGES = {
    "experimental": {"[OPEN]", "[HEURISTIC]", "[COMPUTED]"},
    "published": {"[COMPUTED]", "[PROVEN]"},
    "archived": {"[FAILED]", "[SUPERSEDED]"},
}
ID_RE = re.compile(r"^CR-(\d{4})$")
SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MANIFEST_KEYS = ("schema_version", "id", "slug", "title", "stage", "status",
                 "version", "created", "updated")
MIRRORED_KEYS = ("stage", "status", "version")


def load_json(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def check_item(root: Path, entry: dict) -> list[str]:
    errors = []
    item_id = entry.get("id", "?")
    where = f"{item_id}:"
    path = root / entry.get("path", "")
    if not path.is_dir():
        return [f"{where} folder {entry.get('path')!r} missing"]
    manifest_path = path / "manifest.json"
    if not manifest_path.is_file():
        return [f"{where} manifest.json missing"]
    manifest = load_json(manifest_path)
    errors += [f"{where} manifest lacks {key!r}" for key in MANIFEST_KEYS if key not in manifest]
    if errors:
        return errors

    if manifest["id"] != item_id:
        errors.append(f"{where} manifest id is {manifest['id']}")
    stage, status, version, slug = (manifest[k] for k in ("stage", "status", "version", "slug"))
    if not SLUG_RE.match(slug):
        errors.append(f"{where} slug {slug!r} is not kebab-case")
    if path.name != f"{item_id}_{slug}":
        errors.append(f"{where} folder must be named {item_id}_{slug}")
    if path.parent.name != stage:
        errors.append(f"{where} stage {stage!r} but folder is under {path.parent.name}/")
    if stage not in STAGES:
        errors.append(f"{where} unknown stage {stage!r}")
    elif status not in STAGES[stage]:
        errors.append(f"{where} status {status} not allowed in {stage}")
    if not SEMVER_RE.match(version):
        errors.append(f"{where} version {version!r} is not semver")
    elif stage == "published" and version.startswith("0."):
        errors.append(f"{where} published items must be >= 1.0.0")
    for key in ("created", "updated"):
        if not DATE_RE.match(str(manifest[key])):
            errors.append(f"{where} {key} must be YYYY-MM-DD")
    for key in MIRRORED_KEYS:
        if entry.get(key) != manifest[key]:
            errors.append(f"{where} REGISTRY {key}={entry.get(key)!r} != manifest {manifest[key]!r}")

    changelog = path / "CHANGELOG.md"
    if not changelog.is_file():
        errors.append(f"{where} CHANGELOG.md missing")
    elif f"## [{version}]" not in changelog.read_text():
        errors.append(f"{where} CHANGELOG.md has no section for {version}")
    if not (path / "RESEARCH_LOG.md").is_file():
        errors.append(f"{where} RESEARCH_LOG.md missing")
    if not (path / "README.md").is_file():
        errors.append(f"{where} README.md missing")

    upstream = manifest.get("upstream")
    if upstream:
        if not COMMIT_RE.match(str(upstream.get("commit", ""))):
            errors.append(f"{where} upstream commit must be a full 40-hex SHA")
        if not upstream.get("license"):
            errors.append(f"{where} upstream license must be recorded (use 'none declared')")
    return errors


def check(root: Path) -> list[str]:
    registry = load_json(root / REGISTRY)
    items = registry.get("items", [])
    errors = []
    numbers = []
    for entry in items:
        match = ID_RE.match(str(entry.get("id", "")))
        if not match:
            errors.append(f"bad id {entry.get('id')!r}")
            continue
        numbers.append(int(match.group(1)))
        errors += check_item(root, entry)
    if len(numbers) != len(set(numbers)):
        errors.append("duplicate research ids")
    if numbers != sorted(numbers):
        errors.append("REGISTRY items must be in id order")
    expected_next = f"CR-{max(numbers, default=0) + 1:04d}"
    if registry.get("next_id") != expected_next:
        errors.append(f"next_id must be {expected_next}")
    registered = {(root / e.get("path", "")).resolve() for e in items}
    for stage in STAGES:
        for folder in sorted((root / stage).glob("CR-*")):
            if folder.is_dir() and folder.resolve() not in registered:
                errors.append(f"unregistered item folder {stage}/{folder.name}")
    return errors


def scaffold(root: Path, slug: str, title: str, today: str | None = None) -> Path:
    if not SLUG_RE.match(slug):
        raise ValueError("slug must be kebab-case, e.g. merkle-signature")
    registry_path = root / REGISTRY
    registry = load_json(registry_path)
    item_id = registry["next_id"]
    target = root / "experimental" / f"{item_id}_{slug}"
    if target.exists():
        raise FileExistsError(target)
    today = today or datetime.date.today().isoformat()
    values = {"{{ID}}": item_id, "{{SLUG}}": slug, "{{TITLE}}": title, "{{DATE}}": today,
              "{{PACKAGE}}": slug.replace("-", "_")}
    for source in sorted((root / TEMPLATE).rglob("*")):
        relative = source.relative_to(root / TEMPLATE)
        destination = target / Path(*(values.get(p, p) for p in relative.parts))
        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue
        text = source.read_text()
        for key, value in values.items():
            text = text.replace(key, value)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text)
    registry["items"].append({"id": item_id, "path": f"experimental/{target.name}",
                              "stage": "experimental", "status": "[OPEN]", "version": "0.0.1"})
    registry["next_id"] = f"CR-{int(item_id[3:]) + 1:04d}"
    registry_path.write_text(json.dumps(registry, indent=1) + "\n")
    return target


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="validate registry and every item")
    commands.add_parser("list", help="print the registry")
    new = commands.add_parser("new", help="scaffold a new experimental item")
    new.add_argument("--slug", required=True)
    new.add_argument("--title", required=True)
    args = parser.parse_args(argv)

    if args.command == "check":
        errors = check(args.root)
        for error in errors:
            print(f"ERROR {error}")
        count = len(load_json(args.root / REGISTRY)["items"])
        print(f"{'FAILED' if errors else 'OK'}: {count} research item(s), {len(errors)} error(s)")
        return 1 if errors else 0
    if args.command == "list":
        for entry in load_json(args.root / REGISTRY)["items"]:
            print(f"{entry['id']}  {entry['stage']:<12} {entry['status']:<12} "
                  f"v{entry['version']:<8} {entry['path']}")
        return 0
    target = scaffold(args.root, args.slug, args.title)
    print(f"Created {target.relative_to(args.root)}; edit its manifest and README, then run check.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
