#!/usr/bin/env python3
"""Build a curated GitHub Pages artifact using only the standard library.

Repository metadata is scanned; scientific tests are not executed by this build.
The publication tree never includes arbitrary repository files or dependency clones.
"""
from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
from urllib.parse import quote, urlsplit, unquote

ROOT = Path(__file__).resolve().parents[2]
REPO = 'https://github.com/BioChainAI/Geometric-Labs'
STATUSES = {'implemented', 'experimental', 'reference', 'planned', 'blocked'}
CHECKPOINT = 'ecosystem/docs/checkpoints/2026-10-25'


def official_catalog(root=ROOT):
    result = subprocess.run([sys.executable, str(root/'Research_IDE/tools/releases.py'),
                             '--root', str(root/'Research_IDE'), 'check'],
                            capture_output=True, text=True)
    if result.returncode:
        raise ValueError('invalid official collection: ' + result.stdout + result.stderr)
    return json.loads((root/'Research_IDE/official/CATALOG.json').read_text())


def git(*args, root=ROOT):
    return subprocess.check_output(['git', *args], cwd=root, text=True).strip()


def safe_path(value):
    if not isinstance(value, str) or not value or '\\' in value or '\x00' in value or urlsplit(value).scheme:
        raise ValueError('nonempty POSIX path required')
    p = PurePosixPath(value)
    if p.is_absolute() or '..' in p.parts or value.startswith('.') and value not in ('.gitignore',) and not value.startswith('.github/'):
        raise ValueError('unsafe metadata path: ' + value)
    return value


def load_sections(root=ROOT):
    config = json.loads((root / 'site/sections.json').read_text())
    if config.get('schema') != 'geometric-labs.site-sections.v1':
        raise ValueError('unknown section schema')
    ids, rules = set(), set()
    for s in config['sections']:
        if not re.fullmatch('[a-z][a-z0-9_]*', s['id']) or s['id'] in ids:
            raise ValueError('duplicate/invalid section id')
        ids.add(s['id'])
        if s['status'] not in STATUSES or not all(isinstance(s[k], str) and s[k].strip() for k in ('title', 'role', 'limits')):
            raise ValueError('invalid section status/text')
        if not (root / safe_path(s['entry'])).is_file():
            raise ValueError('missing section entry: ' + s['entry'])
        if not s['matches']:
            raise ValueError('section requires path rules')
        for rule in s['matches']:
            safe_path(rule)
            if rule in rules:
                raise ValueError('duplicate classification rule')
            rules.add(rule)
    for e in config['relationships']:
        if e['source'] not in ids or e['target'] not in ids or e['kind'] not in ('code', 'reference', 'planned', 'control'):
            raise ValueError('invalid section relationship')
    return config


def classify(path, sections):
    matches = [(len(rule), s['id']) for s in sections for rule in s['matches']
               if (path.startswith(rule) if rule.endswith('/') else path == rule)]
    if not matches:
        raise ValueError('unclassified repository path; update site/sections.json: ' + path)
    return max(matches)[1]


def source_url(sha, path):
    return f'{REPO}/blob/{sha}/' + '/'.join(quote(p, safe='') for p in PurePosixPath(path).parts)


def evidence(root=ROOT):
    """Show a frozen record as a frozen record, never as a current test result."""
    record = root / CHECKPOINT / 'checkpoint-validation.json'
    if not record.exists():
        return {'state': 'unavailable', 'message': 'No reviewed checkpoint evidence is recorded.'}
    data = json.loads(record.read_text())
    if data.get('schema') != 'geometric-labs.checkpoint-validation.v1' or any(type(data.get(key)) is not int or data[key] < 0 for key in ('fresh_unique_unittest_methods', 'packet_cases')):
        raise ValueError('invalid checkpoint evidence schema/counts')
    checkpoint_date = PurePosixPath(CHECKPOINT).name
    datetime.strptime(checkpoint_date, '%Y-%m-%d')
    sha = data.get('base_commit', '')
    if not re.fullmatch('[0-9a-f]{40}', sha):
        raise ValueError('invalid evidence revision')
    return {'state': 'recorded', 'label': 'Recorded checkpoint · not rerun by this site build',
            'source_commit': sha, 'date': checkpoint_date,
            'test_methods': data['fresh_unique_unittest_methods'], 'packet_cases': data['packet_cases'],
            'record_path': CHECKPOINT + '/checkpoint-validation.json',
            'url': source_url(sha, CHECKPOINT + '/checkpoint-validation.json'),
            'browser_note': data.get('real_browser_visual_test', 'NOT RECORDED')}


