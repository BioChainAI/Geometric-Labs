import importlib.util
from pathlib import Path
import unittest

class EnvironmentInteroperability(unittest.TestCase):
    def test_image_to_independent_agents_and_orchestrator(self):
        path=Path(__file__).resolve().parents[1]/'tools/interop.py'
        spec=importlib.util.spec_from_file_location('geot_interop',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        report=module.run()
        self.assertEqual(report['accepted_visual_sidecars'],3)
        self.assertEqual(report['fixture_triangle_tqf'],576)
        self.assertFalse(report['trained'])
        self.assertFalse(report['remote_visual_schema_enforced'])
        self.assertEqual(len(report['independent_import_origins']),4)
        self.assertEqual(report['tile_form_id'],3)
        self.assertEqual(report['descriptor_bytes_per_agent'],[16384]*3)
