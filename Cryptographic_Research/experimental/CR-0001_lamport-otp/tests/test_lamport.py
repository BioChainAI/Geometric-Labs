"""Classical baseline: chain links, login, replay, forgery, order, exhaustion, desync."""
from pathlib import Path
import sys
HERE = Path(__file__).resolve()
sys.path[:0] = [str(HERE.parents[1] / "src"), str(HERE.parents[4] / "src")]
import hashlib
import unittest
from geometric_lamport.lamport import LamportClient, LamportServer, build_chain, chain_value, new_seed


class TestChain(unittest.TestCase):
    def test_links_and_anchor(self):
        chain = build_chain(b"seed", 4)
        self.assertEqual(len(chain), 5)
        self.assertEqual(chain[0], b"seed")
        for i in range(4):
            self.assertEqual(chain[i + 1], hashlib.sha256(chain[i]).digest())
            self.assertEqual(chain_value(b"seed", i + 1), chain[i + 1])

    def test_rejects_bad_parameters(self):
        for length in (0, -1, 1.0, True):
            with self.assertRaises(ValueError):
                build_chain(b"seed", length)
        with self.assertRaises(TypeError):
            build_chain("seed", 3)
        with self.assertRaises(ValueError):
            chain_value(b"seed", -1)

    def test_pluggable_hash(self):
        blake = lambda v: hashlib.blake2s(v).digest()
        client = LamportClient(b"s", 3, blake)
        server = LamportServer(client.anchor, 3, blake)
        self.assertTrue(server.verify(client.password_for(server.challenge())))


class TestUpstreamEquivalence(unittest.TestCase):
    """Prefixes printed in the upstream README (commit e658632) for
    `python3 main.py --length 5 --seed demo`, oldest anchor first."""

    def test_readme_session(self):
        seed = hashlib.sha256(b"demo").digest()
        expected = ["b2e07a478cd7467f", "c9e347df8b725fe9", "e27454afd4571a60",
                    "5e2a90a840823b54", "175939018983abca", "2a97516c354b6884"]
        client = LamportClient(seed, 5)
        server = LamportServer(client.anchor, 5)
        self.assertEqual(client.anchor.hex()[:16], expected[0])
        for prefix in expected[1:]:
            password = client.password_for(server.challenge())
            self.assertEqual(password.hex()[:16], prefix)
            self.assertTrue(server.verify(password))


class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.length = 6
        self.client = LamportClient(new_seed(), self.length)
        self.server = LamportServer(self.client.anchor, self.length)

    def login(self):
        return self.server.verify(self.client.password_for(self.server.challenge()))

    def test_full_chain_then_exhaustion(self):
        for expected in range(self.length - 1, -1, -1):
            self.assertEqual(self.server.challenge(), expected)
            self.assertTrue(self.login())
        self.assertEqual(self.server.remaining, 0)
        with self.assertRaises(RuntimeError):
            self.server.challenge()
        self.assertFalse(self.server.verify(self.client.password_for(0)))

    def test_replay_rejected(self):
        password = self.client.password_for(self.server.challenge())
        self.assertTrue(self.server.verify(password))
        self.assertFalse(self.server.verify(password))

    def test_forgery_rejected_without_consuming(self):
        self.assertFalse(self.server.verify(b"wrong"))
        self.assertFalse(self.server.verify(bytes(32)))
        self.assertFalse(self.server.verify("not bytes"))
        self.assertEqual(self.server.remaining, self.length)

    def test_out_of_order_rejected(self):
        self.assertFalse(self.server.verify(self.client.password_for(self.length - 2)))
        self.assertFalse(self.server.verify(self.client.anchor))

    def test_lost_message_does_not_desynchronize(self):
        # Upstream's counter client skips a password if a login is lost in
        # transit and can never log in again. Challenges make this harmless.
        self.client.password_for(self.server.challenge())
        self.assertTrue(self.login())

    def test_challenge_outside_chain(self):
        for index in (-1, self.length):
            with self.assertRaises(ValueError):
                self.client.password_for(index)


if __name__ == "__main__":
    unittest.main()