def scan(root=ROOT):
    config = load_sections(root)
    sha = git('rev-parse', 'HEAD', root=root)
    paths = git('ls-tree', '-r', '--name-only', 'HEAD', root=root).splitlines()
    dirty = bool(git('status', '--porcelain', root=root))
    files = []
    counts = {s['id']: 0 for s in config['sections']}
    for p in paths:
        section = classify(p, config['sections'])
        counts[section] += 1
        files.append({'path': p, 'section': section, 'url': source_url(sha, p)})
    sections = [dict(s, file_count=counts[s['id']], url=source_url(sha, s['entry'])) for s in config['sections']]
    commits = []
    for line in git('log', '-8', '--format=%H%x09%cI%x09%s', root=root).splitlines():
        commit, date, subject = line.split('\t', 2)
        commits.append({'sha': commit, 'date': date, 'subject': subject, 'url': f'{REPO}/commit/{commit}'})
    recorded = evidence(root)
    if recorded['state'] == 'recorded':
        # Evidence was added after the audited revision; link to the current source
        # record while retaining the exact revision its claims describe.
        recorded['url'] = source_url(sha, recorded['record_path'])
        recorded['same_revision'] = recorded['source_commit'] == sha
    return {'schema': 'geometric-labs.pages-status.v1', 'repository': REPO,
            'source_commit': sha, 'source_url': f'{REPO}/tree/{sha}',
            'branch': git('branch', '--show-current', root=root) or 'detached',
            'preview_with_uncommitted_changes': dirty,
            'built_at': datetime.now(timezone.utc).isoformat(), 'tracked_files': len(files),
            'sections': sections, 'relationships': config['relationships'], 'files': files,
            'recent_commits': commits, 'evidence': recorded,
            'paper_entries': len(json.loads((root/'Research_IDE/CATALOG.json').read_text())['papers']),
            'crypto_entries': len(json.loads((root/'Cryptographic_Research/REGISTRY.json').read_text())['items']),
            'pages_actions_url': REPO + '/actions/workflows/static.yml',
            'checkpoint_url': 'checkpoint/index.html', 'research_ide_url': 'research-ide/index.html'}


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.ids = set(); self.title = False; self.refresh = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title': self.title = True
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            value = attrs.get('content', '')
            if not value.startswith('0; url='): raise ValueError('invalid immediate redirect')
            self.refresh.append(value[len('0; url='):])
        if 'id' in attrs: self.ids.add(attrs['id'])
        for name in ('src', 'href'):
            if name in attrs: self.links.append(attrs[name])


PINNED_CDN = re.compile(r'https://cdn\.jsdelivr\.net/npm/(?:@[a-z0-9._-]+/)?[a-z0-9._-]+@\d+\.\d+\.\d+/[^?#\s]+')
PINNED_PACKAGE = re.compile(r'https://cdn\.jsdelivr\.net/npm/(?:@[a-z0-9._-]+/)?[a-z0-9._-]+@\d+\.\d+\.\d+/')
INTEGRITY = re.compile(r'sha(?:384|512)-[A-Za-z0-9+/]+={0,2}')
# Stylesheets whose content varies by browser and so cannot carry an integrity hash, each with the
# font host it uses. They cannot run script; each page's Content-Security-Policy limits them to
# their own hosts.
UNHASHABLE_STYLESHEETS = {'https://fonts.googleapis.com/css2?': 'https://fonts.gstatic.com/'}
PUBLISHED_ASSETS = {'research-ide': ('official-corpus.js', 'ide-safety.js', 'ide-tailwind.css'),
                    'circuit-seth': ('tutorial.css', 'tutorial.js', 'explorer-tailwind.css')}
# CSP sources accepted besides the exact pinned files a page loads (allowlist, per directive).
CSP_KEYWORDS = {'script-src': {"'self'", "'none'", "'unsafe-inline'", "'wasm-unsafe-eval'"},
                'style-src': {"'self'", "'none'", "'unsafe-inline'"},
                'font-src': {"'self'", "'none'", 'data:'}}
CSP_HASH = re.compile(r"'sha(?:256|384|512)-[A-Za-z0-9+/]+={0,2}'")
# String specifiers of static and dynamic imports in an inline module script.
MODULE_IMPORT = re.compile(r"""(?:\bimport\s*\(?|\bfrom)\s*(['"`])(.*?)\1""", re.S)


