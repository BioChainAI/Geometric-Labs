"""Archive integrity, revision lineage and release boundaries; no PDF dependency."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import archive
import library


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "templates", self.root / "templates")
        self.folder = library.scaffold(self.root, "example", "Example", date="2026-10-26")
        source = self.folder / "source/example.pdf"
        source.write_bytes(b"%PDF-example-fixture")
        library.track(self.root, "RP-0001", date="2026-10-26")
        self.meta = {
            "schema_version": 1, "work_id": "WORK-0001", "revision_label": None,
            "document_date": None, "received_date": "2026-10-26",
            "release_status": "research-draft", "disposition": "retained-reference",
            "review_level": "relevance-triaged", "source_artifact": "source/example.pdf",
            "source_sha256": library.sha256(source), "topics": ["memory"],
            "relevance": [{"repository": "CubiLoom", "role": "primary", "reason": "History storage."}],
            "relations": [], "prior_upload": {"status": "unknown"}, "release_record": None}
        self.write()

    def write(self):
        m = library.load_json(self.folder / "manifest.json")
        m["archive"] = self.meta
        library.dump_json(self.folder / "manifest.json", m)
        library.write_index(self.root)

    def errors(self):
        self.write()
        return archive.validate(self.root, archive.records(self.root))

    def test_unknown_dates_and_versions_remain_valid(self):
        self.assertEqual(self.errors(), [])
        self.assertIn("unknown", archive.render(archive.records(self.root)))

    def test_renamed_duplicate_identified_by_bytes_and_unknown_is_not_guessed(self):
        renamed = self.root / "renamed-release-v99.pdf"
        renamed.write_bytes((self.folder / "source/example.pdf").read_bytes())
        unknown = self.root / "example.pdf"
        unknown.write_bytes(b"different revision")
        found = archive.identify(self.root, [renamed, unknown])
        self.assertEqual(found[0]["exact_matches"], ["RP-0001"])
        self.assertEqual(found[1]["exact_matches"], [])

    def test_source_tampering_rejected_even_if_normal_manifest_rehashed(self):
        (self.folder / "source/example.pdf").write_bytes(b"changed")
        library.track(self.root, "RP-0001", update=True)
        self.assertIn("source hash/size", " ".join(self.errors()))

    def test_unknown_repo_and_multiple_primary_rejected(self):
        self.meta["relevance"][0]["repository"] = "BioChain-AI"
        self.assertIn("unknown or duplicate", " ".join(self.errors()))
        self.meta["relevance"][0]["repository"] = "CubiLoom"
        self.meta["relevance"].append({"repository": "Geometric-Labs", "role": "primary", "reason": "Tests"})
        self.assertIn("exactly one primary", " ".join(self.errors()))

    def test_unsafe_source_and_symlink_rejected(self):
        self.meta["source_artifact"] = "../outside.pdf"
        self.assertIn("unsafe artifact", " ".join(self.errors()))
        outside = self.root / "outside.pdf"
        outside.write_bytes(b"outside")
        (self.folder / "source/link.pdf").symlink_to(outside)
        self.meta["source_artifact"] = "source/link.pdf"
        self.assertIn("escapes paper", " ".join(self.errors()))

    def test_invalid_dates_and_missing_metadata_reported(self):
        self.meta["document_date"] = "2026-02-30"
        self.assertTrue(self.errors())
        del self.meta["document_date"]
        self.assertIn("lacks required", " ".join(self.errors()))

    def test_unresolved_or_self_relation_rejected(self):
        for target in ("RP-9999", "RP-0001"):
            self.meta["relations"] = [{"target": target, "kind": "supersedes", "evidence": "p. 1"}]
            self.assertIn("invalid relation", " ".join(self.errors()))

    def test_duplicate_bytes_and_supersession_cycle_rejected(self):
        rows = archive.records(self.root)
        twin = copy.deepcopy(rows[0]); twin["id"] = "RP-0002"
        self.assertIn("duplicate PDF bytes", " ".join(archive.validate(self.root, rows + [twin])))
        second = library.scaffold(self.root, "revision", "Revision", date="2026-10-26")
        (second / "source/example.pdf").write_bytes(b"%PDF-second")
        library.track(self.root, "RP-0002")
        meta = copy.deepcopy(self.meta)
        meta["source_sha256"] = library.sha256(second / "source/example.pdf")
        meta["relations"] = [{"target": "RP-0001", "kind": "supersedes", "evidence": "Editorial note p. 1"}]
        m = library.load_json(second / "manifest.json"); m["archive"] = meta
        library.dump_json(second / "manifest.json", m)
        self.meta["relations"] = [{"target": "RP-0002", "kind": "supersedes", "evidence": "Editorial note p. 1"}]
        self.assertIn("contain a cycle", " ".join(self.errors()))

    def test_official_release_requires_evidence_and_byte_binding(self):
        self.meta["release_status"] = "official-release"
        self.assertIn("release requires", " ".join(self.errors()))
        evidence = self.folder / "audits/release.md"; evidence.write_text("Review evidence fixture")
        library.track(self.root, "RP-0001")
        self.meta["release_record"] = {"version": "1.0.0", "approved_by": "Fixture reviewer",
            "approved_date": "2026-10-26", "license": "Fixture license",
            "evidence": "audits/release.md", "source_sha256": self.meta["source_sha256"]}
        self.assertEqual(self.errors(), [])
        self.meta["release_record"]["source_sha256"] = "0" * 64
        self.assertIn("different PDF bytes", " ".join(self.errors()))

    def test_generated_index_drift_and_repeatability(self):
        self.assertEqual(archive.main(["--root", str(self.root), "index"]), 0)
        before = (self.root / "archive/INDEX.json").read_bytes()
        self.assertEqual(archive.main(["--root", str(self.root), "check"]), 0)
        self.assertEqual(archive.main(["--root", str(self.root), "index"]), 0)
        self.assertEqual(before, (self.root / "archive/INDEX.json").read_bytes())
        (self.root / "archive/CubiLoom.md").write_text("stale")
        self.assertEqual(archive.main(["--root", str(self.root), "check"]), 1)


class LiveArchiveTests(unittest.TestCase):
    def test_live_archive_matches_library_and_eight_repo_manifest(self):
        rows = archive.records(ROOT)
        self.assertEqual(archive.validate(ROOT, rows), [])
        self.assertTrue(rows)
        manifest = library.load_json(ROOT.parent / "ecosystem/manifest/repositories.v1.json")
        self.assertEqual(set(archive.REPOS), {"Geometric-Labs"} | {r["name"] for r in manifest["repositories"]})
        for name, expected in archive.products(rows).items():
            self.assertEqual((ROOT / "archive" / name).read_text(), expected)
