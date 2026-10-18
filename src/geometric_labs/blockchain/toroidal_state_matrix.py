"""Integer Fibonacci approximants; blueprint Theorem 5.3.

Two-sided updates preserve each phase-plane quadrance for i-axis units.
These primitives do not implement a ledger compression protocol.
"""
from ..hurwitz import HQuat, h_mul, h_inv_unit

def fibonacci(n: int) -> int:
    if type(n) is not int or n<0:
        raise ValueError("nonnegative index required")
    a,b=0,1
    for _ in range(n):
        a,b=b,a+b
    return a

def lucas(n: int) -> int:
    if type(n) is not int or n<0:
        raise ValueError("nonnegative index required")
    a,b=2,1
    for _ in range(n):
        a,b=b,a+b
    return a

def checkpoint(m: int) -> HQuat:
    if type(m) is not int or m<1:
        raise ValueError("positive checkpoint index required")
    return tuple(2*x for x in (fibonacci(m),fibonacci(m+1),fibonacci(m-1),fibonacci(m)))

def two_sided_update(q: HQuat, left: HQuat, right: HQuat) -> HQuat:
    for u in (left,right):
        h_inv_unit(u)
        if u[2:]!=(0,0):
            raise ValueError("torus-preserving phase requires i-axis units")
    return h_mul(h_mul(left,q),right)
