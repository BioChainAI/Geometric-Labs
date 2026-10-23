#!/usr/bin/env python3
"""Research_IDE paper library: scaffold papers, sort IDE exports, validate the catalog.

    python3 tools/library.py new --slug fifteen-lemmas --title "The Fifteen Lemmas" --tier core
    python3 tools/library.py ingest RP-0001                 # sort everything in inbox/
    python3 tools/library.py ingest RP-0001 notes.md --to workflows
    python3 tools/library.py track RP-0001 [--update]       # record hand-made files
    python3 tools/library.py set RP-0001 --stage audited --lean-status draft
    python3 tools/library.py list [--stage S] [--tag T] [--lean-status L] [--tier T]
    python3 tools/library.py index                          # rebuild CATALOG.json/.md
    python3 tools/library.py check
    python3 tools/library.py lock-ide                       # after replacing index.html

Each paper's ``manifest.json`` is the source of truth. ``CATALOG.json`` and
``CATALOG.md`` are generated from the manifests; ``check`` fails when they are
stale, when an artifact's SHA-256 no longer matches, when a file sits in a paper
folder untracked, when a stage lacks its evidence, or when a Lean status is
claimed for files that still contain ``sorry``. Standard library only.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = "papers"
INBOX = "inbox"
TEMPLATE = Path("templates") / "paper"
CATALOG_JSON = "CATALOG.json"
CATALOG_MD = "CATALOG.md"
IDE_FILE = "index.html"
IDE_LOCK = "ide.lock.json"

FOLDERS = ("source", "markdown", "audits", "lean", "flowcharts", "cosmo", "workflows",
           "postprocessing")
# Ordered: each stage needs the evidence of every stage before it.
STAGES = ("intake", "transcribed", "audited", "formalized", "verified")
STAGE_EVIDENCE = {"transcribed": "markdown", "audited": "audits", "formalized": "lean"}
ALL_STAGES = STAGES + ("archived",)
LEAN_STATUSES = ("none", "draft", "sorry-free", "lake-verified")
TIERS = ("core", "series", "external")
ID_RE = re.compile(r"^RP-(\d{4})$")
SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MANIFEST_KEYS = ("schema_version", "id", "slug", "title", "tier", "stage", "lean_status",
                 "tags", "created", "updated", "artifacts")
VERIFICATION_KEYS = ("toolchain", "command", "date", "by")
MAX_BYTES = 95 * 1024 * 1024  # GitHub rejects files over 100 MiB

# (filename regex, folder, kind) in priority order; first match wins.
EXPORT_RULES = (
    (r"^Flowchart-Lean4-Bundle-.*\.json$", "flowcharts", "flowchart-bundle"),
    (r"^Guided-Flowchart-Lean4-Walkthrough-.*\.md$", "flowcharts", "flowchart-walkthrough"),
    (r"^Geometric_Engine_Lemma_Audit_Prompt_v2.*\.md$", "audits", "audit-prompt"),
    (r"^canonical_registry.*\.json$", "audits", "canonical-registry"),
    (r"^CosmoID-Ledger-.*\.json$", "cosmo", "cosmo-ledger"),
    (r"^SHD-CCP-CosmoID-.*\.png$", "cosmo", "cosmo-sigil"),
    (r"audit.*\.(md|markdown|txt)$", "audits", "audit-notes"),
    (r"workflow.*\.(md|markdown|txt|json|ya?ml)$", "workflows", "workflow"),
    (r"\.lean$", "lean", "lean-module"),
    (r"\.pdf$", "source", "source-pdf"),
    (r"\.(tex|txt)$", "source", "source-text"),
    (r"\.(md|markdown)$", "markdown", "transcription"),
)


def today() -> str:
    return datetime.date.today().isoformat()


def load_json(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def dump_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def classify(name: str, folder: str | None = None) -> tuple[str, str]:
    for pattern, rule_folder, kind in EXPORT_RULES:
        if re.search(pattern, name, re.IGNORECASE):
            if folder is None or folder == rule_folder:
                return rule_folder, kind
            break
    return (folder, "other") if folder else ("postprocessing", "other")


def normalize_id(text: str) -> str:
    digits = text.upper().removeprefix("RP-").split("_")[0]
    if not digits.isdigit():
        raise ValueError(f"not a paper id: {text!r} (expected RP-0001)")
    return f"RP-{int(digits):04d}"


def paper_dirs(root: Path) -> list[Path]:
    return sorted(p for p in (root / PAPERS).glob("RP-*") if p.is_dir())


def find_paper(root: Path, paper_id: str) -> Path:
    paper_id = normalize_id(paper_id)
    matches = [p for p in paper_dirs(root) if p.name.split("_")[0] == paper_id]
    if not matches:
        raise FileNotFoundError(f"{paper_id} not found under {PAPERS}/")
    return matches[0]


def lean_has_sorry(path: Path) -> bool:
    text = re.sub(r"/-.*?-/", "", path.read_text(errors="replace"), flags=re.S)
    text = re.sub(r"--[^\n]*", "", text)
    return re.search(r"\bsorry\b", text) is not None


# --------------------------------------------------------------------------- check

def check_paper(path: Path) -> list[str]:
    where = f"{path.name}:"
    manifest_path = path / "manifest.json"
    if not manifest_path.is_file():
        return [f"{where} manifest.json missing"]
    manifest = load_json(manifest_path)
    errors = [f"{where} manifest lacks {key!r}" for key in MANIFEST_KEYS if key not in manifest]
    if errors:
        return errors

    paper_id, slug = manifest["id"], manifest["slug"]
    if not ID_RE.match(paper_id):
        errors.append(f"{where} bad id {paper_id!r}")
    if not SLUG_RE.match(slug):
        errors.append(f"{where} slug {slug!r} is not kebab-case")
    if path.name != f"{paper_id}_{slug}":
        errors.append(f"{where} folder must be named {paper_id}_{slug}")
    if manifest["tier"] not in TIERS:
        errors.append(f"{where} tier must be one of {', '.join(TIERS)}")
    if manifest["stage"] not in ALL_STAGES:
        errors.append(f"{where} unknown stage {manifest['stage']!r}")
    if manifest["lean_status"] not in LEAN_STATUSES:
        errors.append(f"{where} unknown lean_status {manifest['lean_status']!r}")
    for key in ("created", "updated"):
        if not DATE_RE.match(str(manifest[key])):
            errors.append(f"{where} {key} must be YYYY-MM-DD")
    for name in ("README.md", "RESEARCH_LOG.md"):
        if not (path / name).is_file():
            errors.append(f"{where} {name} missing")

    tracked = set()
    for artifact in manifest["artifacts"]:
        rel = artifact.get("path", "")
        tracked.add(rel)
        file = path / rel
        if rel.split("/")[0] not in FOLDERS:
            errors.append(f"{where} artifact {rel!r} is outside the artifact folders")
        elif not file.is_file():
            errors.append(f"{where} artifact {rel} missing")
        elif sha256(file) != artifact.get("sha256"):
            errors.append(f"{where} {rel} changed since it was recorded "
                          f"(re-ingest with --replace or run track --update)")
        elif file.stat().st_size > MAX_BYTES:
            errors.append(f"{where} {rel} exceeds 95 MiB; store it with Git LFS or link it")
    if len(tracked) != len(manifest["artifacts"]):
        errors.append(f"{where} duplicate artifact paths")
    for folder in FOLDERS:
        for file in sorted((path / folder).rglob("*")):
            rel = file.relative_to(path).as_posix()
            if file.is_file() and file.name != ".gitkeep" and rel not in tracked:
                errors.append(f"{where} untracked file {rel} (run track {paper_id})")

    kinds = {a.get("path", "").split("/")[0] for a in manifest["artifacts"]}
    stage = manifest["stage"]
    if stage in STAGES:
        for needed_stage, folder in STAGE_EVIDENCE.items():
            if STAGES.index(stage) >= STAGES.index(needed_stage) and folder not in kinds:
                errors.append(f"{where} stage {stage!r} needs at least one {folder}/ artifact")
        if stage == "verified" and manifest["lean_status"] != "lake-verified":
            errors.append(f"{where} stage 'verified' needs lean_status 'lake-verified'")

    lean_status = manifest["lean_status"]
    lean_files = [path / a["path"] for a in manifest["artifacts"]
                  if a.get("path", "").endswith(".lean") and (path / a["path"]).is_file()]
    if lean_status != "none" and not lean_files:
        errors.append(f"{where} lean_status {lean_status!r} needs a lean/*.lean artifact")
    if lean_status in ("sorry-free", "lake-verified"):
        for file in lean_files:
            if lean_has_sorry(file):
                errors.append(f"{where} {file.relative_to(path).as_posix()} still contains "
                              f"'sorry' but lean_status is {lean_status!r}")
    if lean_status == "lake-verified":
        record = manifest.get("lean_verification") or {}
        missing = [k for k in VERIFICATION_KEYS if not record.get(k)]
        if missing:
            errors.append(f"{where} lake-verified needs lean_verification "
                          f"{', '.join(missing)}")
    return errors


def check(root: Path) -> list[str]:
    errors = []
    ids = []
    for path in paper_dirs(root):
        errors += check_paper(path)
        match = ID_RE.match(path.name.split("_")[0])
        if match:
            ids.append(match.group(1))
    if len(ids) != len(set(ids)):
        errors.append("duplicate paper ids")
    if (root / CATALOG_JSON).is_file() and (root / CATALOG_MD).is_file():
        catalog = build_catalog(root)
        if load_json(root / CATALOG_JSON) != catalog:
            errors.append(f"{CATALOG_JSON} is stale (run index)")
        if (root / CATALOG_MD).read_text() != render_catalog_md(catalog):
            errors.append(f"{CATALOG_MD} is stale (run index)")
    else:
        errors.append(f"{CATALOG_JSON}/{CATALOG_MD} missing (run index)")
    lock_path = root / IDE_LOCK
    if (root / IDE_FILE).is_file():
        if not lock_path.is_file():
            errors.append(f"{IDE_LOCK} missing (run lock-ide)")
        elif load_json(lock_path).get("sha256") != sha256(root / IDE_FILE):
            errors.append(f"{IDE_FILE} does not match {IDE_LOCK} (run lock-ide and "
                          f"record the new IDE version in CHANGELOG.md)")
    return errors


# --------------------------------------------------------------------------- catalog

def build_catalog(root: Path) -> dict:
    papers = []
    numbers = [0]
    for path in paper_dirs(root):
        manifest_path = path / "manifest.json"
        if not manifest_path.is_file():
            continue
        manifest = load_json(manifest_path)
        counts: dict[str, int] = {}
        for artifact in manifest.get("artifacts", []):
            folder = artifact.get("path", "").split("/")[0]
            counts[folder] = counts.get(folder, 0) + 1
        match = ID_RE.match(str(manifest.get("id", "")))
        if match:
            numbers.append(int(match.group(1)))
        papers.append({
            "id": manifest.get("id"),
            "title": manifest.get("title"),
            "path": f"{PAPERS}/{path.name}",
            "tier": manifest.get("tier"),
            "stage": manifest.get("stage"),
            "lean_status": manifest.get("lean_status"),
            "tags": manifest.get("tags", []),
            "cosmo_id": manifest.get("cosmo_id", ""),
            "updated": manifest.get("updated"),
            "artifacts": dict(sorted(counts.items())),
        })
    return {"schema_version": 1, "next_id": f"RP-{max(numbers) + 1:04d}", "papers": papers}


def render_catalog_md(catalog: dict) -> str:
    lines = ["# Research paper catalog", "",
             "Generated by `make index` from each paper's `manifest.json`. Do not edit by hand.",
             ""]
    papers = catalog["papers"]
    if not papers:
        lines += ["No papers yet. Start one with "
                  "`make new SLUG=<kebab-case> TITLE=\"<title>\"`.", ""]
    else:
        stages = {s: sum(p["stage"] == s for p in papers) for s in ALL_STAGES}
        lines += ["| " + " | ".join(ALL_STAGES) + " |",
                  "|" + " :---: |" * len(ALL_STAGES),
                  "| " + " | ".join(str(stages[s]) for s in ALL_STAGES) + " |", "",
                  "| ID | Title | Tier | Stage | Lean | Artifacts | Tags | Updated |",
                  "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"]
        for p in papers:
            counts = ", ".join(f"{k} {v}" for k, v in p["artifacts"].items()) or "-"
            title = str(p["title"]).replace("|", "\\|")
            lines.append(f"| [{p['id']}]({p['path']}/) | {title} | {p['tier']} | "
                         f"{p['stage']} | {p['lean_status']} | {counts} | "
                         f"{', '.join(p['tags']) or '-'} | {p['updated']} |")
        lines.append("")
    lines.append(f"Next ID: `{catalog['next_id']}`")
    return "\n".join(lines) + "\n"


def write_index(root: Path) -> dict:
    catalog = build_catalog(root)
    dump_json(root / CATALOG_JSON, catalog)
    (root / CATALOG_MD).write_text(render_catalog_md(catalog))
    return catalog


# --------------------------------------------------------------------------- commands

def scaffold(root: Path, slug: str, title: str, tier: str = "external",
             tags: list[str] | None = None, date: str | None = None) -> Path:
    if not SLUG_RE.match(slug):
        raise ValueError("slug must be kebab-case, e.g. fifteen-lemmas")
    if tier not in TIERS:
        raise ValueError(f"tier must be one of {', '.join(TIERS)}")
    paper_id = build_catalog(root)["next_id"]
    target = root / PAPERS / f"{paper_id}_{slug}"
    if target.exists():
        raise FileExistsError(target)
    date = date or today()
    values = {"{{ID}}": paper_id, "{{SLUG}}": slug, "{{TITLE}}": title, "{{DATE}}": date,
              "{{TIER}}": tier}
    for source in sorted((root / TEMPLATE).rglob("*")):
        destination = target / source.relative_to(root / TEMPLATE)
        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue
        text = source.read_text()
        for key, value in values.items():
            text = text.replace(key, json.dumps(value)[1:-1] if source.suffix == ".json"
                                else value)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text)
    for folder in FOLDERS:
        (target / folder).mkdir(exist_ok=True)
        (target / folder / ".gitkeep").touch()
    manifest = load_json(target / "manifest.json")
    manifest["tags"] = sorted(set(tags or []))
    dump_json(target / "manifest.json", manifest)
    write_index(root)
    return target


def record(manifest: dict, rel: str, kind: str, file: Path, date: str) -> None:
    entry = {"path": rel, "kind": kind, "sha256": sha256(file),
             "bytes": file.stat().st_size, "added": date}
    artifacts = [a for a in manifest["artifacts"] if a["path"] != rel]
    manifest["artifacts"] = sorted(artifacts + [entry], key=lambda a: a["path"])


def latest_cosmo_id(ledger: Path) -> str:
    try:
        versions = load_json(ledger).get("versions") or []
        return str((versions[0].get("cosmo") or {}).get("hex", "")) if versions else ""
    except (ValueError, AttributeError, OSError):
        return ""


def ingest(root: Path, paper_id: str, files: list[Path], folder: str | None = None,
           replace: bool = False, date: str | None = None) -> list[str]:
    """Copy each file into the paper, removing it from inbox/ once recorded.

    A file already inside the paper is moved, so ``--to`` can re-file it.
    """
    if folder is not None and folder not in FOLDERS:
        raise ValueError(f"--to must be one of {', '.join(FOLDERS)}")
    paper = find_paper(root, paper_id)
    manifest = load_json(paper / "manifest.json")
    inbox = (root / INBOX).resolve()
    paper_root = paper.resolve()
    date = date or today()
    report = []
    if not files:
        files = sorted(p for p in inbox.iterdir() if p.is_file() and p.name != "README.md")
    for file in files:
        file = file.resolve()
        if not file.is_file():
            report.append(f"SKIP {file}: not a file")
            continue
        dest_folder, kind = classify(file.name, folder)
        dest = paper / dest_folder / file.name
        rel = dest.relative_to(paper).as_posix()
        if dest.exists() and sha256(dest) == sha256(file):
            report.append(f"SAME {rel}")
        elif dest.exists() and not replace:
            report.append(f"KEEP {rel}: a different file already exists (use --replace)")
            continue
        else:
            report.append(f"{'REPL' if dest.exists() else 'ADD '} {rel}  [{kind}]")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, dest)
        record(manifest, rel, kind, dest, date)
        if kind == "cosmo-ledger":
            manifest["cosmo_id"] = latest_cosmo_id(dest) or manifest.get("cosmo_id", "")
        if file != dest.resolve() and (file.parent == inbox or paper_root in file.parents):
            old = file.relative_to(paper_root).as_posix() if paper_root in file.parents else None
            manifest["artifacts"] = [a for a in manifest["artifacts"] if a["path"] != old]
            file.unlink()
    manifest["updated"] = date
    dump_json(paper / "manifest.json", manifest)
    write_index(root)
    return report


def track(root: Path, paper_id: str, update: bool = False, date: str | None = None) -> list[str]:
    paper = find_paper(root, paper_id)
    manifest = load_json(paper / "manifest.json")
    known = {a["path"]: a for a in manifest["artifacts"]}
    date = date or today()
    report = []
    for folder in FOLDERS:
        for file in sorted((paper / folder).rglob("*")):
            rel = file.relative_to(paper).as_posix()
            if not file.is_file() or file.name == ".gitkeep":
                continue
            if rel not in known:
                kind = classify(file.name, folder)[1]
                record(manifest, rel, kind, file, date)
                report.append(f"ADD  {rel}  [{kind}]")
            elif update and known[rel]["sha256"] != sha256(file):
                record(manifest, rel, known[rel]["kind"], file, date)
                report.append(f"UPD  {rel}")
    if report:
        manifest["updated"] = date
        dump_json(paper / "manifest.json", manifest)
        write_index(root)
    return report


def set_fields(root: Path, paper_id: str, stage: str | None = None,
               lean_status: str | None = None, tags: list[str] | None = None,
               verification: dict | None = None, date: str | None = None) -> dict:
    paper = find_paper(root, paper_id)
    manifest = load_json(paper / "manifest.json")
    if stage is not None:
        manifest["stage"] = stage
    if lean_status is not None:
        manifest["lean_status"] = lean_status
    if tags:
        manifest["tags"] = sorted(set(manifest["tags"]) | set(tags))
    if verification:
        manifest["lean_verification"] = verification
    manifest["updated"] = date or today()
    dump_json(paper / "manifest.json", manifest)
    write_index(root)
    return manifest


def lock_ide(root: Path) -> dict:
    lock_path = root / IDE_LOCK
    lock = load_json(lock_path) if lock_path.is_file() else {}
    lock.update({"file": IDE_FILE, "sha256": sha256(root / IDE_FILE),
                 "bytes": (root / IDE_FILE).stat().st_size, "locked": today()})
    dump_json(lock_path, lock)
    return lock


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="validate every paper, the catalog and the IDE lock")
    commands.add_parser("index", help="rebuild CATALOG.json and CATALOG.md")
    commands.add_parser("lock-ide", help="record the SHA-256 of index.html")
    listing = commands.add_parser("list", help="print papers, optionally filtered")
    listing.add_argument("--stage", choices=ALL_STAGES)
    listing.add_argument("--lean-status", choices=LEAN_STATUSES)
    listing.add_argument("--tier", choices=TIERS)
    listing.add_argument("--tag")
    new = commands.add_parser("new", help="scaffold a new paper")
    new.add_argument("--slug", required=True)
    new.add_argument("--title", required=True)
    new.add_argument("--tier", choices=TIERS, default="external")
    new.add_argument("--tag", action="append", default=[])
    take = commands.add_parser("ingest", help="sort IDE exports into a paper")
    take.add_argument("paper")
    take.add_argument("files", nargs="*", type=Path, help="default: every file in inbox/")
    take.add_argument("--to", choices=FOLDERS, help="force the destination folder")
    take.add_argument("--replace", action="store_true", help="overwrite a changed file")
    tracker = commands.add_parser("track", help="record files placed in a paper by hand")
    tracker.add_argument("paper")
    tracker.add_argument("--update", action="store_true", help="re-hash edited files")
    setter = commands.add_parser("set", help="update stage, Lean status or tags")
    setter.add_argument("paper")
    setter.add_argument("--stage", choices=ALL_STAGES)
    setter.add_argument("--lean-status", choices=LEAN_STATUSES)
    setter.add_argument("--tag", action="append", default=[])
    setter.add_argument("--toolchain", help="with lake-verified: e.g. leanprover/lean4:v4.12.0")
    setter.add_argument("--command", dest="lean_command", help="with lake-verified: command run")
    setter.add_argument("--by", help="with lake-verified: who ran it")
    args = parser.parse_args(argv)
    root = args.root

    try:
        if args.command == "check":
            errors = check(root)
            for error in errors:
                print(f"ERROR {error}")
            count = len(paper_dirs(root))
            print(f"{'FAILED' if errors else 'OK'}: {count} paper(s), {len(errors)} error(s)")
            return 1 if errors else 0
        if args.command == "index":
            catalog = write_index(root)
            print(f"Indexed {len(catalog['papers'])} paper(s); next id {catalog['next_id']}")
        elif args.command == "lock-ide":
            lock = lock_ide(root)
            print(f"Locked {IDE_FILE} sha256={lock['sha256']}")
        elif args.command == "list":
            for p in build_catalog(root)["papers"]:
                if ((args.stage and p["stage"] != args.stage)
                        or (args.lean_status and p["lean_status"] != args.lean_status)
                        or (args.tier and p["tier"] != args.tier)
                        or (args.tag and args.tag not in p["tags"])):
                    continue
                print(f"{p['id']}  {p['tier']:<8} {p['stage']:<12} {p['lean_status']:<13} "
                      f"{p['title']}")
        elif args.command == "new":
            target = scaffold(root, args.slug, args.title, args.tier, args.tag)
            print(f"Created {target.relative_to(root)}; fill in its manifest source and README.")
        elif args.command == "ingest":
            for line in ingest(root, args.paper, args.files, args.to, args.replace):
                print(line)
        elif args.command == "track":
            print("\n".join(track(root, args.paper, args.update)) or "Nothing new to track.")
        elif args.command == "set":
            verification = None
            if args.lean_status == "lake-verified":
                verification = {"toolchain": args.toolchain, "command": args.lean_command,
                                "date": today(), "by": args.by}
            manifest = set_fields(root, args.paper, args.stage, args.lean_status, args.tag,
                                  verification)
            print(f"{manifest['id']}: stage={manifest['stage']} "
                  f"lean_status={manifest['lean_status']} tags={manifest['tags']}")
            problems = check_paper(find_paper(root, args.paper))
            for problem in problems:
                print(f"WARNING {problem}")
            return 1 if problems else 0
    except (ValueError, FileNotFoundError, FileExistsError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
