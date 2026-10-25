#!/usr/bin/env python3
"""Build a curated GitHub Pages artifact using only the standard library.

Repository metadata is scanned; scientific tests are not executed by this build.
The publication tree never includes arbitrary repository files or dependency clones.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
from urllib.parse import quote, urlsplit, unquote

ROOT = Path(__file__).resolve().parents[2]
REPO = 'https://github.com/BioChainAI/Geometric-Labs'
STATUSES = {'implemented', 'experimental', 'reference', 'planned', 'blocked'}
CHECKPOINT = 'ecosystem/docs/checkpoints/2026-10-25'


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
        super().__init__(); self.links = []; self.ids = set(); self.title = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title': self.title = True
        if 'id' in attrs: self.ids.add(attrs['id'])
        for name in ('src', 'href'):
            if name in attrs: self.links.append(attrs[name])


def validate_artifact(output):
    """Validate generated JSON and root local links; copies have their own scope."""
    output = Path(output).resolve()
    status = json.loads((output/'data/status.json').read_text())
    if status['schema'] != 'geometric-labs.pages-status.v1' or len(status['files']) != status['tracked_files']:
        raise ValueError('invalid generated snapshot schema/count')
    parser = Links(); parser.feed((output/'index.html').read_text())
    if not parser.title: raise ValueError('landing page requires a title')
    for link in parser.links:
        parts = urlsplit(link)
        if parts.scheme:
            if parts.scheme != 'https': raise ValueError('unsafe external URL')
            continue
        if parts.netloc: raise ValueError('protocol-relative URL refused')
        if parts.path:
            target = (output/unquote(parts.path)).resolve()
            if not target.is_relative_to(output) or not target.is_file():
                raise ValueError('broken/escaping local link: ' + link)
        elif parts.fragment and parts.fragment not in parser.ids:
            raise ValueError('missing page anchor: ' + link)
    if not (output/'checkpoint/index.html').is_file() or not (output/'research-ide/index.html').is_file():
        raise ValueError('missing published workbench/checkpoint')
    if any((output/p).exists() for p in ('.git', 'ecosystem/workspaces', '.env', 'src', 'verification')):
        raise ValueError('unapproved repository content in site artifact')
    return status


def build(output, *, root=ROOT, require_clean=False):
    output = Path(output).resolve(); root = root.resolve()
    # Never delete or build into a source checkout or any of its ancestors.
    if output == root or output.is_relative_to(root) or root.is_relative_to(output):
        raise ValueError('output must be outside the repository')
    data = scan(root)
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
    # Explicit publication allowlist, not an entire-repository upload.
    cp = root/CHECKPOINT
    for source, destination in [('index.html','index.html'), ('README.md','README.md'),
                                ('map.json','map.json'), ('inventory.json','inventory.json'),
                                ('checkpoint-validation.json','checkpoint-validation.json'),
                                ('geot-validation.json','geot-validation.json'),
                                ('research-ide.log','research-ide.log'), ('cryptographic-research.log','cryptographic-research.log')]:
        target=output/'checkpoint'/destination; target.parent.mkdir(exist_ok=True)
        shutil.copy2(cp/source,target)
    (output/'research-ide').mkdir(); shutil.copy2(root/'Research_IDE/index.html', output/'research-ide/index.html')
    (output/'UPDATE_PROCEDURE.md').write_text((root/'site/README.md').read_text())
    validate_artifact(output)
    return data


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=Path('/tmp/geometric-labs-pages'))
    p.add_argument('--require-clean',action='store_true')
    args=p.parse_args()
    data=build(args.output,require_clean=args.require_clean)
    print(f"Built {args.output}: {data['tracked_files']} tracked paths, {len(data['sections'])} sections; source {data['source_commit'][:12]}")
    print('Scientific test evidence is historical, not re-executed by this build.')


if __name__=='__main__': main()
