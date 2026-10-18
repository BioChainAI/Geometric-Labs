"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.threading.balancer_64stream import *
from geometric_labs.threading.cubocta_12engine_ring import close_group
from geometric_labs.hurwitz import HURWITZ_24_UNITS
import random

class Verification(unittest.TestCase):
    def test_64_routes_and_invariants(self):
        rng=random.Random(64)
        for _ in range(100):
            inputs=sum([close_group([rng.choice(HURWITZ_24_UNITS) for _ in range(3)]) for _ in range(3)],[])
            model=build_balancer(inputs)
            self.assertTrue(all(verify_balancer(model).values()))
            streams=projection_streams(model)
            self.assertEqual(set(streams),set(range(64)))
            self.assertEqual(streams[12],tuple(q[0] for q in inputs))
            model['E'][0]=tuple(-c for c in model['E'][0])
            self.assertFalse(verify_balancer(model)['slot_closure'])
        with self.assertRaises(ValueError): stream_id(4,0)
        with self.assertRaises(ValueError): build_balancer([H_ONE]*11)


if __name__ == "__main__":
    unittest.main()
