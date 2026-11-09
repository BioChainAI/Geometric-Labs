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
            for name in ('index.html', 'explorer.html', 'tutorial.css', 'tutorial.js', 'explorer-tailwind.css'):
                self.assertEqual((output/'circuit-seth'/name).read_bytes(), (ROOT/'site/circuit-seth'/name).read_bytes())
            for name in ('index.html', 'official-corpus.js', 'ide-safety.js', 'ide-tailwind.css'):
                self.assertEqual((output/'research-ide'/name).read_bytes(), (ROOT/'Research_IDE'/name).read_bytes())
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

    def test_geocubit_explainer_is_first_party_and_published(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/'site'
            build.build(output)
            for name in ('index.html', 'explainer.css', 'explainer.js', 'protocol.md'):
                self.assertEqual((output/'geocubit-crypto'/name).read_bytes(),
                                 (ROOT/'site/geocubit-crypto'/name).read_bytes())
            homepage = (output/'index.html').read_text()
            self.assertIn('href="geocubit-crypto/index.html"', homepage)
            page = output/'geocubit-crypto/index.html'
            parsed = build.Links(); parsed.feed(page.read_text())
            self.assertIn('protocol.md', parsed.links)
            self.assertIn('explainer.js', parsed.links)
            build.validate_artifact(output)
            (output/'geocubit-crypto/explainer.js').unlink()
            with self.assertRaises(ValueError):
                build.validate_artifact(output)

    def test_geocubit_explainer_requires_local_assets_only(self):
        html = (ROOT/'site/geocubit-crypto/index.html').read_text()
        self.assertEqual(build.check_external_resources('geocubit-crypto/index.html', html), [])
        self.assertIn('content="default-src', html)
        self.assertIn('connect-src \'none\'', html)

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


SCRIPT_URL = 'https://cdn.jsdelivr.net/npm/demo@1.2.3/dist/demo.min.js'
STYLE_URL = 'https://cdn.jsdelivr.net/npm/demo@1.2.3/dist/demo.min.css'
PAGE_CSP = ("default-src 'none'; script-src 'self' 'unsafe-inline' " + SCRIPT_URL + "; style-src 'self' " + STYLE_URL
            + "; font-src https://cdn.jsdelivr.net/npm/demo@1.2.3/dist/fonts/ data:; object-src 'none'; base-uri 'none'")
CSP_META = '<meta http-equiv="Content-Security-Policy" content="' + PAGE_CSP + '">'
PAGE_HEAD = ('<!DOCTYPE html><html><head><title>t</title>\n' + CSP_META + '\n'
             '<script src="' + SCRIPT_URL + '" integrity="sha384-{digest}" crossorigin="anonymous"></script>\n'
             '<link rel="stylesheet" href="' + STYLE_URL + '" integrity="sha384-{digest}" crossorigin="anonymous">\n'
             '</head><body></body></html>')


class ExternalResources(unittest.TestCase):
    """Published pages load third-party files only pinned, hash-checked and listed file by file in the CSP."""
    def page(self, digest='A'*64):
        return PAGE_HEAD.replace('{digest}', digest)

    def test_published_pages_pass(self):
        for page in ('Research_IDE/index.html', 'site/circuit-seth/explorer.html'):
            resources = build.check_external_resources(page, (ROOT/page).read_text())
            self.assertTrue(resources, page)
        for page in ('site/index.html', 'site/circuit-seth/index.html'):
            self.assertEqual(build.check_external_resources(page, (ROOT/page).read_text()), [])

    def test_fixture_page_passes(self):
        self.assertEqual(len(build.check_external_resources('fixture', self.page())), 2)
        local_module = self.page().replace('</head>', '<script type="module">import "./local.js"; import("../x.js");</script></head>')
        self.assertEqual(len(build.check_external_resources('fixture', local_module)), 2)
        hashed = self.page().replace("'unsafe-inline'", "'sha256-" + 'B'*43 + "='")
        self.assertEqual(len(build.check_external_resources('fixture', hashed)), 2)

    def test_unpinned_unhashed_or_unlisted_resources_fail(self):
        good = self.page()
        tag = '<script src="' + SCRIPT_URL + '"'
        for bad in (good.replace(' integrity="sha384-' + 'A'*64 + '"', '', 1),
                    good.replace(' crossorigin="anonymous"', '', 1),
                    good.replace('demo@1.2.3/dist/demo.min.js', 'demo/dist/demo.min.js'),
                    good.replace('demo@1.2.3/dist/demo.min.js', 'demo@latest/dist/demo.min.js'),
                    good.replace(SCRIPT_URL, 'https://cdn.tailwindcss.com'),
                    good.replace(SCRIPT_URL, 'https://unpkg.com/demo@1.2.3/dist/demo.min.js'),
                    # CSP sources: every file listed, nothing else
                    good.replace(' ' + SCRIPT_URL + ';', ';', 1),
                    good.replace("script-src 'self'", "script-src 'self' https://extra.example", 1),
                    good.replace("script-src 'self'", "script-src 'self' 'unsafe-eval'", 1),
                    good.replace("script-src 'self'", "script-src 'self' 'strict-dynamic'", 1),
                    good.replace("script-src 'self' 'unsafe-inline' " + SCRIPT_URL, "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net", 1),
                    good.replace("script-src 'self' 'unsafe-inline' " + SCRIPT_URL, "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net/npm/demo@1.2.3/", 1),
                    good.replace("script-src 'self'", "script-src 'self' unpinned.example", 1),
                    good.replace("script-src 'self'", "script-src 'self' data:", 1),
                    good.replace("script-src 'self'", "script-src 'self' blob:", 1),
                    good.replace("style-src 'self'", "style-src 'self' https://cdn.jsdelivr.net", 1),
                    good.replace('font-src https://cdn.jsdelivr.net/npm/demo@1.2.3/dist/fonts/', 'font-src https://cdn.jsdelivr.net', 1),
                    good.replace("default-src 'none'", "default-src *", 1),
                    good.replace("default-src 'none'", "DEFAULT-SRC *; default-src 'none'", 1),
                    good.replace("<meta http-equiv=\"Content-Security-Policy\"", '<meta name="x"', 1),
                    # policy position: a meta CSP applies only to what follows it, and only in <head>
                    good.replace(CSP_META + '\n', '', 1).replace('</head>', CSP_META + '</head>', 1),
                    good.replace(CSP_META + '\n', '', 1).replace('<body>', '<body>' + CSP_META, 1),
                    good.replace(CSP_META, CSP_META + CSP_META, 1),
                    # loads the gate must see
                    good.replace(tag, '<script src="//cdn.jsdelivr.net/npm/demo@1.2.3/dist/demo.min.js"', 1),
                    good.replace(tag, '<script src="//unpinned.example/x.js" src="' + SCRIPT_URL + '"', 1),
                    good.replace('<body>', '<body><svg><script href="https://unpinned.example/x.js"></script></svg>', 1),
                    good.replace('</head>', '<script type="module">import "https://cdn.jsdelivr.net/npm/demo/dist/demo.mjs";</script></head>', 1),
                    good.replace('</head>', '<script type="module">import(\'//unpinned.example/x.js\');</script></head>', 1),
                    good.replace('</head>', '<script type="importmap">{"imports": {}}</script></head>', 1),
                    good.replace('<title>t</title>', '<title>t</title><base href="https://unpinned.example/">', 1)):
            with self.assertRaises(ValueError, msg=bad[:600]): build.check_external_resources('fixture', bad)

    def test_scheme_relative_script_needs_pin_and_policy(self):
        page = '<!DOCTYPE html><html><head><title>t</title><script src="//unpinned.example/lib.js"></script></head><body></body></html>'
        with self.assertRaises(ValueError): build.check_external_resources('fixture', page)
        local = page.replace('//unpinned.example/lib.js', 'assets/lib.js')
        self.assertEqual(build.check_external_resources('fixture', local), [])

    def test_unhashable_font_stylesheet_is_the_only_exception(self):
        page = (ROOT/'site/circuit-seth/explorer.html').read_text()
        build.check_external_resources('explorer', page)
        swapped = page.replace('https://fonts.googleapis.com/css2?', 'https://fonts.example.com/css2?')
        with self.assertRaises(ValueError): build.check_external_resources('explorer', swapped)

    def test_remote_integrity_check_compares_downloaded_bytes(self):
        import base64, hashlib
        body = b'console.log("pinned")'
        digest = base64.b64encode(hashlib.sha384(body).digest()).decode()
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory)/'page.html').write_text(self.page(digest))
            checked = build.verify_remote_integrity(directory, opener=lambda url: body)
            self.assertEqual(len(checked), 2)
            with self.assertRaises(ValueError):
                build.verify_remote_integrity(directory, opener=lambda url: body + b' ')

    def test_missing_page_asset_fails_artifact_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'site';build.build(output)
            for folder, name in (('research-ide', 'ide-safety.js'), ('circuit-seth', 'explorer-tailwind.css')):
                path = output/folder/name; data = path.read_bytes(); path.unlink()
                with self.assertRaises(ValueError): build.validate_artifact(output)
                path.write_bytes(data)
            build.validate_artifact(output)


if __name__=='__main__': unittest.main()
