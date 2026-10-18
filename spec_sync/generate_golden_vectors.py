#!/usr/bin/env python3
"""Deterministic, versioned local-profile vectors. --check never rewrites files."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import argparse
import json
import random
from geometric_labs.hurwitz import H_ONE,H_TIER,HURWITZ_24_UNITS,h_mul,h_norm,gram_tqf,canonical_associate
from geometric_labs.tile_codec import encode_tile,encode_form1,encode_form2,encode_form3,decode_tile
from geometric_labs.s5_hyperbolic_tree import step_s5_shift_add,abelian_shadow
from geometric_labs.garner_crt import encode,closed_form_inverses,MODULUS
from geometric_labs.blockchain.qcc_delta_chain import encode_chain
from geometric_labs.blockchain.holonomy_prefix_scan import holonomy
from geometric_labs.blockchain.toroidal_state_matrix import checkpoint
from geometric_labs.certification.merkle_12layer import compute_merkle_12_root
from geometric_labs.threading.cubocta_12engine_ring import close_group,global_fourth,CUBOCTA_RING
from geometric_labs.threading.balancer_64stream import build_balancer,projection_streams,verify_balancer
from geometric_labs.threading.supercycle_24step import split_phases
from geometric_labs.threading.torus_soliton_mux import covering_determinants,allocate_rectangles
from geometric_labs.threading.tqf_stream_pruner import prune

DIRECTORY=Path(__file__).resolve().parent/'golden_vectors'

def envelope(data: dict) -> dict:
    return {'schema_version':1,'profile':'geometric-labs-reference-v1',
            'integer_encoding':'JSON decimal integers; uint64 tiles are fixed 16-digit hex strings',
            'quaternion_coordinates':'doubled integers, except explicitly labeled S5 ordinary coordinates',
            'data':data}

def build_vectors() -> dict[str,dict]:
    headers={'cycle_step':2,'wheel_idx':3,'struct_sel':1,'gate_byte':36,
             'step_mux':6,'stream_slot':12,'scale_reg':0}
    tiles=[]
    for form in range(16):
        payload=0x12345678
        semantics='opaque; shape semantics unspecified'
        if form==1:
            tile=encode_form1(H_TIER,**headers);semantics='Hurwitz doubled coordinates'
        elif form==2:
            tile=encode_form2(123456789,**headers);semantics='three 10-bit CRT residues'
        elif form==3:
            tile=encode_form3(1.5,**headers);semantics='big-endian IEEE-754 binary32'
        else:
            tile=encode_tile(payload,form_id=form,**headers)
        tiles.append({'form':form,'semantics':semantics,'hex':f'{tile:016x}','decoded':decode_tile(tile)})
    word=['+i','+j','-i','+k','+j','+i','-k','+j']
    address=(1,0,0,0);path=[]
    for label in word:
        address=step_s5_shift_add(address,label);path.append(address)
    rng=random.Random(881883887)
    values=[0,1,880,881,882,MODULUS-1]+[rng.randrange(MODULUS) for _ in range(32)]
    chain=[HURWITZ_24_UNITS[(i*i+7*i+3)%24] for i in range(720)]
    chain[0]=H_ONE;chain[-1]=(0,2,0,0)
    layers=[encode_tile(k,cycle_step=k%8,form_id=k%16) for k in range(12)]
    inputs=sum([close_group(list(HURWITZ_24_UNITS[k:k+3])) for k in (3,9,17)],[])
    balancer=build_balancer(inputs)
    raw=[10,15,20,25,30,28,26,24,35,50]
    return {
      'v1_tiles_forms_0_15.json':envelope({'forms':tiles,'form1_example':list(H_TIER),'form2_value':123456789,'form3_value':1.5}),
      'v1_hurwitz_and_s5_tree.json':envelope({'units':HURWITZ_24_UNITS,'tier':H_TIER,
          'multiplication_table':[[h_mul(a,b) for b in HURWITZ_24_UNITS] for a in HURWITZ_24_UNITS],
          'canonical_associates':[canonical_associate(q) for q in HURWITZ_24_UNITS],
          'gram':{'u':[1000000,1,0,0],'v':[2000001,2,0,0],'quadrea':4},
          's5':{'coordinate_system':'ordinary integers','word':word,'path':path,'address':address,'shadow':abelian_shadow(word)}}),
      'v1_garner_crt_881_883_887.json':envelope({'primes':[881,883,887],'modulus':MODULUS,
          'inverses':closed_form_inverses(),'cases':[{'value':x,'residues':encode(x)} for x in values]}),
      'v1_quaternion_blockchain_merkle.json':envelope({'states':chain,'deltas':encode_chain(chain),
          'gears':holonomy(chain),'checkpoints':[{'m':m,'q':checkpoint(m),'norm':h_norm(checkpoint(m))} for m in range(1,9)],
          'layers_hex':[f'{x:016x}' for x in layers],'merkle_root_hex':compute_merkle_12_root(layers).hex()}),
      'v1_64stream_balancer_threading.json':envelope({'structures':balancer,
          'streams':{str(k):v for k,v in projection_streams(balancer).items()},'invariants':verify_balancer(balancer),
          'global_fourth':global_fourth([inputs[k] for k in (3,7,11)]),'ring':CUBOCTA_RING,
          'phases':{'inputs':[17,-8,31],'split':split_phases(17,-8,31)},
          'covering_determinants':covering_determinants(),
          'rectangles_rational':[[str(x) for x in row] for row in allocate_rectangles(12)],
          'pruning':{'raw':raw,'knots':prune(raw)}})}

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    vectors=build_vectors()
    DIRECTORY.mkdir(parents=True,exist_ok=True)
    mismatches=[]
    for name,data in vectors.items():
        serialized=json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n'
        path=DIRECTORY/name
        if args.check:
            if not path.exists() or path.read_bytes()!=serialized.encode('utf-8'):
                mismatches.append(name)
        else:
            path.write_bytes(serialized.encode('utf-8'))
    if mismatches:
        print('Vector mismatch: '+', '.join(mismatches),file=sys.stderr)
        return 1
    print(('Checked' if args.check else 'Generated')+f' {len(vectors)} vector files.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
