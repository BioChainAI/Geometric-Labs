"""Registry tool: the live tree passes, and each rule rejects a broken copy."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import json
import shutil
import tempfile
import unittest
import registry


class TestLiveTree(unittest.TestCase):
    def test_repository_registry_is_valid(self):
        self.assertEqual(registry.check(ROOT), [])


class TestRules(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for name in ("REGISTRY.json", "templates", "experimental", "published"):
            source = ROOT / name
            if source.is_dir():
                shutil.copytree(source, self.tmp / name)
            else:
                shutil.copy(source, self.tmp / name)
        self.item = self.tmp / "experimental" / "CR-0001_lamport-otp"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def edit_manifest(self, **changes):
        path = self.item / "manifest.json"
        data = json.loads(path.read_text()) | changes
        path.write_text(json.dumps(data))

    def assertRejected(self, fragment):
        errors = registry.check(self.tmp)
        self.assertTrue(any(fragment in e for e in errors), errors)

    def test_copy_is_valid(self):
        self.assertEqual(registry.check(self.tmp), [])

    def test_version_drift_between_registry_and_manifest(self):
        self.edit_manifest(version="0.2.0")
        self.assertRejected("REGISTRY version")

    def test_changelog_must_cover_version(self):
        (self.item / "CHANGELOG.md").write_text("# Changelog\n")
        self.assertRejected("no section for 0.1.0")

    def test_status_must_fit_stage(self):
        self.edit_manifest(status="[PROVEN]")
        self.assertRejected("not allowed in experimental")

    def test_upstream_must_be_pinned(self):
        manifest = json.loads((self.item / "manifest.json").read_text())
        manifest["upstream"]["commit"] = "main"
        (self.item / "manifest.json").write_text(json.dumps(manifest))
        self.assertRejected("40-hex")

    def test_unregistered_folder(self):
        (self.tmp / "experimental" / "CR-0099_stray").mkdir()
        self.assertRejected("unregistered item folder")

    def test_research_log_required(self):
        (self.item / "RESEARCH_LOG.md").unlink()
        self.assertRejected("RESEARCH_LOG.md missing")

    def test_scaffold_produces_a_valid_item(self):
        target = registry.scaffold(self.tmp, "merkle-signature", "Merkle signatures", "2026-10-19")
        self.assertEqual(target.name, "CR-0002_merkle-signature")
        self.assertEqual(registry.check(self.tmp), [])
        manifest = json.loads((target / "manifest.json").read_text())
        self.assertEqual((manifest["id"], manifest["status"]), ("CR-0002", "[OPEN]"))
        self.assertTrue((target / "src" / "merkle_signature" / "__init__.py").is_file())
        self.assertNotIn("{{", (target / "README.md").read_text())
        with self.assertRaises(ValueError):
            registry.scaffold(self.tmp, "Bad Slug", "x")


if __name__ == "__main__":
    unittest.main()
