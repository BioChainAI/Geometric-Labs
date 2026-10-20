"""Track E3: nine-tile OTP frames, positive and negative fixtures."""
from pathlib import Path
import sys
HERE = Path(__file__).resolve()
sys.path[:0] = [str(HERE.parents[1] / "src"), str(HERE.parents[4] / "src")]
import unittest
from geometric_labs.tile_codec import decode_tile, encode_tile, match_south_halo
from geometric_lamport.lamport import LamportClient, LamportServer
from geometric_lamport.tile_frame import (FRAME_TILES, MAX_INDEX, FrameVerifier,
                                          decode_frame, encode_frame)

ROUTING = {"cycle_step": 5, "wheel_idx": 2, "struct_sel": 1, "gate_byte": 0xA5,
           "stream_slot": 9, "scale_reg": 3}
PASSWORD = bytes(range(32))


class TestFrameCodec(unittest.TestCase):
    def test_round_trip(self):
        for index in (0, 1, 880, 881, MAX_INDEX):
            tiles = encode_frame(index, PASSWORD, **ROUTING)
            self.assertEqual(len(tiles), FRAME_TILES)
            self.assertTrue(all(0 <= t < 2**64 for t in tiles))
            self.assertEqual(decode_frame(tiles), (index, PASSWORD, ROUTING))

    def test_layout(self):
        tiles = encode_frame(7, PASSWORD, **ROUTING)
        fields = [decode_tile(t) for t in tiles]
        self.assertEqual([f["step_mux"] for f in fields], list(range(9)))
        self.assertEqual([f["form_id"] for f in fields], [2] + [0] * 8)
        self.assertEqual(fields[1]["payload"], 0x00010203)
        self.assertEqual(fields[8]["payload"], 0x1C1D1E1F)
        halo = (5 << 5) | (2 << 2) | 1
        self.assertTrue(all(match_south_halo(t, halo) for t in tiles))

    def test_encode_rejects(self):
        for index in (-1, MAX_INDEX + 1, 1.0):
            with self.assertRaises(ValueError):
                encode_frame(index, PASSWORD)
        for password in (PASSWORD[:31], PASSWORD + b"\0", "x" * 32):
            with self.assertRaises(ValueError):
                encode_frame(0, password)
        with self.assertRaises(ValueError):
            encode_frame(0, PASSWORD, form_id=3)
        with self.assertRaises(ValueError):
            encode_frame(0, PASSWORD, step_mux=1)

    def test_decode_rejects_defects(self):
        good = encode_frame(4, PASSWORD, **ROUTING)
        cases = {
            "short": good[:-1],
            "long": good + good[:1],
            "reordered": [good[0], good[2], good[1]] + good[3:],
            "spliced stream": good[:5] + encode_frame(4, PASSWORD, **(ROUTING | {"stream_slot": 8}))[5:],
            "wrong fragment form": good[:3] + [good[3] | (1 << 40)] + good[4:],
            "wrong index form": [encode_tile(4, form_id=0, **ROUTING)] + good[1:],
            "noncanonical residue": [encode_tile(1000 << 20, form_id=2, **ROUTING)] + good[1:],
            "reserved index bits": [good[0] | (1 << 30)] + good[1:],
            "not uint64": good[:8] + [2**64],
        }
        for name, tiles in cases.items():
            with self.subTest(name), self.assertRaises(ValueError):
                decode_frame(tiles)


class TestFrameVerifier(unittest.TestCase):
    def setUp(self):
        self.client = LamportClient(bytes(range(100, 132)), 4)
        self.server = LamportServer(self.client.anchor, 4)
        self.verifier = FrameVerifier(self.server, **ROUTING)

    def frame(self, index=None, **overrides):
        index = self.server.challenge() if index is None else index
        return encode_frame(index, self.client.password_for(index), **(ROUTING | overrides))

    def test_full_session_over_frames(self):
        for _ in range(4):
            self.assertTrue(self.verifier.verify_frame(self.frame()))
        self.assertFalse(self.verifier.verify_frame(encode_frame(0, PASSWORD, **ROUTING)))

    def test_replay_and_tamper(self):
        frame = self.frame()
        tampered = frame[:6] + [frame[6] ^ 1] + frame[7:]
        self.assertFalse(self.verifier.verify_frame(tampered))
        self.assertTrue(self.verifier.verify_frame(frame))
        self.assertFalse(self.verifier.verify_frame(frame))

    def test_index_is_a_prefilter_not_a_bypass(self):
        # Correct password, wrong index claim: rejected and nothing consumed.
        index = self.server.challenge()
        lying = encode_frame(index - 1, self.client.password_for(index), **ROUTING)
        self.assertFalse(self.verifier.verify_frame(lying))
        # Right index, wrong password: rejected.
        self.assertFalse(self.verifier.verify_frame(encode_frame(index, PASSWORD, **ROUTING)))
        self.assertEqual(self.server.remaining, 4)

    def test_profile_requires_32_byte_seed(self):
        # The last login presents h0, the seed itself, so a short seed cannot
        # be framed. Profile v0 therefore mandates 32-byte seeds.
        short = LamportClient(b"short seed", 2)
        encode_frame(1, short.password_for(1))
        with self.assertRaises(ValueError):
            encode_frame(0, short.password_for(0))

    def test_wrong_route_rejected(self):
        self.assertFalse(self.verifier.verify_frame(self.frame(gate_byte=0)))
        self.assertFalse(self.verifier.verify_frame(["garbage"]))
        self.assertEqual(self.server.remaining, 4)


if __name__ == "__main__":
    unittest.main()