def first_attributes(attrs):
    """Attributes by name; the first occurrence wins, as in browsers."""
    result = {}
    for key, value in attrs:
        result.setdefault(key, value)
    return result


def url_parts(url):
    """Split a URL attribute as a browser reads it: outer spaces and inner tabs/newlines dropped,
    backslashes read as slashes."""
    return urlsplit(re.sub(r'[\t\n\r]', '', url.strip()).replace('\\', '/'))


def is_external(url):
    parts = url_parts(url)
    return bool(parts.scheme or parts.netloc)


class Resources(HTMLParser):
    """External scripts and stylesheets of one page with their integrity attributes, the CSP metas
    with their position, and anything that could load script without being listed here."""
    def __init__(self):
        super().__init__(); self.external = []; self.csp = []; self.problems = []
        self.elements = 0; self.first_load = None; self.in_head = False; self.module = None
    def handle_starttag(self, tag, attrs):
        attrs = first_attributes(attrs); self.elements += 1
        if tag == 'head': self.in_head = True
        elif tag == 'body': self.in_head = False
        if tag == 'base': self.problems.append('a base element is not allowed')
        if tag == 'meta' and (attrs.get('http-equiv') or '').strip().lower() == 'content-security-policy':
            self.csp.append({'policy': attrs.get('content') or '', 'position': self.elements, 'in_head': self.in_head})
        if tag in ('script', 'link') and self.first_load is None:
            self.first_load = self.elements
        url = None
        if tag == 'script':
            url = attrs.get('src') or attrs.get('href') or attrs.get('xlink:href')
            kind = (attrs.get('type') or '').strip().lower()
            if kind == 'importmap': self.problems.append('an import map is not allowed')
            if url is None and kind == 'module': self.module = []
        elif tag == 'link' and 'stylesheet' in (attrs.get('rel') or '').lower().split():
            url = attrs.get('href')
        if url is not None and is_external(url):
            self.external.append({'tag': tag, 'url': url, 'integrity': attrs.get('integrity'),
                                  'crossorigin': attrs.get('crossorigin')})
    def handle_data(self, data):
        if self.module is not None: self.module.append(data)
    def handle_endtag(self, tag):
        if tag == 'head': self.in_head = False
        if tag == 'script' and self.module is not None:
            for _, specifier in MODULE_IMPORT.findall(''.join(self.module)):
                if is_external(specifier):
                    self.problems.append('an inline module imports an external file: ' + specifier)
            self.module = None


def csp_sources(policy, directive):
    """Sources of the first occurrence of a directive (later duplicates are ignored, as in browsers)."""
    for part in policy.split(';'):
        words = part.split()
        if words and words[0].lower() == directive:
            return words[1:]
    return None


def csp_location(url):
    """The CSP source that allows exactly this file: the URL without query or fragment."""
    parts = urlsplit(url)
    return f'{parts.scheme}://{parts.netloc}{parts.path}'


def check_external_resources(name, text):
    """Every external script/stylesheet is pinned with SRI, and the page CSP lists exactly those files."""
    parser = Resources(); parser.feed(text); parser.close()
    if parser.problems:
        raise ValueError(f'{name}: {parser.problems[0]}')
    if not parser.external:
        return []
    if len(parser.csp) != 1:
        raise ValueError('page with external resources needs one Content-Security-Policy: ' + name)
    meta = parser.csp[0]
    if not meta['in_head'] or meta['position'] > parser.first_load:
        raise ValueError(name + ': the Content-Security-Policy meta must be in <head>, before any script or stylesheet')
    used = {'script': set(), 'link': set()}
    font_bases = set()
    for item in parser.external:
        unhashable = next((prefix for prefix in UNHASHABLE_STYLESHEETS
                           if item['tag'] == 'link' and item['url'].startswith(prefix)), None)
        if not unhashable:
            if not PINNED_CDN.fullmatch(item['url']):
                raise ValueError('external resource must be an exact-version jsDelivr npm file: ' + item['url'])
            if not item['integrity'] or not INTEGRITY.fullmatch(item['integrity']) or item['crossorigin'] != 'anonymous':
                raise ValueError('external resource needs integrity and crossorigin="anonymous": ' + item['url'])
        used[item['tag']].add(csp_location(item['url']))
        if item['tag'] == 'link':
            font_bases.add(UNHASHABLE_STYLESHEETS[unhashable] if unhashable else PINNED_PACKAGE.match(item['url']).group(0))
    policy = meta['policy']
    for directive, tag in (('script-src', 'script'), ('style-src', 'link')):
        sources = csp_sources(policy, directive)
        if sources is None:
            raise ValueError(f'{name}: CSP lacks {directive}')
        listed = set()
        for source in sources:
            if source.lower() in CSP_KEYWORDS[directive] or CSP_HASH.fullmatch(source):
                continue
            if source not in used[tag]:
                raise ValueError(f'{name}: CSP {directive} allows a source other than the pinned files in use: {source}')
            listed.add(source)
        if listed != used[tag]:
            raise ValueError(f'{name}: CSP {directive} must list exactly {sorted(used[tag])}')
    for source in csp_sources(policy, 'font-src') or []:
        if source.lower() not in CSP_KEYWORDS['font-src'] and not any(
                source.startswith(base) or source + '/' == base for base in font_bases):
            raise ValueError(f'{name}: CSP font-src source is outside the pinned stylesheet packages: {source}')
    for directive in ('default-src', 'object-src', 'base-uri'):
        if [s.lower() for s in csp_sources(policy, directive) or []] != ["'none'"]:
            raise ValueError(name + ": CSP needs default-src, object-src and base-uri 'none'")
    return parser.external


