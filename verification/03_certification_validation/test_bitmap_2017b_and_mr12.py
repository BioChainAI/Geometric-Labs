"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.certification.prime_anchor_cert import *

class Verification(unittest.TestCase):
    def test_bitmap_against_trial_division(self):
        self.assertEqual(len(PRIME_BITMAP),2017)
        count=0
        for n in range(16130):
            trial=n>=2 and all(n%d for d in range(2,isqrt(n)+1))
            self.assertEqual(bitmap_is_prime(n),trial)
            self.assertEqual(is_prime_64(n),trial)
            count+=trial
        self.assertEqual(count,1877)
        self.assertEqual(hurwitz_box_primes(),[2,3,5,7,13])

    def test_large_primes_pseudoprimes_and_bounds(self):
        for n in (341,561,3215031751,341550071728321,3825123056546413051,2**64-1):
            self.assertFalse(is_prime_64(n))
        self.assertTrue(is_prime_64(18446744073709551557))
        for n in (-1,2**64):
            with self.assertRaises(ValueError): is_prime_64(n)
        with self.assertRaises(ValueError): bitmap_is_prime(16130)


if __name__ == "__main__":
    unittest.main()
