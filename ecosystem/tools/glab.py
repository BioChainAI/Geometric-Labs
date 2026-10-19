#!/usr/bin/env python3
"""Clone-missing workspace manager. Existing checkouts never pull, reset or advance."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
MANIFEST = BASE / 'manifest/repositories.v1.json'
LOCK = BASE / 'locks/commits.lock.json'
SCHEMA = 'biochain.geometric-labs.ecosystem-lock.v1'
NAMES = ('SHD-CCP-core', 'Kernel-Registry', 'CubiLoom', 'PolyShard-Agent',
         'Polycentric-Orchestrator', 'Manifold-Projection', 'FractalOS-runtime')


def manifest():
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    repos = data['repositories']
    if [r['name'] for r in repos] != list(NAMES):
        raise ValueError('manifest must declare the exact seven repositories in order')
    extras = data.get('external_integrations', [])
    if len(extras) != 1 or extras[0]['name'] != 'BioChain-AI' or extras[0]['required']:
        raise ValueError('legacy BioChain-AI must remain optional')
    for repo in repos + extras:
        name = repo['name']
        if repo['git_url'] != f'https://github.com/BioChainAI/{name}.git':
            raise ValueError('unexpected repository URL for ' + name)
        if repo['relative_path'] != 'workspaces/' + name:
            raise ValueError('unexpected workspace path for ' + name)
    graph = {r['name']: r['dependencies'] for r in repos}
    done, active = set(), set()

    def visit(name):
        if name in active or name not in graph:
            raise ValueError('cyclic or unknown dependency: ' + name)
        if name in done:
            return
        active.add(name)
        for dep in graph[name]:
            visit(dep)
        active.remove(name)
        done.add(name)
    for name in graph:
        visit(name)
    return data


def git(*args, cwd=None, check=False):
    result = subprocess.run(['git', *args], cwd=cwd, text=True, capture_output=True)
    if check and result.returncode:
        # Do not echo remote configuration or potentially credential-bearing stderr.
        raise RuntimeError('Git operation failed: ' + args[0])
    return result


def targets(include_optional=False):
    data = manifest()
    return data['repositories'] + (data['external_integrations'] if include_optional else [])


def folder(repo):
    workspace = BASE / 'workspaces'
    path = BASE / repo['relative_path']
    if workspace.is_symlink() or path.is_symlink():
        raise ValueError('symlink workspace refused')
    if workspace.resolve().parent != BASE.resolve() or path.resolve().parent != workspace.resolve():
        raise ValueError('unsafe workspace path')
    return path


def inventory():
    workspace = BASE / 'workspaces'
    if workspace.is_symlink():
        raise ValueError('symlink workspace refused')
    allowed = {r['name'] for r in targets(True)}
    if workspace.exists():
        for path in workspace.iterdir():
            if path.name == '.gitignore' and path.is_file() and not path.is_symlink():
                continue
            if path.name not in allowed or path.is_symlink() or not path.is_dir():
                raise RuntimeError('unrecognized workspace entry: ' + path.name)
    # Validate optional checkout as well if already present; never ignore dirty data.
    return {r['name']: inspect(r) for r in targets(True) if folder(r).exists()}


def inspect(repo):
    path = folder(repo)
    if not (path / '.git').exists():
        raise RuntimeError(repo['name'] + ' is not an independent Git checkout')
    top = git('rev-parse', '--show-toplevel', cwd=path, check=True).stdout.strip()
    if Path(top).resolve() != path.resolve():
        raise RuntimeError('checkout root mismatch: ' + repo['name'])
    origin = git('remote', 'get-url', 'origin', cwd=path, check=True).stdout.strip()
    if origin != repo['git_url']:
        raise RuntimeError('unrecognized origin: ' + repo['name'])
    status = git('status', '--porcelain=v1', '--untracked-files=all', cwd=path, check=True)
    if status.stdout.strip():
        raise RuntimeError(repo['name'] + ' has uncommitted/untracked changes; preserved')
    sha = git('rev-parse', '--verify', 'HEAD^{commit}', cwd=path, check=True).stdout.strip()
    if not re.fullmatch('[0-9a-f]{40}', sha):
        raise RuntimeError('invalid commit identity: ' + repo['name'])
    return {'git_url': repo['git_url'], 'commit': sha}


def manifest_digest():
    data = json.dumps(manifest(), sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(data).hexdigest()


def read_lock(required=False):
    if not LOCK.exists():
        if required:
            raise RuntimeError('no reviewed lock: run lock after testing')
        return None
    data = json.loads(LOCK.read_text())
    if data.get('schema') != SCHEMA or data.get('manifest_sha256') != manifest_digest():
        raise RuntimeError('lock schema/manifest mismatch')
    commits = data.get('repositories', {})
    if set(commits) != set(NAMES):
        raise RuntimeError('lock repository set is incomplete or unknown')
    for repo in targets():
        item = commits[repo['name']]
        if item.get('git_url') != repo['git_url'] or not re.fullmatch('[0-9a-f]{40}', item.get('commit', '')):
            raise RuntimeError('invalid lock identity: ' + repo['name'])
    return data


def report():
    print('Seven independent dependencies (Geometric-Labs is the eighth repository):')
    for repo in targets():
        print(repo['name'], repo['role'], repo['git_url'])
    print('BioChain-AI: optional legacy adapter, excluded by default')
    return 0


def doctor():
    print('Python:', sys.version.split()[0], 'Git:', shutil.which('git'))
    print('C compiler:', shutil.which('cc') or 'missing (protocol gate requires C11)')
    present = inventory()
    for repo in targets():
        item = present.get(repo['name'])
        print('FOUND' if item else 'MISSING', repo['name'], item['commit'] if item else '')
    print(f'{len(set(present) & set(NAMES))}/7 core checkouts')
    if LOCK.exists():
        check_lock()
    return 0 if all(name in present for name in NAMES) else 1


def sync(include_optional=False, require_lock=False):
    if not shutil.which('git'):
        raise RuntimeError('Git executable unavailable')
    pinned = read_lock(required=require_lock)
    present = inventory()  # Validate every existing checkout before any clone.
    if pinned:
        for name, item in present.items():
            if name in NAMES and item != pinned['repositories'][name]:
                raise RuntimeError('existing checkout differs from lock; preserved: ' + name)
    (BASE / 'workspaces').mkdir(exist_ok=True)
    for repo in targets(include_optional):
        name = repo['name']
        if name in present:
            print('KEEP', name, '(no pull/reset/checkout)')
            continue
        path = folder(repo)
        print('CLONE', name, flush=True)
        git('clone', '--', repo['git_url'], str(path), check=True)
        if pinned and name in NAMES:
            sha = pinned['repositories'][name]['commit']
            if git('cat-file', '-e', sha + '^{commit}', cwd=path).returncode:
                git('fetch', 'origin', sha, cwd=path, check=True)
            # Only a newly created clone may be moved to its reviewed commit.
            git('checkout', '--detach', sha, cwd=path, check=True)
        item = inspect(repo)
        if pinned and name in NAMES and item != pinned['repositories'][name]:
            raise RuntimeError('new clone failed pinned restore: ' + name)
    return 0


def collect_lock():
    present = inventory()
    if not all(name in present for name in NAMES):
        raise RuntimeError('missing core checkouts: run sync')
    return {name: present[name] for name in NAMES}


def lock(refresh=False):
    commits = collect_lock()
    output = {'schema': SCHEMA, 'source_manifest': 'manifest/repositories.v1.json',
              'manifest_sha256': manifest_digest(), 'repositories': commits}
    current = read_lock()
    if current == output:
        print('LOCK UNCHANGED (7 repositories)')
        return 0
    if current is not None and not refresh:
        raise RuntimeError('lock advancement requires explicit --refresh-lock after tests/review')
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    temporary = LOCK.with_suffix('.tmp')
    with temporary.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(output, indent=2, sort_keys=True) + '\n')
    temporary.replace(LOCK)
    print('WROTE reviewed-candidate lock (7 repositories; not a publication)')
    return 0


def check_lock(quiet=False):
    data = read_lock(required=True)
    current = collect_lock()
    if current != data['repositories']:
        raise RuntimeError('lock differs from checked-out commits/URLs')
    if not quiet:
        print('LOCK OK (7 clean independent checkouts)')
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['list', 'doctor', 'sync', 'lock', 'check-lock', 'profiles'])
    parser.add_argument('--include-optional', action='store_true')
    parser.add_argument('--require-lock', action='store_true')
    parser.add_argument('--refresh-lock', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'list':
            return report()
        if args.command == 'profiles':
            print((BASE / 'environments/repository_profiles.v1.json').read_text())
            return 0
        if args.command == 'doctor':
            return doctor()
        if args.command == 'sync':
            return sync(args.include_optional, args.require_lock)
        if args.command == 'lock':
            return lock(args.refresh_lock)
        return check_lock()
    except (ValueError, RuntimeError, OSError, KeyError, TypeError) as error:
        print('ERROR:', str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
