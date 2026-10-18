"""Executable conformance tests; see docs/architecture_blueprint.md."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import unittest
from geometric_labs.tile_codec import *
from geometric_labs.certification.merkle_12layer import *
from geometric_labs.hurwitz import HURWITZ_24_UNITS
import zlib
import random

class Verification(unittest.TestCase):
    def test_headers_and_all_forms(self):
        for form in range(16):
            tile=encode_tile(0xdeadbeef,cycle_step=7,wheel_idx=6,struct_sel=3,gate_byte=255,step_mux=9,form_id=form,stream_slot=15,scale_reg=2)
            d=decode_tile(tile)
            self.assertEqual(d['payload'],0xdeadbeef)
            self.assertEqual(d['form_id'],form)
            self.assertEqual(d['gate_byte'],255)
            self.assertEqual(d['stream_slot'],15)
            self.assertTrue(match_south_halo(tile,0xfb))
            self.assertFalse(match_south_halo(tile,0xfa))
        with self.assertRaises(ValueError): encode_tile(cycle_step=8)
        with self.assertRaises(ValueError): decode_tile(2**64)

    def test_typed_cores(self):
        for q in ((0,-126,126,0),(127,-127,127,-127),(2,0,0,0),(1,-1,1,1)):
            self.assertEqual(decode_form1(encode_form1(q)),q)
        for q in ((-2,0,0,0),(1,0,0,0),(128,0,0,0),(0,-128,0,0)):
            with self.assertRaises(ValueError): encode_form1(q)
        rng=random.Random(2)
        for value in [0,690017700]+[rng.randrange(690017701) for _ in range(300)]:
            self.assertEqual(decode_form2(encode_form2(value)),value)
        for value in (-0.,1.5,-2.25): self.assertEqual(decode_form3(encode_form3(value)),value)
        with self.assertRaises(ValueError): decode_form2(encode_tile(0xffffffff,form_id=2))
        with self.assertRaises(ValueError): decode_form1(encode_tile(0x80000000,form_id=1))

    def test_merkle_every_layer_and_crc_affinity(self):
        layers=[encode_form1(HURWITZ_24_UNITS[k] if HURWITZ_24_UNITS[k][0]>=0 else tuple(-c for c in HURWITZ_24_UNITS[k]),cycle_step=k%8) for k in range(12)]
        root=compute_merkle_12_root(layers)
        self.assertEqual(len(root),32)
        for i in range(12):
            tamper=list(layers);tamper[i]^=1
            self.assertNotEqual(root,compute_merkle_12_root(tamper))
        forged,predicted=crc32_forgery(b'abcdefgh',b'12345678',b'ABCDEFGH')
        self.assertEqual(zlib.crc32(forged),predicted)
        for message in (b'',b'changed payload',b'not the original block'):
            target=zlib.crc32(b'authentic block')
            collision=forge_crc32_suffix(message,target)
            self.assertTrue(collision.startswith(message))
            self.assertEqual(zlib.crc32(collision),target)
        with self.assertRaises(ValueError): compute_merkle_12_root(layers[:11])


if __name__ == "__main__":
    unittest.main()
