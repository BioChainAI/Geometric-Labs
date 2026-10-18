"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.hurwitz import *
import random

class Verification(unittest.TestCase):
    def test_cancellation(self):
        u=(10**6,1,0,0);v=(2*10**6+1,2,0,0)
        self.assertEqual(gram_tqf(u,v),4)
        qs=[float(sum(c*c for c in t)) for t in (u,v,tuple(a-b for a,b in zip(u,v)))]
        self.assertNotEqual(sum(qs)**2-2*sum(q*q for q in qs),4.)

    def test_exact_and_unbounded(self):
        self.assertEqual(gram_tqf((10**100,1),(10**100+1,1)),4)
        self.assertEqual(gram_tqf((1,2),(2,4)),0)
        with self.assertRaises(ValueError): gram_tqf((1,), (1,2))

    def test_hurwitz_group_and_ring(self):
        self.assertEqual(len(set(HURWITZ_24_UNITS)),24)
        for a in HURWITZ_24_UNITS:
            self.assertEqual(h_mul(a,h_inv_unit(a)),H_ONE)
            for b in HURWITZ_24_UNITS:
                self.assertIn(h_mul(a,b),HURWITZ_24_UNITS)
        rng=random.Random(42)
        for _ in range(200):
            p=tuple(2*rng.randrange(-100,100)+1 for _ in range(4))
            q=tuple(2*rng.randrange(-100,100) for _ in range(4))
            self.assertEqual(h_norm(h_mul(p,q)),h_norm(p)*h_norm(q))
            r=rng.choice(HURWITZ_24_UNITS)
            self.assertEqual(h_mul(h_mul(p,q),r),h_mul(p,h_mul(q,r)))
            self.assertEqual(canonical_associate(p),canonical_associate(h_mul(r,p)))
        with self.assertRaises(ValueError): h_norm((1,0,0,0))
        with self.assertRaises(ValueError): h_inv_unit((4,0,0,0))


if __name__ == "__main__":
    unittest.main()
