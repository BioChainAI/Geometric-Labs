"""64-bit Einstein Tile headers and reference payload profile.

See spec_sync/einstein_tile_64bit_rfc.md: forms 0 and 4–15 are opaque
because shape layouts were not supplied. No invented shape semantics.
"""
import struct
from .hurwitz import validate, canonical_associate
from .garner_crt import encode as crt_encode, decode as crt_decode
FIELDS = {'cycle_step':(61,3),'wheel_idx':(58,3),'struct_sel':(56,2),
          'gate_byte':(48,8),'step_mux':(44,4),'form_id':(40,4),
          'stream_slot':(36,4),'scale_reg':(32,4)}

def encode_tile(payload: int = 0, **headers: int) -> int:
    if type(payload) is not int or not 0<=payload<2**32:
        raise ValueError("payload must be uint32")
    unknown=set(headers)-set(FIELDS)
    if unknown:
        raise ValueError(f"unknown headers: {sorted(unknown)}")
    tile=payload
    for name,(shift,width) in FIELDS.items():
        value=headers.get(name,0)
        if type(value) is not int or not 0<=value<1<<width:
            raise ValueError(f"{name} out of range")
        tile |= value<<shift
    return tile

def decode_tile(tile: int) -> dict[str,int]:
    if type(tile) is not int or not 0<=tile<2**64:
        raise ValueError("tile must be uint64")
    return {name:(tile>>shift)&((1<<width)-1) for name,(shift,width) in FIELDS.items()} | {'payload':tile&0xffffffff}

def match_south_halo(tile_u64: int, expected_halo: int) -> bool:
    if type(tile_u64) is not int or not 0<=tile_u64<2**64 or type(expected_halo) is not int or not 0<=expected_halo<256:
        raise ValueError("uint64 tile and uint8 halo required")
    return tile_u64>>56==expected_halo

def encode_form1(q: tuple[int,int,int,int], **headers: int) -> int:
    """Seven-bit nonnegative dw, three signed bytes; reject truncation."""
    q=validate(q)
    if not 0<=q[0]<=127 or any(not -127<=c<=127 for c in q[1:]):
        raise ValueError("Form-1 coordinate outside reference range; normalize explicitly")
    core=(q[0]<<24)|((q[1]&255)<<16)|((q[2]&255)<<8)|(q[3]&255)
    return encode_tile(core,**(headers|{'form_id':1}))

def decode_form1(tile: int) -> tuple[int,int,int,int]:
    d=decode_tile(tile)
    if d['form_id']!=1 or d['payload']>>31:
        raise ValueError("not a reference Form-1 core")
    core=d['payload'];coords=[(core>>shift)&255 for shift in (24,16,8,0)]
    q=tuple(c-256 if c>=128 else c for c in coords)
    if any(c==-128 for c in q):
        raise ValueError("-128 is reserved in reference profile")
    return validate(q)

def encode_form2(value: int, **headers: int) -> int:
    x,y,z=crt_encode(value)
    return encode_tile((x<<20)|(y<<10)|z,**(headers|{'form_id':2}))

def decode_form2(tile: int) -> int:
    d=decode_tile(tile)
    if d['form_id']!=2 or d['payload']>>30:
        raise ValueError("not a Form-2 core")
    p=d['payload']
    return crt_decode(((p>>20)&1023,(p>>10)&1023,p&1023))

def encode_form3(value: float, **headers: int) -> int:
    payload=int.from_bytes(struct.pack('>f',value),'big')
    return encode_tile(payload,**(headers|{'form_id':3}))

def decode_form3(tile: int) -> float:
    d=decode_tile(tile)
    if d['form_id']!=3:
        raise ValueError("not a Form-3 core")
    return struct.unpack('>f',d['payload'].to_bytes(4,'big'))[0]
