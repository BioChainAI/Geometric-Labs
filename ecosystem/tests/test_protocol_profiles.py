"""Offline profile gates; unsupported semantics never become implied decoders."""
import json
from pathlib import Path
import sys
import unittest

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'tools'))
from protocol_compatibility import receive
from preservation import preservation_errors


class ProtocolProfiles(unittest.TestCase):
    def decode(self,word,profile='glab-local-v1',**kwargs):
        return receive(word.to_bytes(8,'big'),wire_format_id='einstein-tile/1',
                       semantic_profile_id=profile,**kwargs)

    def test_supported_forms_and_explicit_opaque(self):
        for form in (0,*range(4,16)):
            self.assertTrue(self.decode(form<<40)['semantic_unresolved'])
            with self.assertRaises(ValueError):
                self.decode(form<<40,semantic_decode=True)
        self.assertEqual(self.decode((1<<40)|0x02000000,semantic_decode=True)['value'],(2,0,0,0))
        self.assertEqual(self.decode(2<<40,semantic_decode=True)['value'],0)
        self.assertEqual(self.decode((3<<40)|0x3fc00000,semantic_decode=True)['value'],1.5)

    def test_no_cross_profile_semantic_substitution(self):
        for profile in ('unknown','glab-local-v2'):
            with self.assertRaises(ValueError): self.decode(0,profile)
        with self.assertRaises(ValueError):
            self.decode(3<<40,'shdccp-proposed-v1',required_profile='glab-local-v1',semantic_decode=True)
        for form in (0,1,2,15):
            with self.assertRaises(ValueError): self.decode(form<<40,'shdccp-proposed-v1',semantic_decode=True)

    def test_reserved_form1_and_form2_fail_closed(self):
        for core in (0x80000000,0x01800101,0x01000000):
            with self.assertRaises(ValueError): self.decode((1<<40)|core,semantic_decode=True)
        with self.assertRaises(ValueError): self.decode((2<<40)|0xc0000000,semantic_decode=True)

    def test_wrong_wire_version_endian_and_legacy_not_reinterpreted(self):
        for wire in ('einstein-tile/2','ZONE/TYPE/SEQ/PAYLOAD'):
            with self.assertRaises(ValueError):
                receive(bytes(8),wire_format_id=wire,semantic_profile_id='glab-local-v1')
        with self.assertRaises(ValueError): self.decode(0,byte_order='little-endian')
        with self.assertRaises(ValueError):
            receive(bytes(7),wire_format_id='einstein-tile/1',semantic_profile_id='glab-local-v1')

    def test_original_reference_bytes_unchanged(self):
        snapshot = json.loads((BASE/'docs/status/preservation.v1.json').read_text())
        self.assertEqual(preservation_errors(BASE.parent, snapshot), [])


if __name__=='__main__':
    unittest.main()
