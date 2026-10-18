"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.threading.cubocta_12engine_ring import *
from geometric_labs.hurwitz import HURWITZ_24_UNITS, h_norm
import random

class Verification(unittest.TestCase):
    def test_all_cyclic_single_erasures(self):
        rng=random.Random(13)
        self.assertEqual(len(set(CUBOCTA_RING)),12)
        self.assertTrue(all(sum(x*x for x in p)==2 for p in CUBOCTA_RING))
        for _ in range(100):
            g=close_group([rng.choice(HURWITZ_24_UNITS) for _ in range(3)])
            for slot in range(4):
                erased=list(g);erased[slot]=None
                self.assertEqual(recover_single(erased),g[slot])

    def test_cascade_and_tier(self):
        groups=[close_group(list(HURWITZ_24_UNITS[k:k+3])) for k in (3,9,17)]
        star=global_fourth([g[3] for g in groups])
        for group in range(3):
            for slot in range(3):
                erased=[list(g) for g in groups]
                erased[group][slot]=erased[group][3]=None
                self.assertEqual(cascade_recover(erased,star),groups)
        self.assertEqual(tier_word(),H_ONE)
        self.assertEqual(ONLOAD_SCALE*OFFLOAD_SCALE,1)
        for q in ((6,-10,14,22),(1,3,5,7)):
            self.assertEqual(offload_recall(q),q)
            self.assertEqual(h_norm(h_mul(H_TIER,q)),h_norm(q))
        with self.assertRaises(ValueError): recover_single([None,None,H_ONE,H_ONE])


if __name__ == "__main__":
    unittest.main()
