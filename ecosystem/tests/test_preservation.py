"""Navigation may evolve; scientific fixtures and unknown paths stay protected."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE/'tools'))
from preservation import MUTABLE_DOCUMENTATION, preservation_errors


class Preservation(unittest.TestCase):
    def test_only_two_navigation_files_are_exempt(self):
        self.assertEqual(set(MUTABLE_DOCUMENTATION), {'README.md', 'docs/papers/README.md'})
        snapshot = json.loads((BASE/'docs/status/preservation.v1.json').read_text())
        self.assertTrue(set(MUTABLE_DOCUMENTATION) <= snapshot['sha256'].keys())
        self.assertTrue(all(MUTABLE_DOCUMENTATION.values()))

    def test_navigation_edits_allowed_but_protected_changes_and_deletions_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = ['README.md', 'docs/papers/README.md', 'src/geometric_labs/hurwitz.py',
                     'verification/test_golden_vectors.py', 'spec_sync/golden_vectors/vector.json',
                     'docs/architecture_blueprint.md', 'Makefile', '.github/workflows/verify_15_lemmas.yml']
            digest = hashlib.sha256(b'original').hexdigest()
            snapshot = {'sha256': dict.fromkeys(paths, digest)}
            for name in paths:
                path = root/name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'original')
            for name in MUTABLE_DOCUMENTATION:
                (root/name).write_bytes(b'new archive links')
            self.assertEqual(preservation_errors(root, snapshot), [])
            for name in paths[2:]:
                with self.subTest(name=name):
                    path = root/name
                    path.write_bytes(b'changed')
                    self.assertEqual(preservation_errors(root, snapshot), [f'{name}: original reference bytes changed'])
                    path.unlink()
                    self.assertEqual(preservation_errors(root, snapshot), [f'{name}: original reference file missing'])
                    path.write_bytes(b'original')

    def test_unrecognized_paths_are_immutable_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            snapshot = {'sha256': {'new-reference.txt': hashlib.sha256(b'expected').hexdigest()}}
            (root/'new-reference.txt').write_bytes(b'edited')
            self.assertTrue(preservation_errors(root, snapshot))
