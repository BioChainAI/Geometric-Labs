"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.threading.supercycle_24step import *
import random

class Verification(unittest.TestCase):
    def test_scheduler(self):
        self.assertEqual(SUPER_CYCLE,24)
        self.assertEqual(len({schedule(k)[:2] for k in range(24)}),24)
        self.assertEqual([k for k in range(24) if schedule(k)[2]=='onload'],[2,10,18])
        for k in range(24): self.assertEqual(schedule(k),schedule(k+24))

    def test_exact_phase_roundtrips(self):
        rng=random.Random(24)
        for _ in range(1000):
            values=tuple(rng.randrange(-10**50,10**50) for _ in range(3))
            s,z=split_phases(*values)
            self.assertEqual(join_phases(s,z),values)
            self.assertEqual(rotate_plane(rotate_plane(rotate_plane(z))),z)
            self.assertEqual(split_phases(values[2],values[0],values[1]),(s,rotate_plane(z)))
        with self.assertRaises(ValueError): join_phases(1,(0,0))


if __name__ == "__main__":
    unittest.main()
