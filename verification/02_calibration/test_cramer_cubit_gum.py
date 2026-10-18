"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.calibration.acoustic_cubit import *

class Verification(unittest.TestCase):
    def test_cubit_and_temperature(self):
        self.assertAlmostEqual(local_cubit(20)*100,53.7476,places=4)
        derivative=(local_cubit(20.001)-local_cubit(19.999))/.002
        self.assertAlmostEqual(derivative,.00098,delta=.00003)
        for t in (0,5,15,20,30):
            v=cramer_sound_speed(t)
            self.assertAlmostEqual(v/(2*4*local_cubit(t)),room_mode((1,0,0),(4,4,4)),places=11)
        self.assertEqual(room_mode((1,0,0),(4,4,4)),80.)

    def test_six_term_gum(self):
        u,U=gum_uncertainty((1,2,3,4,5,6),(.1,.1,.1,.1,.1,.1))
        self.assertAlmostEqual(u*u,.91)
        self.assertEqual(U,2*u)
        with self.assertRaises(ValueError): gum_uncertainty((1,),(.1,))
        with self.assertRaises(ValueError): cramer_sound_speed(31)
        with self.assertRaises(ValueError): local_cubit(20,f_cal=0)


if __name__ == "__main__":
    unittest.main()
