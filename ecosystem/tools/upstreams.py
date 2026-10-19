"""Load actual independently pinned source checkouts; reject package shadowing."""
import importlib
import sys
from pathlib import Path

import glab

# Dependency checkouts are read-only inputs; avoid creating untracked bytecode.
sys.dont_write_bytecode = True

PACKAGES = {'SHD-CCP-core': 'shdccp_core', 'Kernel-Registry': 'kernel_registry',
            'PolyShard-Agent': 'polyshard_agent', 'Polycentric-Orchestrator': 'polycentric',
            'Manifold-Projection': 'manifold_projection'}


def load(names=None):
    names = names or tuple(PACKAGES)
    glab.inventory()
    if glab.LOCK.exists():
        glab.check_lock(quiet=True)
    repos = {r['name']: r for r in glab.targets()}
    for name in names:
        source = glab.folder(repos[name]) / 'src'
        if not source.is_dir():
            raise RuntimeError('missing independent src checkout: ' + name)
        sys.path.insert(0, str(source))
    origins = {}
    for name in names:
        package = PACKAGES[name]
        module = importlib.import_module(package)
        origin = Path(module.__file__).resolve()
        expected = (glab.folder(repos[name]) / 'src' / package).resolve()
        if not origin.is_relative_to(expected):
            raise RuntimeError('package shadowing refused: ' + package)
        origins[package] = str(origin.relative_to(glab.BASE))
    return origins
