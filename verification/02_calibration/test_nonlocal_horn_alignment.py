"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.calibration.horn_frame_solver import *
from geometric_labs.hurwitz import H_TIER

class Verification(unittest.TestCase):
    def test_coherence_sign_and_frame_invariance(self):
        qs=[(1,2,3,4),(-2,0,1,3),(3,1,2,0),(0,1,1,1)]
        baseline=phi_m_coherence(qs)
        flipped=[tuple((-1 if i%2 else 1)*x for x in q) for i,q in enumerate(qs)]
        rotated=[(q[1],-q[0],q[3],-q[2]) for q in qs]
        self.assertAlmostEqual(baseline,phi_m_coherence(flipped),places=12)
        self.assertAlmostEqual(baseline,phi_m_coherence(rotated),places=12)
        self.assertAlmostEqual(phi_m_coherence([(1,0,0,0),(-1,0,0,0)]),1.)
        self.assertAlmostEqual(phi_m_coherence([(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]),.25)
        with self.assertRaises(ValueError): phi_m_coherence([(0,0,0,0)])

    def test_horn_fit_and_exact_snap(self):
        a=[(0,1,2,0),(0,3,1,0),(0,2,1,2),(0,0,4,1),(0,3,0,2),(0,1,1,3)]
        b=[rotate_anchor(p,H_TIER) for p in a]
        perm=[3,0,5,1,4,2]
        self.assertEqual(match_signatures(a,[b[i] for i in perm]),perm)
        fitted=horn_rotation([p[1:] for p in a],[p[1:] for p in b])
        snapped=snap_hurwitz(fitted)
        self.assertEqual([rotate_anchor(p,snapped) for p in a],b)
        with self.assertRaises(ValueError): match_signatures([(1,0),(0,1)],[(1,0),(0,1)])



class FullOctahedralAlignment(unittest.TestCase):
    def test_all_24_rotations_including_quarter_turns(self):
        self.assertEqual(len(set(OCTAHEDRAL_24)),24)
        anchors=[(1,2,0),(3,1,0),(2,1,2),(0,4,1),(3,0,2),(1,1,3)]
        perm=[3,0,5,1,4,2]
        for matrix in OCTAHEDRAL_24:
            b=[apply_rotation(matrix,anchors[i]) for i in perm]
            matching,found=align_octahedral(anchors,b)
            self.assertEqual(matching,perm)
            self.assertEqual(found,matrix)

if __name__ == "__main__":
    unittest.main()
