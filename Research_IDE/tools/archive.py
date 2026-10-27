#!/usr/bin/env python3
"""Index archive metadata in library manifests; identify PDFs by bytes, never by title."""
from __future__ import annotations

import argparse
from collections import deque
import datetime
import json
import re
import sys
from pathlib import Path, PurePosixPath

import library

ROOT = Path(__file__).resolve().parents[1]
REPOS = ("Geometric-Labs", "SHD-CCP-core", "Kernel-Registry", "CubiLoom",
         "PolyShard-Agent", "Polycentric-Orchestrator", "Manifold-Projection", "FractalOS-runtime")
RELATIONS = {"related-to", "clarifies", "corrects", "supersedes"}
RELEASES = {"research-draft", "release-candidate", "official-release", "withdrawn"}
FIELDS = {"schema_version", "work_id", "revision_label", "document_date", "received_date",
          "release_status", "disposition", "review_level", "source_artifact", "source_sha256",
          "topics", "relevance", "relations", "prior_upload", "release_record"}


def records(root: Path) -> list[dict]:
    result = []
    for folder in library.paper_dirs(root):
        m = library.load_json(folder / "manifest.json")
        if "archive" in m:
            result.append({"id": m["id"], "title": m["title"],
                           "path": folder.relative_to(root).as_posix(), "archive": m["archive"]})
    return result


def safe_artifact(folder: Path, value: str) -> Path:
    if not isinstance(value, str):
        raise ValueError("artifact path must be a string")
    rel = PurePosixPath(value)
    if (not value or rel.is_absolute() or ".." in rel.parts or "\\" in value
            or rel.as_posix() != value):
        raise ValueError("unsafe artifact path")
    path = folder / value
    if not path.resolve().is_relative_to(folder.resolve()):
        raise ValueError("artifact escapes paper")
    return path


