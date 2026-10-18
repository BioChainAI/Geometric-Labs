"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.certification.wheel_30_oracle import *
from geometric_labs.certification.prime_anchor_cert import is_prime_64

class Verification(unittest.TestCase):
    def test_wheel_bias_and_legendre_split(self):
        self.assertEqual(WHEEL_UNITS,(1,7,11,13,17,19,23,29))
        self.assertEqual(B_PLUS,(1,11,19,29))
        self.assertEqual(B_MINUS,(7,13,17,23))
        self.assertTrue(verify_bias())
        self.assertEqual(ORACLE_BIAS,Fraction(15,4))

    def test_geometry_is_not_a_certificate(self):
        for n in (49,77,121):
            self.assertTrue(wheel_candidate(n))
            self.assertFalse(is_prime_64(n))
        for n in range(7,200):
            if is_prime_64(n): self.assertTrue(wheel_candidate(n))


if __name__ == "__main__":
    unittest.main()
