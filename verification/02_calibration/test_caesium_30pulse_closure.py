"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.calibration.chronometry_window import *
from math import prod

class Verification(unittest.TestCase):
    def test_factorization_and_closure(self):
        self.assertEqual(prod(p**e for p,e in CS_FACTORIZATION.items()),NU_CS)
        self.assertEqual(Fraction(NU_CS,W_SIGMA)%1,PARITY_RESIDUAL)
        pulses,seconds=joint_closure([NU_CS,40,432])
        self.assertEqual((pulses,seconds),(30,Fraction(1,2)))
        self.assertEqual(NU_CS*seconds,4596315885)
        for k in range(1,pulses): self.assertTrue(any((k*f)%60 for f in (NU_CS,40,432)))

    def test_general_carriers(self):
        self.assertEqual(joint_closure([60]),(1,Fraction(1,60)))
        self.assertEqual(joint_closure([7],100),(100,Fraction(1)))
        with self.assertRaises(ValueError): joint_closure([])


if __name__ == "__main__":
    unittest.main()
