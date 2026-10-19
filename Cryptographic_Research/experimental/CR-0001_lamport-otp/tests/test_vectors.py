"""Committed golden vectors reproduce and are internally consistent."""
from pathlib import Path
import sys
HERE = Path(__file__).resolve()
sys.path[:0] = [str(HERE.parents[1] / "src"), str(HERE.parents[4] / "src"), str(HERE.parents[1] / "vectors")]
import json
import unittest
import generate_vectors
from geometric_lamport.hurwitz_walk import recover_digest
from geometric_lamport.lamport import LamportServer
from geometric_lamport.tile_frame import FrameVerifier


class TestGoldenVectors(unittest.TestCase):
    def setUp(self):
        self.vectors = json.loads(generate_vectors.OUTPUT.read_text())

    def test_no_drift(self):
        self.assertEqual(generate_vectors.OUTPUT.read_text(), generate_vectors.render())

    def test_frames_replay_a_full_session(self):
        data = self.vectors["data"]
        server = LamportServer(bytes.fromhex(data["chain_hex"][-1]), data["length"])
        verifier = FrameVerifier(server, **data["routing"])
        for frame in data["frames_in_login_order"]:
            self.assertTrue(verifier.verify_frame([int(t, 16) for t in frame["tiles"]]))
        self.assertEqual(server.remaining, 0)

    def test_walk_negative_control_inverts(self):
        walk = self.vectors["data"]["walk_negative_control"]
        self.assertEqual(recover_digest(tuple(walk["product"]), 32).hex(), walk["input_hex"])


if __name__ == "__main__":
    unittest.main()
