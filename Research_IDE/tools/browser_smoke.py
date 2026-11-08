#!/usr/bin/env python3
"""Optional Chromium workflow check, with local PDF.js 4.10.38 test dependencies.

Supply build/pdf.min.mjs and build/pdf.worker.min.mjs from the pdfjs-dist@4.10.38 npm package in
--dependency-dir. They must be the exact published files: the page checks their integrity hashes.
Other CDNs are blocked to exercise the IDE's metadata/manual-import fallbacks.
This is a functional check, not a visual review of CDN styling or the 3D viewer.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import tempfile
import threading

from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--site-dir', type=Path, required=True)
parser.add_argument('--dependency-dir', type=Path, required=True)
parser.add_argument('--output-dir', type=Path, required=True)
args = parser.parse_args()
PDFJS = 'https://cdn.jsdelivr.net/npm/pdfjs-dist@4.10.38/build/'
for name in ('pdf.min.mjs', 'pdf.worker.min.mjs'):
    if not (args.dependency_dir/name).is_file():
        parser.error('missing pinned PDF.js test dependency: ' + name)
args.output_dir.mkdir(parents=True, exist_ok=True)
corpus = json.loads((args.site_dir/'research-ide/official/CATALOG.json').read_text())
expected = {row['id'] for row in corpus['documents']}
with tempfile.TemporaryDirectory(prefix='official-ide-browser-') as directory:
    shutil.copytree(args.site_dir, Path(directory)/'Geometric-Labs')
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, *args): pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=directory))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    base = f'http://127.0.0.1:{server.server_port}/Geometric-Labs/research-ide/'
    checks = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=shutil.which('chromium'), headless=True, args=['--no-sandbox'])
            context = browser.new_context(viewport={'width': 1440, 'height': 1000})
            def route_request(route):
                url = route.request.url
                if url.startswith(base): route.continue_()
                elif url in (PDFJS + 'pdf.min.mjs', PDFJS + 'pdf.worker.min.mjs'):
                    # crossorigin="anonymous" module scripts need a CORS response for the integrity check.
                    route.fulfill(path=str(args.dependency_dir/url.rsplit('/', 1)[1]), content_type='text/javascript',
                                  headers={'Access-Control-Allow-Origin': '*'})
                else: route.abort()
            context.route('**/*', route_request)
            # The page's Content-Security-Policy refuses string evaluation, so wait_for_function
            # predicates are written as functions ("() => ...").
            page = context.new_page(); errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(base+'index.html')
            page.wait_for_function('() => papersState.filter(p => p.officialRecord).length === ' + str(len(expected)))
            page.wait_for_function("() => document.getElementById('badgeCount_biochain').textContent === '" + str(len(expected)) + "'")
            assert page.evaluate('activeCorpusTab') == 'biochain'
            assert set(page.evaluate('papersState.map(p => p.id)')) == expected
            assert page.locator('#badgeCount_biochain').inner_text() == str(len(expected))
            assert 'Official' in page.locator('#corpusTabBtn_biochain').inner_text()
            checks.append('Default collection contains exactly the designated official publications, with no archive/sample entries.')
            # DOM access remains usable when optional icon/CSS/3D CDNs are unavailable.
            page.add_style_tag(content='.hidden { display: none !important; }')
            page.locator('#corpusSearchInput').fill('CubiLoom')
            assert page.locator('#fileTreeContainer').inner_text().strip()
            page.locator('#corpusSearchInput').fill('')
            page.locator('#mdFileInput').set_input_files({'name': 'archived-note.md',
                'mimeType': 'text/markdown', 'buffer': b'# Archived note\n\nManually imported.'})
            page.wait_for_function("() => papersState.some(p => p.workspaceTab === 'custom' && p.title === 'Archived note')")
            assert page.evaluate('activeCorpusTab') == 'custom'
            assert set(page.evaluate("papersState.filter(p => p.workspaceTab === 'biochain').map(p => p.id)")) == expected
            checks.append('Manual archived Markdown import stays in the Research Desk and does not change the official collection.')
            page.evaluate("switchCorpusTab('biochain')")
            page.locator('#officialOpenPdf').click(force=True)
            page.wait_for_function('() => getActivePaper().pdfDoc !== null', timeout=30000)
            page.wait_for_function("() => document.getElementById('officialPdfStatus').textContent.includes('SHA-256 checked')", timeout=30000)
            assert page.evaluate('getActivePaper().pdfDoc.numPages') == corpus['documents'][0]['pages']
            assert page.evaluate("document.getElementById('pdfRenderCanvas').width") > 0
            checks.append('Original official PDF loads through real PDF.js 4.10.38 (integrity-checked modules), passes SHA-256 and renders pages in the inspector.')
            # An imported PDF is a working document, even while official releases were selected.
            source = args.site_dir/'research-ide'/corpus['documents'][0]['pdf_path']
            page.locator('#pdfFileInput').set_input_files(str(source))
            page.wait_for_function("() => papersState.some(p => p.workspaceTab === 'custom' && p.pdfDoc)", timeout=30000)
            assert page.evaluate('activeCorpusTab') == 'custom'
            assert len(page.evaluate("papersState.filter(p => p.workspaceTab === 'biochain')")) == len(expected)
            checks.append('Manual PDF import never becomes an official publication.')
            tampered = context.new_page()
            tampered.route('**/papers/**/*.pdf', lambda route: route.fulfill(status=200, body=b'changed PDF'))
            tampered.goto(base+'index.html')
            tampered.wait_for_function("() => document.getElementById('badgeCount_biochain').textContent === '" + str(len(expected)) + "'")
            tampered.locator('#officialOpenPdf').click(force=True)
            tampered.wait_for_function("() => document.getElementById('officialPdfStatus').textContent.includes('hash mismatch')")
            assert tampered.evaluate('getActivePaper().pdfDoc') is None
            checks.append('Tampered PDF bytes fail before parsing and cannot appear as a checked official source.')
            broken = context.new_page()
            broken.route('**/official/CATALOG.json', lambda route: route.fulfill(status=503, body='unavailable'))
            broken.goto(base+'index.html')
            broken.locator('#officialRetryButton').wait_for(state='visible')
            assert broken.evaluate("papersState.filter(p => p.workspaceTab === 'biochain').length") == 0
            broken.unroute('**/official/CATALOG.json')
            broken.locator('#officialRetryButton').click(force=True)
            broken.wait_for_function('() => papersState.length === ' + str(len(expected)))
            checks.append('Catalog failure is explicit; retry restores only official entries without falling back to samples.')
            assert not errors, errors
            browser.close()
        (args.output_dir/'official-browser-review.json').write_text(json.dumps({
            'status': 'PASS', 'checks': checks,
            'scope': 'Functional IDE workflow; local pinned PDF.js dependencies, other CDNs blocked. Styling/3D/AI calls not tested.'}, indent=2)+'\n')
        print('\n'.join(checks))
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=2)
