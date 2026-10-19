import json
import pathlib
import sys
import tempfile
import unittest

BASE=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'tools'))
import glab

class TestManifest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.m=glab.manifest()

    def test_exact_seven_core_repos(self):
        names=[r['name'] for r in self.m['repositories']]
        self.assertEqual(names,['SHD-CCP-core','Kernel-Registry','CubiLoom','PolyShard-Agent',
                                'Polycentric-Orchestrator','Manifold-Projection','FractalOS-runtime'])
        self.assertEqual(len(set(names)),7)

    def test_real_github_org_and_paths(self):
        for repo in glab.targets():
            self.assertEqual(repo['git_url'],f'https://github.com/BioChainAI/{repo["name"]}.git')
            self.assertEqual(glab.folder(repo).parent,BASE/'workspaces')
            self.assertTrue(repo['required'])

    def test_dependency_graph_acyclic(self):
        graph={r['name']:r['dependencies'] for r in glab.targets()}
        done=set();active=set()
        def visit(n):
            if n in done:return
            self.assertNotIn(n,active,'dependency cycle')
            active.add(n)
            for dep in graph[n]:
                self.assertIn(dep,graph)
                visit(dep)
            active.remove(n);done.add(n)
        for n in graph:visit(n)

    def test_legacy_is_not_required(self):
        self.assertEqual(self.m['external_integrations'][0]['name'],'BioChain-AI')
        self.assertFalse(self.m['external_integrations'][0]['required'])
        self.assertEqual(len(glab.targets(include_optional=True)),8)
        self.assertEqual(len(glab.targets()),7)

    def test_source_of_truth_contains_unique_ownership(self):
        owners=set(self.m['source_of_truth'].values())
        self.assertTrue(owners.issubset({r['name'] for r in self.m['repositories']}|{'Geometric-Labs'}))
        self.assertEqual(self.m['source_of_truth']['tile_fields'],'SHD-CCP-core')

    def test_demo_requires_four_repo_contracts(self):
        self.assertEqual(set(self.m['demo_requirements']),{'SHD-CCP-core','PolyShard-Agent',
                           'Polycentric-Orchestrator','Manifold-Projection'})

if __name__=='__main__':unittest.main()
