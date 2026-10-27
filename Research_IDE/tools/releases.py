#!/usr/bin/env python3
"""Generate the owner-designated official collection without changing proof status."""
from __future__ import annotations

import argparse
import copy
import datetime
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

import archive
import library

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 'geometric-labs.official-corpus.v1'


def publication_id(url: str) -> str:
    parts = urlsplit(url)
    match = re.fullmatch(r'/([0-9]+)/[A-Za-z0-9_]+/?', parts.path)
    if (parts.scheme != 'https' or parts.netloc != 'www.academia.edu'
            or parts.query or parts.fragment or not match):
        raise ValueError('canonical https://www.academia.edu/ID/Title URL required')
    return match.group(1)


def promote(root: Path, pid: str, url: str, *, date: str, inherit=(), replaces=(),
            source_note='User-supplied PDF matched to the user-supplied Academia publication title.') -> None:
    """Record explicit owner designation and copy relevance/labels with provenance.

    Call only after the owner has designated this publication. PDF ingest and
    document-family matching happen separately; this function never overwrites PDFs.
    """
    pub_id = publication_id(url)
    datetime.date.fromisoformat(date)
    folder = library.find_paper(root, pid)
    m = library.load_json(folder/'manifest.json')
    a = m['archive']
    inherited = []
    relevance = {r['repository']: copy.deepcopy(r) for r in a['relevance']}
    topics, tags = set(a['topics']), set(m['tags'])
    for source_id in dict.fromkeys([*inherit, *replaces]):
        if source_id == pid:
            raise ValueError('cannot inherit from self')
        source_folder = library.find_paper(root, source_id)
        source = library.load_json(source_folder/'manifest.json')
        sa = source['archive']
        if source_id in replaces and sa['work_id'] != a['work_id']:
            raise ValueError('replacement must be within a reviewed work family')
        inherited.append({'from': source_id, 'source_sha256': sa['source_sha256'],
                          'tags': source['tags'], 'topics': sa['topics'], 'relevance': sa['relevance']})
        tags.update(source['tags']); topics.update(sa['topics'])
        for rel in sa['relevance']:
            if rel['repository'] not in relevance:
                rel = copy.deepcopy(rel)
                if rel['role'] == 'primary' and any(r['role'] == 'primary' for r in relevance.values()):
                    rel['role'] = 'supporting'
                relevance[rel['repository']] = rel
    a['relevance'] = list(relevance.values())
    a['topics'] = sorted(topics)
    m['tags'] = sorted(tags)
    m['source']['url'] = url
    m['updated'] = date
    a['release_status'] = 'official-release'
    a['release_record'] = {
        'basis': 'owner-designated-publication', 'publication_id': pub_id, 'publication_url': url,
        'designated_by': 'BioChainAI repository owner (explicit user instruction)',
        'designation_date': date, 'version': a['revision_label'], 'license': None,
        'source_sha256': a['source_sha256'], 'evidence': 'workflows/official-designation.md',
        'source_note': source_note, 'inheritance': inherited, 'replaces_references': list(replaces),
        'scientific_verification': 'Separate from official designation; existing triage/Lean status unchanged.'}
    evidence = folder/'workflows/official-designation.md'
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(
        f'# Official collection designation — {pid}\n\n'
        f'On {date}, the repository owner supplied this Academia URL and designated the list as '
        f'“the official release papers for the Geometric Labs ecosystem.”\n\n'
        f'Publication: {url}\n\nSource SHA-256: `{a["source_sha256"]}`.\n\n'
        f'{source_note}\n\n'
        'This records the owner’s collection choice, not peer review, an independent proof audit, '
        'a software release or an additional reuse license. Publication date and version remain '
        'unknown unless explicit in the source. External Academia bytes were not independently verified.\n\n'
        f'Inherited metadata sources: {", ".join(x["from"] for x in inherited) or "none"}. '
        f'Current-reference replacements: {", ".join(replaces) or "none"}. '
        'Inherited labels and repository relevance are captured in the manifest release record.\n')
    library.dump_json(folder/'manifest.json', m)
    library.track(root, pid, update=True, date=date)
    for source_id in replaces:
        source_folder = library.find_paper(root, source_id)
        source = library.load_json(source_folder/'manifest.json')
        source['archive']['disposition'] = 'superseded'
        source['archive']['current_reference'] = pid
        source['updated'] = date
        library.dump_json(source_folder/'manifest.json', source)
        with (source_folder/'RESEARCH_LOG.md').open('a') as handle:
            handle.write(f'\n- {date}: Official reference now {pid}, as designated by the owner. '
                         'Original PDF retained; content revision ordering is not inferred from PDF bytes.\n')
    library.write_index(root)


