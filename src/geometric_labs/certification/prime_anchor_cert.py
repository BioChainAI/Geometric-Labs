"""Packed Form-1 sieve and deterministic unsigned-64-bit Miller–Rabin.

The first 12 prime bases suffice below 2**64; inputs beyond that are rejected.
"""
from math import isqrt
from ..hurwitz import h_norm
MAX_FORM1_NORM = 16_129
MR12_BASES = (2,3,5,7,11,13,17,19,23,29,31,37)

def is_prime_64(n: int) -> bool:
    if type(n) is not int or not 0<=n<2**64:
        raise ValueError("unsigned 64-bit integer required")
    if n<2:
        return False
    for p in MR12_BASES:
        if n%p==0:
            return n==p
    d=n-1;s=0
    while d%2==0:
        d//=2;s+=1
    for a in MR12_BASES:
        x=pow(a,d,n)
        if x in (1,n-1):
            continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1:
                break
        else:
            return False
    return True

def build_prime_bitmap() -> bytes:
    sieve=bytearray([1])*(MAX_FORM1_NORM+1)
    sieve[:2]=b'\0\0'
    for p in range(2,isqrt(MAX_FORM1_NORM)+1):
        if sieve[p]:
            for k in range(p*p,MAX_FORM1_NORM+1,p):
                sieve[k]=0
    packed=bytearray(MAX_FORM1_NORM//8+1)
    for n,prime in enumerate(sieve):
        if prime:
            packed[n//8] |= 1 << (n%8)
    return bytes(packed)

PRIME_BITMAP = build_prime_bitmap()

def bitmap_is_prime(n: int) -> bool:
    if type(n) is not int or not 0<=n<=MAX_FORM1_NORM:
        raise ValueError("outside Form-1 bitmap")
    return bool(PRIME_BITMAP[n//8] & (1 << (n%8)))

def hurwitz_box_primes() -> list[int]:
    from itertools import product
    result=set()
    for parity in (0,1):
        values=range(-4+parity,5,2)
        for q in product(values,repeat=4):
            n=h_norm(q)
            if bitmap_is_prime(n):
                result.add(n)
    return sorted(result)
