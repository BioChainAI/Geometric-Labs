"""Cuboctahedral engine ring and noncommutative erasure recovery; M1–M2."""
from fractions import Fraction
from ..hurwitz import H_ONE, H_TIER, HQuat, h_mul, h_inv_unit, h_conj
from ..blockchain.holonomy_prefix_scan import product
CUBOCTA_RING = tuple(tuple(0 if i==zero else signs[[j for j in range(3) if j!=zero].index(i)] for i in range(3)) for zero in (2,0,1) for signs in ((1,1),(1,-1),(-1,1),(-1,-1)))
ONLOAD_SCALE = Fraction(31,3)
OFFLOAD_SCALE = Fraction(3,31)

def close_group(data: list[HQuat]) -> list[HQuat]:
    if len(data)!=3:
        raise ValueError("three data engines required")
    for q in data:
        h_inv_unit(q)
    return list(data)+[h_inv_unit(product(data))]

def recover_single(group: list[HQuat | None]) -> HQuat:
    if len(group)!=4 or group.count(None)!=1:
        raise ValueError("exactly one erased engine required")
    i=group.index(None)
    cyclic=group[i+1:]+group[:i]
    recovered=h_inv_unit(product(cyclic))
    return recovered

def global_fourth(parities: list[HQuat]) -> HQuat:
    if len(parities)!=3:
        raise ValueError("three planar parities required")
    return h_inv_unit(product(parities))

def cascade_recover(groups: list[list[HQuat | None]], f_star: HQuat) -> list[list[HQuat]]:
    if len(groups)!=3 or any(len(g)!=4 for g in groups):
        raise ValueError("three four-engine groups required")
    result=[list(g) for g in groups]
    missing=[i for i,g in enumerate(result) if g[3] is None]
    if len(missing)>1:
        raise ValueError("at most one missing group parity supported")
    if missing:
        p=[g[3] for g in result]+[f_star]
        result[missing[0]][3]=recover_single(p)
    for g in result:
        if None in g:
            g[g.index(None)]=recover_single(g)
        if product(g)!=H_ONE:
            raise ValueError("inconsistent recovered group")
    if global_fourth([g[3] for g in result])!=f_star:
        raise ValueError("global parity mismatch")
    return result

def offload_recall(q: HQuat) -> HQuat:
    return h_mul(h_conj(H_TIER),h_mul(H_TIER,q))

def tier_word() -> HQuat:
    return product([h_conj(H_TIER),H_TIER,h_conj(H_TIER),H_TIER])