def verify_remote_integrity(output, opener=None):
    """Fetch every pinned CDN file named by the published pages and compare it with its integrity."""
    import base64
    from urllib.request import Request, urlopen
    opener = opener or (lambda url: urlopen(Request(url, headers={'User-Agent': 'geometric-labs-pages'}), timeout=60).read())
    checked = {}
    for page in sorted(Path(output).resolve().rglob('*.html')):
        for item in check_external_resources(page.name, page.read_text()):
            if not item['integrity'] or item['url'] in checked:
                continue
            algorithm, expected = item['integrity'].split('-', 1)
            try:
                body = opener(item['url'])
            except OSError as exc:
                raise ValueError(f"could not download {item['url']}: {exc}") from exc
            actual = base64.b64encode(hashlib.new(algorithm, body).digest()).decode()
            if actual != expected:
                raise ValueError('integrity mismatch for ' + item['url'])
            checked[item['url']] = item['integrity']
    return checked


def validate_artifact(output):
    """Validate generated JSON, homepage and compatibility redirect links."""
    output = Path(output).resolve()
    status = json.loads((output/'data/status.json').read_text())
    if status['schema'] != 'geometric-labs.pages-status.v1' or len(status['files']) != status['tracked_files']:
        raise ValueError('invalid generated snapshot schema/count')
    for relative in ('index.html', 'Research_IDE/index.html', 'circuit-seth/index.html', 'circuit-seth/explorer.html'):
        page = output/relative
        if not page.is_file(): raise ValueError('missing published route: ' + relative)
        parser = Links(); parser.feed(page.read_text())
        if not parser.title: raise ValueError('page requires a title: ' + relative)
        if relative == 'Research_IDE/index.html' and parser.refresh != ['../research-ide/index.html']:
            raise ValueError('Research IDE alias must redirect to the canonical route')
        for link in parser.links + parser.refresh:
            parts = urlsplit(link)
            if parts.scheme:
                if parts.scheme != 'https': raise ValueError('unsafe external URL')
                continue
            if parts.netloc: raise ValueError('protocol-relative URL refused')
            if parts.path:
                target = (page.parent/unquote(parts.path)).resolve()
                if not target.is_relative_to(output) or not target.is_file():
                    raise ValueError('broken/escaping local link: ' + link)
            elif parts.fragment and parts.fragment not in parser.ids:
                raise ValueError('missing page anchor: ' + link)
    if not (output/'checkpoint/index.html').is_file() or not (output/'research-ide/index.html').is_file():
        raise ValueError('missing published workbench/checkpoint')
    if not (output/'research-ide/official-corpus.js').is_file():
        raise ValueError('missing official corpus loader')
    for folder, names in PUBLISHED_ASSETS.items():
        for name in names:
            if not (output/folder/name).is_file():
                raise ValueError('missing published asset: ' + folder + '/' + name)
    for page in sorted(output.rglob('*.html')):
        check_external_resources(page.relative_to(output).as_posix(), page.read_text())
    corpus = json.loads((output/'research-ide/official/CATALOG.json').read_text())
    if corpus.get('schema') != 'geometric-labs.official-corpus.v1':
        raise ValueError('unknown official corpus schema')
    for row in corpus['documents']:
        pdf = (output/'research-ide'/safe_path(row['pdf_path'])).resolve()
        if (row['release_status'] != 'official-release' or not pdf.is_relative_to(output/'research-ide/papers')
                or not pdf.is_file() or hashlib.sha256(pdf.read_bytes()).hexdigest() != row['source_sha256']):
            raise ValueError('invalid/missing official PDF: ' + row['id'])
    expected_pdfs = {'research-ide/' + row['pdf_path'] for row in corpus['documents']}
    actual_pdfs = {p.relative_to(output).as_posix() for p in output.rglob('*')
                   if p.is_file() and p.suffix.lower() == '.pdf'}
    if actual_pdfs != expected_pdfs:
        raise ValueError('unapproved PDF in Pages artifact')
    if any((output/p).exists() for p in ('.git', 'ecosystem/workspaces', '.env', 'src', 'verification')):
        raise ValueError('unapproved repository content in site artifact')
    return status


