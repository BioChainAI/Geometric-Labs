"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.threading.torus_soliton_mux import *
from geometric_labs.threading.tqf_stream_pruner import *
import random

class Verification(unittest.TestCase):
    def test_covering_and_disjoint_rectangles(self):
        self.assertEqual(J_G[0]*J_G[3]-J_G[1]*J_G[2],14)
        self.assertEqual(covering_determinants(),[7,161,2569,37513,533057])
        for count in (0,1,12,64): self.assertTrue(rectangles_disjoint(allocate_rectangles(count)))
        self.assertFalse(rectangles_disjoint([(Fraction(0),Fraction(1),Fraction(0),Fraction(1))]*2))
        graph={0:{1,2},1:{0,2},2:{0,1,3},3:{2}}
        colors=color_conflicts(graph)
        for u,neighbors in graph.items():
            for v in neighbors: self.assertNotEqual(colors[u],colors[v])
        self.assertLessEqual(len(set(colors.values())),max(map(len,graph.values()))+1)

    def test_lossless_pruning(self):
        raw=[10,15,20,25,30,28,26,24,35,50]
        knots=prune(raw)
        self.assertEqual(len(knots),5)
        self.assertEqual(interpolate(knots,len(raw)),raw)
        rng=random.Random(8)
        for n in (0,1,2,10,100):
            for raw in ([3*k+7 for k in range(n)],[rng.randrange(-100,100) for _ in range(n)]):
                self.assertEqual(interpolate(prune(raw),len(raw)),raw)
        with self.assertRaises(ValueError): interpolate([(0,0),(2,1)],3)
        with self.assertRaises(ValueError): interpolate([(0,0),(0,1)],1)


if __name__ == "__main__":
    unittest.main()