def validate(root: Path, rows: list[dict]) -> list[str]:
    errors, sources, revisions, graph = [], {}, set(), {}
    ids = {row["id"] for row in rows}
    for row in rows:
        pid, a = row["id"], row["archive"]
        folder = root / row["path"]
        try:
            if not isinstance(a, dict) or not FIELDS <= a.keys():
                raise ValueError("archive metadata lacks required fields")
            if a["schema_version"] != 1 or not re.fullmatch(r"WORK-\d{4}", a["work_id"]):
                raise ValueError("invalid archive schema/work ID")
            if a["release_status"] not in RELEASES:
                raise ValueError("unknown release status")
            if a["disposition"] not in {"retained-reference", "superseded", "withdrawn"}:
                raise ValueError("unknown disposition")
            if a["review_level"] not in {"unreviewed", "relevance-triaged", "claim-audited"}:
                raise ValueError("unknown review level")
            for date in (a["document_date"], a["received_date"]):
                if date is not None:
                    if not isinstance(date, str) or datetime.date.fromisoformat(date).isoformat() != date:
                        raise ValueError("date must be YYYY-MM-DD or null")
            if a["received_date"] is None:
                raise ValueError("received_date required")
            if a["revision_label"] is not None and not isinstance(a["revision_label"], str):
                raise ValueError("revision_label must be string or null")
            if not isinstance(a["topics"], list) or not a["topics"] or any(
                    not isinstance(t, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", t) for t in a["topics"]):
                raise ValueError("nonempty kebab-case topics required")
            source = safe_artifact(folder, a["source_artifact"])
            manifest = library.load_json(folder / "manifest.json")
            artifacts = {x["path"]: x for x in manifest["artifacts"]}
            if not a["source_artifact"].startswith("source/") or source.suffix.lower() != ".pdf":
                raise ValueError("source must be source/*.pdf")
            digest = library.sha256(source)
            tracked = artifacts.get(a["source_artifact"], {})
            if (digest != a["source_sha256"] or digest != tracked.get("sha256")
                    or source.stat().st_size != tracked.get("bytes")):
                raise ValueError("source hash/size does not match archive and manifest")
            if digest in sources:
                raise ValueError(f"duplicate PDF bytes already in {sources[digest]}; record receipt there")
            sources[digest] = pid
            revision = (a["work_id"], a["revision_label"])
            if a["revision_label"] is not None:
                if revision in revisions:
                    raise ValueError("duplicate named revision within work")
                revisions.add(revision)
            if not isinstance(a["relevance"], list) or not a["relevance"]:
                raise ValueError("at least one repository relevance required")
            mapped, primary = set(), 0
            for rel in a["relevance"]:
                if rel["repository"] not in REPOS or rel["repository"] in mapped:
                    raise ValueError("unknown or duplicate repository relevance")
                mapped.add(rel["repository"])
                if rel["role"] not in {"primary", "supporting", "context"} or not rel["reason"].strip():
                    raise ValueError("relevance role/reason required")
                primary += rel["role"] == "primary"
            if primary != 1:
                raise ValueError("exactly one primary repository required")
            graph[pid] = []
            for rel in a["relations"]:
                if rel["target"] not in ids or rel["target"] == pid or rel["kind"] not in RELATIONS:
                    raise ValueError("invalid relation target/kind")
                if not rel["evidence"].strip():
                    raise ValueError("relation evidence required")
                if rel["kind"] == "supersedes":
                    graph[pid].append(rel["target"])
            record = a["release_record"]
            if a["release_status"] in {"release-candidate", "official-release"}:
                if not isinstance(record, dict) or any(not record.get(k) for k in (
                        "version", "approved_by", "approved_date", "license", "evidence", "source_sha256")):
                    raise ValueError("release requires version, approval, license and evidence record")
                if record["source_sha256"] != digest:
                    raise ValueError("release record binds different PDF bytes")
                datetime.date.fromisoformat(record["approved_date"])
                evidence = safe_artifact(folder, record["evidence"])
                if record["evidence"] not in artifacts or not evidence.is_file():
                    raise ValueError("release evidence must be a tracked artifact")
            elif record is not None:
                raise ValueError("non-release must use null release_record")
        except (ValueError, TypeError, KeyError, OSError, AttributeError) as exc:
            errors.append(f"{pid}: {exc}")

    # Kahn traversal stays linear and avoids recursion limits for large archives.
    indegree = {pid: 0 for pid in ids}
    for targets in graph.values():
        for target in targets:
            indegree[target] += 1
    queue = deque(pid for pid, degree in indegree.items() if degree == 0)
    visited = 0
    while queue:
        pid = queue.popleft()
        visited += 1
        for target in graph.get(pid, []):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if visited != len(ids):
        errors.append("supersedes relations contain a cycle")
    return errors


def index_data(rows: list[dict]) -> dict:
    return {"schema_version": 1, "repositories": list(REPOS), "documents": rows}


def link(row: dict) -> str:
    return f"[{row['id']}](../{row['path']}/README.md)"


def render(rows: list[dict], repo: str | None = None) -> str:
    title = f"{repo} reading list" if repo else "Research archive: repository relevance"
    lines = [f"# {title}", "", "Generated by `python3 tools/archive.py index`. Relevance is triage, not implementation or proof.",
             "", "One PDF per RP ID; WORK IDs group related revisions. Unknown dates and versions remain unknown.", "",
             "| Document | Title | Primary repository | Document date | Release status |",
             "| --- | --- | --- | --- | --- |"]
    selected = [r for r in rows if repo is None or any(x["repository"] == repo for x in r["archive"]["relevance"])]
    for row in selected:
        a = row["archive"]
        primary = next(x["repository"] for x in a["relevance"] if x["role"] == "primary")
        lines.append(f"| {link(row)} | {row['title'].replace('|', '/')} | {primary} | "
                     f"{a['document_date'] or 'unknown'} | {a['release_status']} |")
    lines += ["", "## Reading notes", ""]
    for row in selected:
        lines += [f"### {row['id']}: {row['title']}", "", f"{link(row)} · {row['archive']['work_id']}", ""]
        for rel in row["archive"]["relevance"]:
            if repo is None or rel["repository"] == repo:
                lines += [f"- **{rel['repository']} ({rel['role']}):** {rel['reason']}"]
        lines.append("")
    return "\n".join(lines)


def products(rows: list[dict]) -> dict[str, str]:
    result = {"INDEX.json": json.dumps(index_data(rows), indent=2, ensure_ascii=False) + "\n",
              "INDEX.md": render(rows)}
    result.update({f"{repo}.md": render(rows, repo) for repo in REPOS})
    return result


def identify(root: Path, paths: list[Path]) -> list[dict]:
    known: dict[str, list[str]] = {}
    # Include ordinary library entries as well, so promotion cannot hide a duplicate.
    for folder in library.paper_dirs(root):
        m = library.load_json(folder / "manifest.json")
        for art in m["artifacts"]:
            if art["path"].startswith("source/") and art["path"].lower().endswith(".pdf"):
                source = safe_artifact(folder, art["path"])
                digest = library.sha256(source)
                known.setdefault(digest, []).append(m["id"])
    return [{"file": str(p), "sha256": library.sha256(p),
             "exact_matches": sorted(set(known.get(library.sha256(p), [])))} for p in paths]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    sub.add_parser("index")
    listing = sub.add_parser("list")
    listing.add_argument("--repo", choices=REPOS)
    listing.add_argument("--topic")
    listing.add_argument("--status", choices=sorted(RELEASES))
    finder = sub.add_parser("identify")
    finder.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args(argv)
    try:
        rows = records(args.root)
        errors = library.check(args.root) + validate(args.root, rows)
        if errors:
            raise ValueError("\n".join(errors))
        if args.command == "identify":
            print(json.dumps(identify(args.root, args.files), indent=2))
        elif args.command == "list":
            for r in rows:
                a = r["archive"]
                if args.repo and not any(x["repository"] == args.repo for x in a["relevance"]):
                    continue
                if args.topic and args.topic not in a["topics"]:
                    continue
                if args.status and args.status != a["release_status"]:
                    continue
                print(f"{r['id']}  {a['work_id']}  {a['release_status']}  {r['title']}")
        else:
            for name, content in products(rows).items():
                dest = args.root / "archive" / name
                if args.command == "index":
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_text(content)
                elif not dest.is_file() or dest.read_text() != content:
                    raise ValueError(f"stale archive/{name}; run archive.py index")
            print(f"OK: {len(rows)} archived documents, {len(REPOS)} repositories")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