def check(root: Path) -> list[str]:
    errors = library.check(root)
    rows = archive.records(root)
    errors += archive.validate(root, rows)
    by_id = {r['id']: r for r in rows}
    publications = set()
    for row in rows:
        current = row['id']
        seen = set()
        try:
            while by_id[current]['archive'].get('current_reference'):
                if current in seen:
                    raise ValueError('current-reference cycle')
                seen.add(current)
                target = by_id[current]['archive']['current_reference']
                if by_id[target]['archive']['work_id'] != by_id[current]['archive']['work_id']:
                    raise ValueError('current reference crosses work families')
                current = target
            if seen and (by_id[current]['archive']['release_status'] != 'official-release'
                         or by_id[current]['archive']['disposition'] in {'superseded', 'withdrawn'}):
                raise ValueError('current reference must end at an active official publication')
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f'{row["id"]}: {exc}')
    for row in rows:
        a = row['archive']
        if a['release_status'] != 'official-release' or a['disposition'] in {'superseded', 'withdrawn'}:
            continue
        try:
            rec = a['release_record']
            if rec.get('basis') != 'owner-designated-publication':
                continue  # Existing technical approval records keep their own semantics.
            pub = publication_id(rec['publication_url'])
            if pub != rec['publication_id'] or pub in publications:
                raise ValueError('wrong or duplicate publication identity')
            publications.add(pub)
            m = library.load_json(root/row['path']/'manifest.json')
            if m['source']['url'] != rec['publication_url']:
                raise ValueError('manifest publication URL differs from designation')
            for inherited in rec['inheritance']:
                source = by_id[inherited['from']]
                if inherited['source_sha256'] != source['archive']['source_sha256']:
                    raise ValueError('inheritance references different source bytes')
                if not set(inherited['tags']) <= set(m['tags']) or not set(inherited['topics']) <= set(a['topics']):
                    raise ValueError('inherited labels lost')
                if not {r['repository'] for r in inherited['relevance']} <= {r['repository'] for r in a['relevance']}:
                    raise ValueError('inherited repository relevance lost')
            for old in rec['replaces_references']:
                sa = by_id[old]['archive']
                if sa['work_id'] != a['work_id'] or sa.get('current_reference') != row['id'] or sa['disposition'] != 'superseded':
                    raise ValueError('replacement reference does not resolve to current official document')
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f'{row["id"]}: {exc}')
    return errors


def catalog(root: Path) -> dict:
    documents = []
    replacements = {}
    for row in archive.records(root):
        a = row['archive']
        if a.get('current_reference'):
            replacements[row['id']] = a['current_reference']
        rec = a['release_record'] or {}
        if (a['release_status'] != 'official-release' or a['disposition'] in {'superseded', 'withdrawn'}
                or rec.get('basis') != 'owner-designated-publication'):
            continue
        m = library.load_json(root/row['path']/'manifest.json')
        source = archive.safe_artifact(root/row['path'], a['source_artifact'])
        documents.append({'id': row['id'], 'title': row['title'], 'work_id': a['work_id'],
            'release_status': 'official-release', 'publication_id': rec['publication_id'],
            'publication_url': rec['publication_url'], 'document_date': a['document_date'],
            'designation_date': rec['designation_date'], 'version': rec['version'],
            'pdf_path': source.relative_to(root).as_posix(), 'source_sha256': a['source_sha256'],
            'bytes': source.stat().st_size, 'pages': m['source']['pages'],
            'tags': m['tags'], 'topics': a['topics'], 'relevance': a['relevance'],
            'replaces_references': rec['replaces_references'], 'inherited_from': [x['from'] for x in rec['inheritance']],
            'review_level': a['review_level'], 'lean_status': m['lean_status'], 'source_note': rec['source_note']})
    return {'schema': SCHEMA, 'designation_basis': 'Owner-designated official publications; proof status is separate.',
            'documents': sorted(documents, key=lambda r: int(r['publication_id'])), 'replacements': replacements}


def products(root: Path) -> dict[str, str]:
    data = catalog(root)
    lines = ['# Official Geometric Labs publications', '',
             'Owner-designated official collection. Scientific verification, licensing and software implementation status remain separate.', '',
             '| Paper | Publication | Repository relevance | Previous reference |', '| --- | --- | --- | --- |']
    for row in data['documents']:
        title = row['title'].replace('|', '/')
        lines.append(f'| [{row["id"]}](../{Path(row["pdf_path"]).parent.parent.as_posix()}/README.md) | '
                     f'[{title}]({row["publication_url"]}) | '
                     f'{", ".join(r["repository"] for r in row["relevance"])} | '
                     f'{", ".join(row["replaces_references"]) or "—"} |')
    return {'CATALOG.json': json.dumps(data, indent=2, ensure_ascii=False)+'\n',
            'CATALOG.md': '\n'.join(lines)+'\n'}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('index'); sub.add_parser('check'); sub.add_parser('list')
    resolve = sub.add_parser('resolve'); resolve.add_argument('paper')
    designate = sub.add_parser('designate')
    designate.add_argument('paper')
    designate.add_argument('--publication-url', required=True)
    designate.add_argument('--date', required=True)
    designate.add_argument('--inherit', action='append', default=[])
    designate.add_argument('--replaces', action='append', default=[])
    args = parser.parse_args(argv)
    try:
        errors = check(args.root)
        if errors:
            raise ValueError('\n'.join(errors))
        if args.command == 'designate':
            promote(args.root, library.normalize_id(args.paper), args.publication_url,
                    date=args.date, inherit=args.inherit, replaces=args.replaces)
            print('Official designation recorded. Run make index and make check before publication.')
            return 0
        if args.command in {'check', 'index'}:
            for name, content in products(args.root).items():
                path = args.root/'official'/name
                if args.command == 'index':
                    path.parent.mkdir(exist_ok=True); path.write_text(content)
                elif not path.is_file() or path.read_text() != content:
                    raise ValueError('stale official catalog; run releases.py index')
            print(f'OK: {len(catalog(args.root)["documents"])} official publications')
        elif args.command == 'list':
            for row in catalog(args.root)['documents']:
                print(row['id'], row['publication_id'], row['title'])
        else:
            pid = library.normalize_id(args.paper)
            library.find_paper(args.root, pid)
            replacements = catalog(args.root)['replacements']
            seen = set()
            while pid in replacements:
                if pid in seen: raise ValueError('replacement cycle')
                seen.add(pid); pid = replacements[pid]
            print(pid)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
