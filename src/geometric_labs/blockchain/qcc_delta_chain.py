"""Exact unit-quaternion delta chains, open boundary q[-1] := q[0]."""
from ..hurwitz import H_ONE, HQuat, h_mul, h_inv_unit

def encode_chain(states: list[HQuat]) -> list[HQuat]:
    if not states:
        return []
    for q in states:
        h_inv_unit(q)
    return [H_ONE]+[h_mul(q,h_inv_unit(p)) for p,q in zip(states,states[1:])]

def decode_chain(initial: HQuat, deltas: list[HQuat]) -> list[HQuat]:
    h_inv_unit(initial)
    if not deltas:
        return []
    if deltas[0]!=H_ONE:
        raise ValueError("open boundary requires identity first delta")
    result=[];q=initial
    for d in deltas:
        h_inv_unit(d)
        q=h_mul(d,q)
        result.append(q)
    return result
