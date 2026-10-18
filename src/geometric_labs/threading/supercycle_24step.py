"""24-step scheduler and integer Eisenstein-basis phase split; M3.

Represent z=a+omega*b+omega**2*c as (a-c,b-c) in basis (1,omega).
No complex floating-point arithmetic is needed.
"""
from math import lcm
SUPER_CYCLE = lcm(8,3)

def schedule(step: int) -> tuple[int,int,str | None]:
    if type(step) is not int or step<0:
        raise ValueError("nonnegative step required")
    k=step%8
    return k,step%3,('onload' if k==2 else 'offload' if k==6 else None)

def split_phases(a: int,b: int,c: int) -> tuple[int,tuple[int,int]]:
    if any(type(v) is not int for v in (a,b,c)):
        raise ValueError("integer channels required")
    return a+b+c,(a-c,b-c)

def join_phases(s: int,z: tuple[int,int]) -> tuple[int,int,int]:
    x,y=z
    if any(type(v) is not int for v in (s,x,y)) or (s-x-y)%3:
        raise ValueError("phase coefficients outside the integer image")
    c=(s-x-y)//3
    return x+c,y+c,c

def rotate_plane(z: tuple[int,int]) -> tuple[int,int]:
    x,y=z
    return -y,x-y