def build(output, *, root=ROOT, require_clean=False):
    output = Path(output).resolve(); root = root.resolve()
    # Never delete or build into a source checkout or any of its ancestors.
    if output == root or output.is_relative_to(root) or root.is_relative_to(output):
        raise ValueError('output must be outside the repository')
    data = scan(root)
    corpus = official_catalog(root)
    if require_clean and data['preview_with_uncommitted_changes']:
        raise ValueError('production build requires a clean checkout')
    # Avoid arbitrary directory deletion: repeat builds require our marker, and
    # only an empty fresh directory or a marked output is accepted.
    marker = output/'.geometric-pages-build'
    if output.exists():
        if not marker.is_file() and any(output.iterdir()):
            raise ValueError('refusing to replace an unrecognized output directory')
        if marker.is_file(): shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True); marker.write_text('geometric-labs-pages-v1\n')
    (output/'data').mkdir(); (output/'assets').mkdir()
    for name in ('site.css', 'site.js', 'favicon.svg'):
        shutil.copy2(root/'site/assets'/name, output/'assets'/name)
    html = (root/'site/index.html').read_text().replace('__REPO_URL__', REPO)
    (output/'index.html').write_text(html)
    (output/'data/status.json').write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')
    (output/'.nojekyll').write_text('')
    # Explicit Circuit-SETH teaching assets; archived research PDFs remain excluded.
    (output/'circuit-seth').mkdir()
    for name in ('index.html', 'explorer.html') + PUBLISHED_ASSETS['circuit-seth']:
        shutil.copy2(root/'site/circuit-seth'/name, output/'circuit-seth'/name)
    # Explicit publication allowlist, not an entire-repository upload.
    cp = root/CHECKPOINT
    for source, destination in [('index.html','index.html'), ('README.md','README.md'),
                                ('map.json','map.json'), ('inventory.json','inventory.json'),
                                ('checkpoint-validation.json','checkpoint-validation.json'),
                                ('geot-validation.json','geot-validation.json'),
                                ('research-ide.log','research-ide.log'), ('cryptographic-research.log','cryptographic-research.log')]:
        target=output/'checkpoint'/destination; target.parent.mkdir(exist_ok=True)
        shutil.copy2(cp/source,target)
    (output/'research-ide').mkdir()
    for name in ('index.html',) + PUBLISHED_ASSETS['research-ide']:
        shutil.copy2(root/'Research_IDE'/name, output/'research-ide'/name)
    (output/'research-ide/official').mkdir()
    shutil.copy2(root/'Research_IDE/official/CATALOG.json', output/'research-ide/official/CATALOG.json')
    for row in corpus['documents']:
        source = root/'Research_IDE'/safe_path(row['pdf_path'])
        target = output/'research-ide'/row['pdf_path']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    (output/'Research_IDE').mkdir()
    shutil.copy2(root/'site/research-ide-redirect.html', output/'Research_IDE/index.html')
    (output/'UPDATE_PROCEDURE.md').write_text((root/'site/README.md').read_text())
    validate_artifact(output)
    return data


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=Path('/tmp/geometric-labs-pages'))
    p.add_argument('--require-clean',action='store_true')
    p.add_argument('--verify-remote-integrity',action='store_true',
                   help='after building, download each pinned CDN file and compare it with its integrity hash')
    args=p.parse_args()
    data=build(args.output,require_clean=args.require_clean)
    print(f"Built {args.output}: {data['tracked_files']} tracked paths, {len(data['sections'])} sections; source {data['source_commit'][:12]}")
    if args.verify_remote_integrity:
        checked=verify_remote_integrity(args.output)
        print(f'Verified {len(checked)} pinned CDN files against their integrity hashes.')
    print('Scientific test evidence is historical, not re-executed by this build.')


if __name__=='__main__': main()
