"""Four structures, twelve quaternion engines plus four component streams each.

A common frame per closed group is required for reverse emergent closure.
This is an exact router model; it does not launch concurrent OS threads.
"""
from ..hurwitz import H_ONE, H_TIER, HQuat, h_mul, h_norm, h_inv_unit
from ..blockchain.holonomy_prefix_scan import product

def stream_id(structure: int, slot: int) -> int:
    if type(structure) is not int or type(slot) is not int or not 0<=structure<4 or not 0<=slot<16:
        raise ValueError("invalid structure or slot")
    return (structure<<4)|slot

def build_balancer(inputs: list[HQuat], frame: HQuat = H_TIER) -> dict[str,list]:
    if len(inputs)!=12 or any(product(inputs[i:i+4])!=H_ONE for i in (0,4,8)):
        raise ValueError("three closed four-engine input groups required")
    h_inv_unit(frame)
    a=[frame]*12;abar=[h_inv_unit(frame)]*12
    emergent=[h_mul(frame,h_mul(h_inv_unit(q),h_inv_unit(frame))) for q in inputs]
    return {'I':list(inputs),'A':a,'A_bar':abar,'E':emergent}

def projection_streams(structures: dict[str,list[HQuat]]) -> dict[int,tuple]:
    streams={}
    for s,name in enumerate(('I','A','A_bar','E')):
        data=structures[name]
        if len(data)!=12:
            raise ValueError("twelve engines required")
        for j,q in enumerate(data):
            streams[stream_id(s,j)]=q
        for axis in range(4):
            streams[stream_id(s,12+axis)]=tuple(q[axis] for q in data)
    return streams

def verify_balancer(structures: dict[str,list[HQuat]]) -> dict[str,bool]:
    i,a,b,e=(structures[k] for k in ('I','A','A_bar','E'))
    if any(len(x)!=12 for x in (i,a,b,e)):
        raise ValueError("twelve engines in every structure required")
    return {
        'norm':all(h_norm(q)==1 for row in (i,a,b,e) for q in row),
        'slot_closure':all(product([a[j],i[j],b[j],e[j]])==H_ONE for j in range(12)),
        'equilibrium':all(p[0]==q[0] for p,q in zip(i,e)),
        'nested':product(a+b[::-1])==H_ONE,
        'reverse_closure':all(product(e[k:k+4][::-1])==H_ONE for k in (0,4,8))}
