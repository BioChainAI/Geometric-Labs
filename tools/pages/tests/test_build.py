"""Site contracts and publication boundaries. No network or scientific fixtures rewritten."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('pages_build',ROOT/'tools/pages/build.py')
build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)


class PageBuild(unittest.TestCase):
    def test_all_current_paths_classified_once(self):
        data=build.scan(ROOT)
        self.assertEqual(sum(s['file_count'] for s in data['sections']),data['tracked_files'])
        self.assertEqual(len(data['files']),len({f['path'] for f in data['files']}))
        self.assertIn('pages',{s['id'] for s in data['sections']})

    def test_longer_prefix_overrides_ecosystem(self):
        sections=build.load_sections(ROOT)['sections']
        self.assertEqual(build.classify('ecosystem/experiments/alexneth_geot/src/model.py',sections),'vision')
        self.assertEqual(build.classify('ecosystem/docs/new.md',sections),'ecosystem_docs')
        with self.assertRaises(ValueError): build.classify('new_unreviewed_product/file.py',sections)

    def test_metadata_duplicate_unknown_entry_and_bad_status(self):
        original=json.loads((ROOT/'site/sections.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'site').mkdir()
            for s in original['sections']:
                p=root/s['entry'];p.parent.mkdir(parents=True,exist_ok=True);p.touch()
            for change in ('duplicate','entry','status','relationship'):
                config=copy.deepcopy(original)
                if change=='duplicate': config['sections'][1]['id']=config['sections'][0]['id']
                if change=='entry': config['sections'][0]['entry']='missing.md'
                if change=='status': config['sections'][0]['status']='universally-proven'
                if change=='relationship': config['relationships'][0]['target']='absent'
                (root/'site/sections.json').write_text(json.dumps(config))
                with self.assertRaises(ValueError): build.load_sections(root)

    def test_safe_metadata_paths(self):
        for path in ('/etc/passwd','../escape','https://example.com/x','.env','a\\b'):
            with self.assertRaises(ValueError): build.safe_path(path)

    def test_evidence_is_historical_with_its_own_revision(self):
        data=build.scan(ROOT)
        self.assertEqual(data['evidence']['state'],'recorded')
        self.assertEqual(data['evidence']['test_methods'],140)
        self.assertNotEqual(data['evidence']['source_commit'],data['source_commit'])
        self.assertFalse(data['evidence']['same_revision'])

    def test_evidence_can_be_missing_without_inventing_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            data=build.evidence(Path(directory))
            self.assertEqual(data['state'],'unavailable')
            self.assertNotIn('test_methods',data)

    def test_invalid_evidence_is_not_presented_as_a_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);folder=root/build.CHECKPOINT;folder.mkdir(parents=True)
            (folder/'checkpoint-validation.json').write_text(json.dumps({
                'schema':'geometric-labs.checkpoint-validation.v1','base_commit':'a'*40,
                'fresh_unique_unittest_methods':'140','packet_cases':183}))
            with self.assertRaises(ValueError): build.evidence(root)

    def test_output_boundaries_and_foreign_directory_preserved(self):
        with self.assertRaises(ValueError): build.build(ROOT/'_site')
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory);marker=path/'user-file';marker.write_text('keep')
            with self.assertRaises(ValueError): build.build(path)
            self.assertEqual(marker.read_text(),'keep')

    def test_curated_artifact_and_repeat_build(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'site'
            build.build(output)
            data=build.validate_artifact(output)
            self.assertEqual(data['schema'],'geometric-labs.pages-status.v1')
            for name in ('index.html', 'explorer.html', 'tutorial.css', 'tutorial.js'):
                self.assertEqual((output/'circuit-seth'/name).read_bytes(), (ROOT/'site/circuit-seth'/name).read_bytes())
            tutorial = output/'circuit-seth/tutorial.js'
            tutorial.unlink()
            with self.assertRaises(ValueError): build.validate_artifact(output)
            tutorial.write_bytes((ROOT/'site/circuit-seth/tutorial.js').read_bytes())
            self.assertFalse((output/'src').exists())
            self.assertFalse((output/'ecosystem').exists())
            self.assertEqual((output/'research-ide/index.html').read_bytes(),(ROOT/'Research_IDE/index.html').read_bytes())
            self.assertEqual((output/'checkpoint/map.json').read_bytes(),(ROOT/build.CHECKPOINT/'map.json').read_bytes())
            build.build(output)
            build.validate_artifact(output)

    def test_broken_link_and_traversal_fail_artifact_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'site';build.build(output)
            original=(output/'index.html').read_text()
            for link in ('missing.html','../escape.html','javascript:alert(1)'):
                (output/'index.html').write_text(original+'<a href="'+link+'">bad</a>')
                with self.assertRaises(ValueError): build.validate_artifact(output)

    def test_repository_case_research_ide_url_redirects_inside_project(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'site';build.build(output)
            alias=output/'Research_IDE/index.html'
            parser=build.Links();parser.feed(alias.read_text())
            self.assertEqual(parser.refresh,['../research-ide/index.html'])
            self.assertIn('../research-ide/index.html',parser.links)
            self.assertEqual((alias.parent/parser.refresh[0]).resolve(),(output/'research-ide/index.html').resolve())
            alias.unlink()
            with self.assertRaises(ValueError): build.validate_artifact(output)

    def test_only_official_pdfs_published_and_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'site';build.build(output)
            corpus=json.loads((output/'research-ide/official/CATALOG.json').read_text())
            expected={r['pdf_path'] for r in corpus['documents']}
            actual={p.relative_to(output/'research-ide').as_posix() for p in (output/'research-ide/papers').rglob('*.pdf')}
            self.assertEqual(actual,expected)
            self.assertFalse(any('RP-0006_' in p or 'RP-0011_' in p for p in actual))
            extra=output/'archive.pdf';extra.write_bytes(b'unapproved')
            with self.assertRaises(ValueError): build.validate_artifact(output)
            extra.unlink()
            source=output/'research-ide'/corpus['documents'][0]['pdf_path']
            source.write_bytes(b'tampered')
            with self.assertRaises(ValueError): build.validate_artifact(output)

    def test_research_ide_alias_wrong_or_escaping_redirect_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'site';build.build(output)
            alias=output/'Research_IDE/index.html';original=alias.read_text()
            for target in ('missing.html','../../outside.html','https://example.com/'):
                alias.write_text(original.replace('0; url=../research-ide/index.html','0; url='+target))
                with self.assertRaises(ValueError): build.validate_artifact(output)

    def test_production_mode_refuses_dirty_preview(self):
        with tempfile.TemporaryDirectory() as directory:
            data=build.scan(ROOT);data['preview_with_uncommitted_changes']=True
            with patch.object(build,'scan',return_value=data):
                with self.assertRaises(ValueError): build.build(Path(directory)/'site',require_clean=True)

    def test_commit_text_is_json_data_not_html(self):
        text='<script>alert("not markup")</script>'
        self.assertEqual(json.loads(json.dumps({'subject':text}))['subject'],text)
        js=(ROOT/'site/assets/site.js').read_text()
        self.assertNotIn('innerHTML',js)
        self.assertIn('textContent',js)


if __name__=='__main__': unittest.main()
