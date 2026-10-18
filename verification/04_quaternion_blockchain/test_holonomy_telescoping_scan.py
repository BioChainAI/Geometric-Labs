"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.blockchain.holonomy_prefix_scan import *
from geometric_labs.blockchain.qcc_delta_chain import *
from geometric_labs.hurwitz import HURWITZ_24_UNITS
import random

class Verification(unittest.TestCase):
    def test_noncommuting_prefix_all_sizes(self):
        rng=random.Random(19)
        for n in (0,1,2,3,7,12,72,719,720):
            items=[rng.choice(HURWITZ_24_UNITS) for _ in range(n)]
            expected=[];q=H_ONE
            for x in items:
                q=h_mul(q,x);expected.append(q)
            self.assertEqual(prefix_scan(items),expected)
        i=(0,2,0,0);j=(0,0,2,0)
        self.assertNotEqual(product([i,j]),product([j,i]))

    def test_open_boundary_nonidentity_holonomy(self):
        rng=random.Random(721)
        chain=[rng.choice(HURWITZ_24_UNITS) for _ in range(720)]
        chain[0]=H_ONE;chain[-1]=(0,2,0,0)
        deltas=encode_chain(chain)
        self.assertEqual(decode_chain(chain[0],deltas),chain)
        result=holonomy(chain)
        self.assertNotEqual(result['holonomy'],H_ONE)
        self.assertEqual(result['holonomy'],h_inv_unit(chain[-1]))
        self.assertEqual([len(g) for g in middle_gear_partition()],[8,7,7,7,7,8,7,7,7,7])
        with self.assertRaises(ValueError): decode_chain(H_ONE,[(0,2,0,0)])


if __name__ == "__main__":
    unittest.main()
