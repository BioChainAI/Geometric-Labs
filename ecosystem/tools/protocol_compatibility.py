#!/usr/bin/env python3
"""Structural C/Python compatibility gate; semantic differences remain explicit."""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import glab
from upstreams import load

ALIASES = {'core': 'payload', 'scale': 'scale_reg', 'step_index': 'step_mux',
           'gate': 'gate_byte', 'structure': 'struct_sel', 'wheel_unit': 'wheel_idx',
           'stream_slot': 'stream_slot', 'form_id': 'form_id', 'cycle_step': 'cycle_step'}
PROFILES = glab.BASE / 'contracts/protocol_profiles.v1.json'


def contracts():
    return json.loads(PROFILES.read_text())


def receive(raw, *, wire_format_id, semantic_profile_id, byte_order='big-endian',
            required_profile=None, semantic_decode=False):
    """Validate integration metadata before decoding. No upstream codec is redefined."""
    contract = contracts()
    if wire_format_id != contract['wire_format_id'] or byte_order != 'big-endian':
        raise ValueError('wire format/version/byte order mismatch')
    if semantic_profile_id not in contract['profiles']:
        raise ValueError('unknown semantic profile')
    if required_profile and required_profile != semantic_profile_id:
        raise ValueError('semantic profile mismatch')
    if not isinstance(raw, bytes) or len(raw) != 8:
        raise ValueError('exactly eight wire bytes required')
    form = (int.from_bytes(raw, 'big') >> 40) & 15
    if not semantic_decode:
        return {'form_id': form, 'opaque': True, 'semantic_unresolved': True}
    if form not in contract['profiles'][semantic_profile_id]['semantic_decoders']:
        raise ValueError('form semantics unavailable; only opaque forwarding allowed')
    if semantic_profile_id == 'glab-local-v1':
        sys.path.insert(0, str(glab.BASE.parent / 'src'))
        from geometric_labs.tile_codec import decode_form1, decode_form2, decode_form3
        value = {1: decode_form1, 2: decode_form2, 3: decode_form3}[form](int.from_bytes(raw, 'big'))
    else:
        import struct
        value = struct.unpack('>f', raw[4:])[0]
    return {'form_id': form, 'opaque': False, 'value': value}


class Halves(ctypes.Structure):
    _fields_ = [('hi', ctypes.c_uint32), ('lo', ctypes.c_uint32)]


class Fields(ctypes.Structure):
    _fields_ = [('core', ctypes.c_uint32)] + [(name, ctypes.c_uint8) for name in
                ('scale', 'stream_slot', 'form_id', 'step_index', 'gate', 'structure', 'wheel_unit', 'cycle_step')]


