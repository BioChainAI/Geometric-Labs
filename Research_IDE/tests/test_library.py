"""Library tool: the live tree passes, exports sort correctly, and each rule rejects a broken copy."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import json
import shutil
import tempfile
import unittest
import library

# One file per IDE export (MASTER_OPERATION_GUIDE.md section 5.2) plus the source PDF.
EXPORTS = {
    "demo_paper.md": "markdown",
    "GeometricLabs_demo_paper.lean": "lean",
    "Flowchart-Lean4-Bundle-demo_paper.json": "flowcharts",
    "Guided-Flowchart-Lean4-Walkthrough-demo_paper.md": "flowcharts",
    "Geometric_Engine_Lemma_Audit_Prompt_v2.md": "audits",
    "canonical_registry (1).json": "audits",
    "CosmoID-Ledger-demo_paper.json": "cosmo",
    "SHD-CCP-CosmoID-0123456789abcdef.png": "cosmo",
    "demo_paper.pdf": "source",
    "plot.svg": "postprocessing",
}


class TestLiveTree(unittest.TestCase):
    def test_repository_library_is_valid(self):
        self.assertEqual(library.check(ROOT), [])


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for name in ("templates", "papers", "inbox"):
            shutil.copytree(ROOT / name, self.tmp / name)
        for name in ("index.html", "ide.lock.json"):
            shutil.copy(ROOT / name, self.tmp / name)
        for stale in (self.tmp / "inbox").iterdir():
            if stale.name != "README.md":
                stale.unlink()
        library.write_index(self.tmp)
        self.paper = library.scaffold(self.tmp, "demo-paper", "Demo | paper", "core", ["demo"])
        self.pid = self.paper.name.split("_")[0]

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def drop(self, name, text="x"):
        path = self.tmp / "inbox" / name
        path.write_text(text)
        return path

    def manifest(self):
        return json.loads((self.paper / "manifest.json").read_text())

    def edit_manifest(self, **changes):
        path = self.paper / "manifest.json"
        path.write_text(json.dumps(self.manifest() | changes))
        library.write_index(self.tmp)

    def assertRejected(self, fragment):
        errors = library.check(self.tmp)
        self.assertTrue(any(fragment in e for e in errors), errors)

    def test_scaffold_is_valid_and_indexed(self):
        self.assertEqual(library.check(self.tmp), [])
        catalog = json.loads((self.tmp / "CATALOG.json").read_text())
        self.assertEqual(catalog["papers"][-1]["id"], self.pid)
        self.assertEqual(catalog["papers"][-1]["tags"], ["demo"])
        self.assertIn("Demo \\| paper", (self.tmp / "CATALOG.md").read_text())
        second = library.scaffold(self.tmp, "second", "Second")
        self.assertEqual(int(second.name[3:7]), int(self.pid[3:]) + 1)

    def test_ingest_sorts_every_ide_export(self):
        for name in EXPORTS:
            self.drop(name, '{"versions": [{"cosmo": {"hex": "ABCD"}}]}'
                      if name.startswith("CosmoID") else name)
        library.ingest(self.tmp, self.pid, [])
        for name, folder in EXPORTS.items():
            self.assertTrue((self.paper / folder / name).is_file(), name)
        self.assertEqual(sorted(p.name for p in (self.tmp / "inbox").iterdir()), ["README.md"])
        manifest = self.manifest()
        self.assertEqual(len(manifest["artifacts"]), len(EXPORTS))
        self.assertEqual(manifest["cosmo_id"], "ABCD")
        self.assertEqual(library.check(self.tmp), [])

    def test_ingest_keeps_changed_file_without_replace(self):
        library.ingest(self.tmp, self.pid, [self.drop("demo_paper.md", "v1")])
        report = library.ingest(self.tmp, self.pid, [self.drop("demo_paper.md", "v2")])
        self.assertTrue(report[0].startswith("KEEP"), report)
        self.assertTrue((self.tmp / "inbox" / "demo_paper.md").exists())
        library.ingest(self.tmp, self.pid, [], replace=True)
        self.assertEqual((self.paper / "markdown" / "demo_paper.md").read_text(), "v2")
        self.assertEqual(library.check(self.tmp), [])

    def test_ingest_to_overrides_folder(self):
        library.ingest(self.tmp, self.pid, [self.drop("run.md")], folder="workflows")
        self.assertTrue((self.paper / "workflows" / "run.md").is_file())

    def test_notes_sorted_by_name(self):
        library.ingest(self.tmp, self.pid, [self.drop("2026-10-23_audit-notes.md"),
                                            self.drop("agent-workflow.json")])
        self.assertTrue((self.paper / "audits" / "2026-10-23_audit-notes.md").is_file())
        self.assertTrue((self.paper / "workflows" / "agent-workflow.json").is_file())

    def test_refile_inside_paper_moves_record(self):
        library.ingest(self.tmp, self.pid, [self.drop("notes.md")])
        library.ingest(self.tmp, self.pid, [self.paper / "markdown" / "notes.md"], folder="audits")
        self.assertFalse((self.paper / "markdown" / "notes.md").exists())
        self.assertEqual([a["path"] for a in self.manifest()["artifacts"]], ["audits/notes.md"])
        self.assertEqual(library.check(self.tmp), [])

    def test_tampered_artifact_rejected_then_track_update(self):
        library.ingest(self.tmp, self.pid, [self.drop("demo_paper.md")])
        (self.paper / "markdown" / "demo_paper.md").write_text("edited")
        self.assertRejected("changed since it was recorded")
        library.track(self.tmp, self.pid, update=True)
        self.assertEqual(library.check(self.tmp), [])

    def test_untracked_file_rejected_then_tracked(self):
        (self.paper / "audits" / "notes.md").write_text("notes")
        self.assertRejected("untracked file audits/notes.md")
        library.track(self.tmp, self.pid)
        self.assertEqual(library.check(self.tmp), [])

    def test_stage_needs_evidence(self):
        self.edit_manifest(stage="audited")
        self.assertRejected("needs at least one markdown/ artifact")
        self.assertRejected("needs at least one audits/ artifact")

    def test_sorry_blocks_sorry_free(self):
        lean = "theorem t : 1 = 1 := by\n  sorry -- placeholder\n"
        library.ingest(self.tmp, self.pid, [self.drop("GeometricLabs_demo.lean", lean)])
        self.edit_manifest(lean_status="sorry-free")
        self.assertRejected("still contains 'sorry'")

    def test_sorry_in_comments_is_ignored(self):
        lean = "-- no sorry here\n/- sorry -/\ntheorem t : 1 = 1 := by rfl\n"
        library.ingest(self.tmp, self.pid, [self.drop("GeometricLabs_demo.lean", lean)])
        self.edit_manifest(lean_status="sorry-free")
        self.assertEqual(library.check(self.tmp), [])

    def test_lake_verified_needs_record(self):
        library.ingest(self.tmp, self.pid, [self.drop("GeometricLabs_demo.lean", "-- ok\n")])
        self.edit_manifest(lean_status="lake-verified")
        self.assertRejected("lake-verified needs lean_verification")

    def test_stale_catalog_rejected(self):
        (self.paper / "manifest.json").write_text(
            json.dumps(self.manifest() | {"title": "Renamed"}))
        self.assertRejected("CATALOG.json is stale")

    def test_ide_lock_mismatch_rejected(self):
        with (self.tmp / "index.html").open("a") as handle:
            handle.write("<!-- edit -->")
        self.assertRejected("does not match ide.lock.json")

    def test_bad_folder_name_rejected(self):
        self.paper.rename(self.paper.with_name(f"{self.pid}_wrong"))
        library.write_index(self.tmp)
        self.assertRejected("folder must be named")


if __name__ == "__main__":
    unittest.main()
