"""Official designation, metadata inheritance and source-only catalog boundaries."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
import library
import archive
import releases

URL = 'https://www.academia.edu/123456/Example_Paper'


class Releases(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT/'templates', self.root/'templates')
        self.first = self.add_paper('old', b'old source')
        self.second = self.add_paper('new', b'new source')

    def add_paper(self, slug, data):
        folder = library.scaffold(self.root, slug, slug.title(), tags=['retained-label'], date='2026-10-27')
        path = folder/'source/paper.pdf'; path.write_bytes(data)
        pid = folder.name.split('_')[0]
        library.track(self.root, pid)
        m = library.load_json(folder/'manifest.json')
        m['archive'] = {'schema_version': 1, 'work_id': 'WORK-0001', 'revision_label': None,
            'document_date': None, 'received_date': '2026-10-27', 'release_status': 'research-draft',
            'disposition': 'retained-reference', 'review_level': 'relevance-triaged',
            'source_artifact': 'source/paper.pdf', 'source_sha256': library.sha256(path),
            'topics': ['memory'], 'relevance': [{'repository': 'CubiLoom', 'role': 'primary', 'reason': 'History retention'},
                {'repository': 'Manifold-Projection', 'role': 'supporting', 'reason': 'View history'}],
            'relations': [], 'prior_upload': {'status': 'fixture'}, 'release_record': None}
        library.dump_json(folder/'manifest.json', m); library.write_index(self.root)
        return pid

    def promote(self):
        releases.promote(self.root, self.second, URL, date='2026-10-27', replaces=[self.first])

    def test_designation_does_not_invent_proof_license_or_version(self):
        self.promote()
        self.assertEqual(releases.check(self.root), [])
        m = library.load_json(library.find_paper(self.root, self.second)/'manifest.json')
        self.assertEqual(m['stage'], 'intake'); self.assertEqual(m['lean_status'], 'none')
        self.assertIsNone(m['archive']['release_record']['license'])
        self.assertIsNone(m['archive']['release_record']['version'])
        self.assertEqual([r['id'] for r in releases.catalog(self.root)['documents']], [self.second])
        self.assertEqual(releases.catalog(self.root)['replacements'][self.first], self.second)

    def test_repository_links_and_labels_transferred_with_source_hash(self):
        folder = library.find_paper(self.root, self.second)
        m = library.load_json(folder/'manifest.json'); m['tags'] = []
        m['archive']['topics'] = ['new-label']; m['archive']['relevance'] = [m['archive']['relevance'][0]]
        library.dump_json(folder/'manifest.json', m)
        self.promote()
        m = library.load_json(folder/'manifest.json')
        self.assertIn('retained-label', m['tags']); self.assertIn('memory', m['archive']['topics'])
        self.assertIn('Manifold-Projection', [r['repository'] for r in m['archive']['relevance']])
        self.assertEqual(m['archive']['release_record']['inheritance'][0]['from'], self.first)
        self.assertEqual(releases.check(self.root), [])
        m['tags'] = []; library.dump_json(folder/'manifest.json', m); library.write_index(self.root)
        self.assertTrue(any('labels lost' in error for error in releases.check(self.root)))

    def test_pdf_tampering_and_wrong_publication_identity_rejected(self):
        self.promote(); folder = library.find_paper(self.root, self.second)
        m = library.load_json(folder/'manifest.json'); m['archive']['release_record']['publication_id'] = '999'
        library.dump_json(folder/'manifest.json', m)
        self.assertTrue(any('publication identity' in e for e in releases.check(self.root)))
        (folder/'source/paper.pdf').write_bytes(b'tampered')
        self.assertTrue(any('hash/size' in e for e in releases.check(self.root)))

    def test_malformed_publication_urls_and_cross_work_replacements_rejected(self):
        for url in ['http://www.academia.edu/123456/Example', 'https://example.com/123456/Example',
                    'https://www.academia.edu/123456/Example?download=1']:
            with self.assertRaises(ValueError): releases.publication_id(url)
        folder = library.find_paper(self.root, self.first); m = library.load_json(folder/'manifest.json')
        m['archive']['work_id'] = 'WORK-0002'; library.dump_json(folder/'manifest.json', m)
        with self.assertRaises(ValueError): self.promote()

    def test_legacy_source_bytes_remain_unchanged_and_current_cycles_fail(self):
        self.promote(); folder = library.find_paper(self.root, self.first)
        self.assertEqual((folder/'source/paper.pdf').read_bytes(), b'old source')
        m = library.load_json(folder/'manifest.json'); m['archive']['current_reference'] = self.first
        library.dump_json(folder/'manifest.json', m); library.write_index(self.root)
        self.assertTrue(any('cycle' in e for e in releases.check(self.root)))


class LiveOfficialCollection(unittest.TestCase):
    def test_catalog_is_current_and_has_only_designated_publications(self):
        self.assertEqual(releases.check(ROOT), [])
        data = releases.catalog(ROOT)
        self.assertEqual(len(data['documents']), len({r['publication_id'] for r in data['documents']}))
        self.assertTrue(all(r['release_status'] == 'official-release' for r in data['documents']))
        self.assertNotIn('RP-0006', {r['id'] for r in data['documents']})
        self.assertEqual(data['replacements']['RP-0006'], 'RP-0020')
        for name, content in releases.products(ROOT).items():
            self.assertEqual((ROOT/'official'/name).read_text(), content)
