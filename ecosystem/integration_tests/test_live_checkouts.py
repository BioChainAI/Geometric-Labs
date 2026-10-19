"""Pinned integration lane: missing tools/checkouts are failures, never fake passes."""
import importlib.util
from pathlib import Path
import sys
import unittest

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'tools'))
import glab
from protocol_compatibility import run_gate
from upstreams import load


class LiveCheckouts(unittest.TestCase):
    def test_c_python_structural_conformance(self):
        report = run_gate()
        self.assertEqual(report['packet_cases'],183)
        self.assertFalse(report['semantic_compatible'])
        self.assertEqual(len(report['semantic_gaps']),4)

    def test_loopback_three_agents_and_negative_admission(self):
        spec = importlib.util.spec_from_file_location('reference_mesh',BASE/'simulator/reference_mesh.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        report = module.run_mesh()
        self.assertEqual(report['tqf_area16'],576)
        self.assertEqual(report['accepted_events'],3)
        self.assertEqual(len(report['negative_fixtures']),11)
        self.assertFalse(report['private_rag_exported'])
        self.assertEqual(len(report['import_origins']),4)

    def test_registry_does_not_self_certify_or_overwrite_header(self):
        load(['Kernel-Registry'])
        from kernel_registry.linter import validate_candidate
        valid = {'status':'CANDIDATE','form_id':15,'fields':[{'lsb':0,'width':32}],
                 'coder_hash':'sha256:reference-only','test_vectors_hash':'sha256:reference-only'}
        self.assertEqual(validate_candidate(valid),(True,'candidate_structurally_valid_only'))
        self.assertEqual(validate_candidate(valid|{'status':'CERTIFIED'}),(False,'self_certification_forbidden'))
        self.assertEqual(validate_candidate(valid|{'fields':[{'lsb':40,'width':4}]}),(False,'fixed_header_overwrite'))

    def test_clean_release_lock(self):
        self.assertEqual(glab.check_lock(),0)


if __name__=='__main__':
    unittest.main()
