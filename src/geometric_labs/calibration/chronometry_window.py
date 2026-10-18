"""Exact Cs-133 pulse windows; Lemma 11, Proposition 11.4."""
from math import gcd, lcm
from fractions import Fraction
NU_CS = 9_192_631_770
CS_FACTORIZATION = {2:1,3:2,5:1,7:2,47:1,44351:1}
W_SIGMA = 60
PARITY_RESIDUAL = Fraction(1,2)

def joint_closure(carriers: list[int], pulse_hz: int = W_SIGMA) -> tuple[int,Fraction]:
    if type(pulse_hz) is not int or pulse_hz<=0 or not carriers or any(type(f) is not int or f<=0 for f in carriers):
        raise ValueError("positive integer frequencies required")
    pulses=lcm(*(pulse_hz//gcd(pulse_hz,f) for f in carriers))
    return pulses,Fraction(pulses,pulse_hz)
