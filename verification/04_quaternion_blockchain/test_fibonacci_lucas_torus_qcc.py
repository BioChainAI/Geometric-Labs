"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.blockchain.toroidal_state_matrix import *
from geometric_labs.hurwitz import h_norm

class Verification(unittest.TestCase):
    def test_lucas_checkpoints(self):
        self.assertEqual([h_norm(checkpoint(m)) for m in range(1,9)],[3,7,18,47,123,322,843,2207])
        for m in range(1,100): self.assertEqual(h_norm(checkpoint(m)),lucas(2*m))

    def test_two_sided_phase_quadrances(self):
        for m in range(1,20):
            q=checkpoint(m)
            r=two_sided_update(q,(0,2,0,0),(-2,0,0,0))
            self.assertEqual(sum(x*x for x in q[:2]),sum(x*x for x in r[:2]))
            self.assertEqual(sum(x*x for x in q[2:]),sum(x*x for x in r[2:]))
        with self.assertRaises(ValueError): two_sided_update(checkpoint(1),(0,0,2,0),(2,0,0,0))


if __name__ == "__main__":
    unittest.main()
