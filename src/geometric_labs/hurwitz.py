"""Doubled-coordinate Hurwitz ring; blueprint Lemma 5, Parts 2 and 6a.

Python integers widen without overflow; a fixed-width port must check bounds.
Canonical associates use the lexicographically least LEFT unit associate.
"""
from typing import TypeAlias
HQuat: TypeAlias = tuple[int, int, int, int]
H_ONE: HQuat = (2, 0, 0, 0)
H_NEG_ONE: HQuat = (-2, 0, 0, 0)
H_TIER: HQuat = (1, -1, 1, 1)

def validate(q: HQuat) -> HQuat:
    if len(q) != 4 or any(type(c) is not int for c in q):
        raise ValueError("expected four integer doubled coordinates")
    if len({c % 2 for c in q}) != 1:
        raise ValueError("Hurwitz coordinates must share parity")
    return tuple(q)

def h_conj(q: HQuat) -> HQuat:
    w, x, y, z = validate(q)
    return w, -x, -y, -z

def h_norm(q: HQuat) -> int:
    return sum(c*c for c in validate(q)) // 4

def h_mul(p: HQuat, q: HQuat) -> HQuat:
    a,b,c,d = validate(p)
    e,f,g,h = validate(q)
    return ((a*e-b*f-c*g-d*h)//2, (a*f+b*e+c*h-d*g)//2,
            (a*g-b*h+c*e+d*f)//2, (a*h+b*g-c*f+d*e)//2)

def h_inv_unit(q: HQuat) -> HQuat:
    if h_norm(q) != 1:
        raise ValueError("inverse requires a norm-one Hurwitz unit")
    return h_conj(q)

def generate_24_hurwitz_units() -> list[HQuat]:
    units = [tuple(s if j == i else 0 for j in range(4)) for i in range(4) for s in (-2,2)]
    units += [tuple(1 if mask & (1 << i) else -1 for i in (3,2,1,0)) for mask in range(16)]
    return units

HURWITZ_24_UNITS = tuple(generate_24_hurwitz_units())

def canonical_associate(q: HQuat) -> HQuat:
    """Deterministic left-associate orbit representative (local convention)."""
    return min(h_mul(u,q) for u in HURWITZ_24_UNITS)

def gram_tqf(u: tuple[int, ...], v: tuple[int, ...]) -> int:
    """16 times squared triangle area, exact in any dimension."""
    if len(u) != len(v) or not u or any(type(x) is not int for x in (*u,*v)):
        raise ValueError("equal nonempty integer vectors required")
    return 4*(sum(x*x for x in u)*sum(y*y for y in v)-sum(x*y for x,y in zip(u,v))**2)

def projective_spinor_cycle() -> list[tuple[int, int]]:
    from math import gcd
    a,b=1,0
    states=[]
    for _ in range(8):
        a,b=a-b,a+b
        g=gcd(a,b)
        states.append((a//g,b//g))
    return states
