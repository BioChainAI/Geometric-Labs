"""Placeholder; replace with baseline, negative and vector tests."""
from pathlib import Path
import sys
HERE = Path(__file__).resolve()
sys.path[:0] = [str(HERE.parents[1] / "src"), str(HERE.parents[4] / "src")]
import unittest
import {{PACKAGE}}


class TestScaffold(unittest.TestCase):
    def test_identity(self):
        self.assertEqual({{PACKAGE}}.RESEARCH_ID, "{{ID}}")


if __name__ == "__main__":
    unittest.main()
