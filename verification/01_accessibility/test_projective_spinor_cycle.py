"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.hurwitz import projective_spinor_cycle, H_TIER, H_ONE, H_NEG_ONE, h_mul

class Verification(unittest.TestCase):
    def test_eight_steps(self):
        self.assertEqual(projective_spinor_cycle(),[(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0)])

    def test_tier_is_order_six_not_three(self):
        q=H_ONE
        for _ in range(3): q=h_mul(q,H_TIER)
        self.assertEqual(q,H_NEG_ONE)
        for _ in range(3): q=h_mul(q,H_TIER)
        self.assertEqual(q,H_ONE)


if __name__ == "__main__":
    unittest.main()
