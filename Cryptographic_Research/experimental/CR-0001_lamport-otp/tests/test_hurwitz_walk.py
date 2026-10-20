"""Track E1: the exact quaternion walk is a bijection, so it is not one-way."""
from pathlib import Path
import sys
HERE = Path(__file__).resolve()
sys.path[:0] = [str(HERE.parents[1] / "src"), str(HERE.parents[4] / "src")]
import random
import unittest
from geometric_labs.hurwitz import HURWITZ_24_UNITS, h_mul, h_norm
from geometric_lamport.hurwitz_walk import (GENERATORS, digest_to_path, invert_walk,
                                            path_to_digest, recover_digest, walk_encode,
                                            walk_length, walk_product)
from geometric_lamport.lamport import LamportClient


class TestWalk(unittest.TestCase):
    def test_generators(self):
        self.assertTrue(all(h_norm(g) == 5 for g in GENERATORS))
        # One representative per left-unit class, so divisors are unambiguous.
        classes = {min(h_mul(u, g) for u in HURWITZ_24_UNITS) for g in GENERATORS}
        self.assertEqual(len(classes), 6)
        self.assertEqual(walk_length(32), 111)
        self.assertEqual(walk_length(1), 4)

    def test_path_encoding_is_a_bijection(self):
        rng = random.Random(1981)
        for size in (1, 2, 8, 32):
            for _ in range(50):
                digest = bytes(rng.randrange(256) for _ in range(size))
                path = digest_to_path(digest)
                self.assertTrue(all(b != a ^ 1 for a, b in zip(path, path[1:])))
                self.assertEqual(path_to_digest(path, size), digest)
        self.assertEqual(len({tuple(digest_to_path(bytes([b]))) for b in range(256)}), 256)

    def test_backtracking_path_rejected(self):
        path = digest_to_path(bytes(32))
        path[1] = path[0] ^ 1
        with self.assertRaises(ValueError):
            path_to_digest(path, 32)

    def test_product_norm(self):
        q = walk_encode(bytes(range(32)))
        self.assertEqual(h_norm(q), 5 ** 111)


class TestPreimageAttack(unittest.TestCase):
    def test_random_walks_invert_uniquely(self):
        rng = random.Random(5)
        for _ in range(100):
            digest = rng.randbytes(32)
            path = digest_to_path(digest)
            self.assertEqual(invert_walk(walk_product(path), len(path)), path)
            self.assertEqual(recover_digest(walk_encode(digest), 32), digest)

    def test_walk_anchor_leaks_the_next_password(self):
        # If a server stored walk_encode(h(n-1)) as a geometric anchor, any
        # reader of the anchor would log in as the client.
        client = LamportClient(b"victim seed", 5)
        password = client.password_for(4)
        self.assertEqual(recover_digest(walk_encode(password), 32), password)

    def test_invert_rejects_non_walks(self):
        with self.assertRaises(ValueError):
            invert_walk((2, 4, 0, 0), 2)
        with self.assertRaises(ValueError):
            invert_walk((10, 0, 0, 0), 2)  # g * conj(g): a backtracking walk


if __name__ == "__main__":
    unittest.main()