class CCodec:
    def __init__(self, core, temporary):
        compiler = shutil.which('cc')
        if not compiler:
            raise RuntimeError('C11 compiler missing; compatibility gate blocked')
        self.version = subprocess.check_output([compiler, '--version'], text=True).splitlines()[0]
        shared = Path(temporary) / 'libshdccp.so'
        flags = [compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', '-I', str(core/'c/include')]
        subprocess.run(flags + ['-shared', '-fPIC', str(core/'c/src/shdccp.c'), '-o', str(shared)], check=True, capture_output=True)
        binary = Path(temporary) / 'test_codec'
        subprocess.run(flags + [str(core/'c/src/shdccp.c'), str(core/'c/test_codec.c'), '-o', str(binary)], check=True, capture_output=True)
        self.upstream_result = subprocess.check_output([str(binary)], text=True).strip()
        self.lib = ctypes.CDLL(str(shared))
        self.lib.shdccp_pack.argtypes = [Fields, ctypes.POINTER(Halves)]
        self.lib.shdccp_pack.restype = ctypes.c_int
        self.lib.shdccp_unpack.argtypes = [Halves, ctypes.POINTER(Fields)]
        self.lib.shdccp_unpack.restype = None
        self.lib.shdccp_to_be_bytes.argtypes = [Halves, ctypes.POINTER(ctypes.c_uint8)]
        self.lib.shdccp_to_be_bytes.restype = None
        self.lib.shdccp_from_be_bytes.argtypes = [ctypes.POINTER(ctypes.c_uint8)]
        self.lib.shdccp_from_be_bytes.restype = Halves

    def roundtrip(self, fields):
        # C uint8/uint32 narrowing cannot represent larger values: guard the FFI.
        widths = {'core': 32, 'gate': 8, 'scale': 4, 'stream_slot': 4, 'form_id': 4,
                  'step_index': 4, 'structure': 2, 'wheel_unit': 3, 'cycle_step': 3}
        if set(fields) != set(widths) or any(type(v) is not int or not 0 <= v < 1 << widths[k] for k,v in fields.items()):
            raise ValueError('C input bounds violated before narrowing')
        output = Halves()
        if self.lib.shdccp_pack(Fields(**fields), ctypes.byref(output)) != 0:
            raise ValueError('C codec rejected packet')
        wire = (ctypes.c_uint8 * 8)()
        self.lib.shdccp_to_be_bytes(output, wire)
        restored = self.lib.shdccp_from_be_bytes(wire)
        decoded = Fields()
        self.lib.shdccp_unpack(restored, ctypes.byref(decoded))
        if {name: getattr(decoded,name) for name in widths} != fields:
            raise AssertionError('C unpack mismatch')
        return bytes(wire)


def run_gate():
    origins = load(['SHD-CCP-core'])
    from shdccp_core.tile import FIELDS, pack, unpack
    sys.path.insert(0, str(glab.BASE.parent/'src'))
    from geometric_labs.tile_codec import FIELDS as LOCAL_FIELDS, encode_tile, decode_tile
    core = glab.BASE/'workspaces/SHD-CCP-core'
    spec_path = core/'spec/shdccp_einstein_v1.json'
    spec = json.loads(spec_path.read_text())
    spec_fields = {f['name']: (f['lsb'], f['width']) for f in spec['fixed_fields']}
    python_fields = {name: (lsb,width) for name,lsb,width in FIELDS}
    local_fields = {'core': (0,32)} | {upstream: LOCAL_FIELDS[local] for upstream,local in ALIASES.items() if upstream != 'core'}
    if spec['wire_word_bytes'] != 8 or spec['wire_byte_order'] != 'big-endian' or spec['spec_id'] != 'SHDCCP-EINSTEIN-1':
        raise AssertionError('upstream envelope spec mismatch')
    if not spec_fields == python_fields == local_fields:
        raise AssertionError('fixed field positions differ')
    vectors_path = core/'spec/golden_vectors.json'
    vectors = json.loads(vectors_path.read_text())
    if vectors['spec'] != spec['spec_id']:
        raise AssertionError('upstream vector spec mismatch')
    cases = [(item['fields'],bytes.fromhex(item['wire_hex'])) for item in vectors['cases']]
    local_path = glab.BASE.parent/'spec_sync/golden_vectors/v1_tiles_forms_0_15.json'
    local_vectors = json.loads(local_path.read_text())
    if local_vectors['profile'] != contracts()['profiles']['glab-local-v1']['fixture_profile_alias']:
        raise AssertionError('local fixture profile changed')
    for item in local_vectors['data']['forms']:
        raw = bytes.fromhex(item['hex'])
        fields = {name: item['decoded'][local] for name,local in ALIASES.items()}
        cases.append((fields,raw))
    # Every individual bit exercises boundary positions, independent of both codecs.
    for bit in range(64):
        word = 1 << bit
        cases.append(({name:(word >> pos)&((1 << width)-1) for name,pos,width in FIELDS},word.to_bytes(8,'big')))
    rng = random.Random(6401)
    for _ in range(100):
        word = rng.getrandbits(64)
        cases.append(({name:(word >> pos)&((1 << width)-1) for name,pos,width in FIELDS},word.to_bytes(8,'big')))
    with tempfile.TemporaryDirectory(prefix='glab-c11-') as temporary:
        c = CCodec(core,temporary)
        for fields,expected in cases:
            local = {ALIASES[name]:value for name,value in fields.items()}
            if pack(**fields) != expected or c.roundtrip(fields) != expected or encode_tile(**local).to_bytes(8,'big') != expected:
                raise AssertionError('C/Python/local byte disagreement')
            if unpack(expected) != fields or decode_tile(int.from_bytes(expected,'big')) != local:
                raise AssertionError('Python decode disagreement')
        invalid = Fields(form_id=16)
        if c.lib.shdccp_pack(invalid,ctypes.byref(Halves())) == 0:
            raise AssertionError('C failed to reject out-of-range form')
        compiler, upstream_result = c.version,c.upstream_result
    gaps = [
        {'forms':[0], 'issue':'local opaque vs upstream named lossy quaternion'},
        {'forms':[1], 'issue':'upstream raw codec does not certify parity/sign/reserved flags'},
        {'forms':[2], 'issue':'local 10/10/10 packing not standardized upstream'},
        {'forms':list(range(4,16)), 'issue':'named Codex forms have no complete upstream semantic codec'}]
    return {'schema':'biochain.protocol-compatibility-report.v1','status':'PASS',
            'wire_format_id':'einstein-tile/1','semantic_profiles':['glab-local-v1','shdccp-proposed-v1'],
            'semantic_compatible':False,'semantic_gaps':gaps,'packet_cases':len(cases),
            'form_id_bits':[40,43],'byte_order':'big-endian','c_api':'two-u32 on native host (not an actual 32-bit host run)',
            'compiler':compiler,'upstream_c_test':upstream_result,'import_origins':origins,
            'fixture_sha256':{str(p.relative_to(glab.BASE.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (spec_path,vectors_path,local_path)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    try:
        report = run_gate()
    except (ValueError, RuntimeError, AssertionError, OSError, subprocess.CalledProcessError) as error:
        print('PROTOCOL GATE FAILED:', error, file=sys.stderr)
        return 1
    serialized = json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(serialized)
    print(serialized,end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
