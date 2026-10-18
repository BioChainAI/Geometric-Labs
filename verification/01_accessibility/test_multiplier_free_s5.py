"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.s5_hyperbolic_tree import *
from geometric_labs.hurwitz import h_mul
import random

class Verification(unittest.TestCase):
    def test_random_reduced_words(self):
        rng=random.Random(20261017)
        for depth in range(1,13):
            for _ in range(30):
                word=[];q=(1,0,0,0)
                for _ in range(depth):
                    label=rng.choice([g for g in S5_GENS if not word or g!=OPPOSITE[word[-1]]])
                    before=q;q=step_s5_shift_add(q,label);word.append(label)
                    exact=h_mul(tuple(2*c for c in before),tuple(2*c for c in S5_GENS[label]))
                    self.assertEqual(tuple(2*c for c in q),exact)
                self.assertEqual(recover_s5_word(q,depth),word)
                self.assertEqual(sum(c*c for c in q),5**depth)
        self.assertEqual(abelian_shadow(['+i','+j','-i']), (0,1,0))
        self.assertEqual(recover_s5_word((1,0,0,0),0),[])

    def test_invalid_addresses(self):
        with self.assertRaises(ValueError): recover_s5_word((5,0,0,0),2)
        with self.assertRaises(ValueError): recover_s5_word((1,0,0,0),1)
        with self.assertRaises(ValueError): step_s5_shift_add((1,0,0,0),'x')


if __name__ == "__main__":
    unittest.main()
