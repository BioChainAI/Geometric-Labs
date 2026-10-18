"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.garner_crt import *
import random

class Verification(unittest.TestCase):
    def test_default_and_general_triplets(self):
        self.assertEqual(closed_form_inverses(),(441,665,739))
        rng=random.Random(881883887)
        for p in (5,11,17,101,881):
            mod=p*(p+2)*(p+6)
            for x in [0,1,mod-1]+[rng.randrange(mod) for _ in range(1000)]:
                self.assertEqual(decode(encode(x,p),p),x)

    def test_reject_noncanonical(self):
        for x in (-1,MODULUS):
            with self.assertRaises(ValueError): encode(x)
        with self.assertRaises(ValueError): decode((881,0,0))
        with self.assertRaises(ValueError): closed_form_inverses(3)


if __name__ == "__main__":
    unittest.main()
