"""Z/30Z proposal filter, not a primality certificate; Lemma 4 Part 5."""
from fractions import Fraction
from math import gcd
WHEEL_UNITS = tuple(n for n in range(30) if gcd(n,30)==1)
B_PLUS = tuple(n for n in WHEEL_UNITS if n%5 in (1,4))
B_MINUS = tuple(n for n in WHEEL_UNITS if n%5 in (2,3))
ORACLE_BIAS = Fraction(30,len(WHEEL_UNITS))

def wheel_candidate(n: int) -> bool:
    return n%30 in WHEEL_UNITS

def verify_bias() -> bool:
    return ORACLE_BIAS==Fraction(15,4) and set(B_PLUS)|set(B_MINUS)==set(WHEEL_UNITS)
