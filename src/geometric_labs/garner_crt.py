"""Prime-triplet CRT; blueprint Lemma 9. All operations use exact integers."""
from math import gcd
DEFAULT_PRIMES = (881,883,887)
MODULUS = 690_017_701

def closed_form_inverses(p: int = 881) -> tuple[int,int,int]:
    """Residue-selected polynomial inverses for pairwise-coprime (p,p+2,p+6).

    Default p=881 uses ((p+1)/2,(3p+17)/4,(5p+29)/6).
    Primality is not necessary for CRT; pairwise coprimality is.
    """
    if type(p) is not int or p<=1 or any(gcd(a,b)!=1 for a,b in ((p,p+2),(p,p+6),(p+2,p+6))):
        raise ValueError("triplet must be positive and pairwise coprime")
    def inv_gap(a: int, gap: int) -> int:
        modulus=a+gap
        k=next(k for k in range(1,gap) if (k*modulus-1)%gap==0)
        return (k*modulus-1)//gap
    return inv_gap(p,2),inv_gap(p+2,4),inv_gap(p,6)

def encode(value: int, p: int = 881) -> tuple[int,int,int]:
    closed_form_inverses(p)
    if type(value) is not int or not 0<=value<p*(p+2)*(p+6):
        raise ValueError("CRT value out of range")
    return value%p,value%(p+2),value%(p+6)

def decode(residues: tuple[int,int,int], p: int = 881) -> int:
    c12,c23,c13=closed_form_inverses(p)
    if len(residues)!=3 or any(type(x) is not int or not 0<=x<m for x,m in zip(residues,(p,p+2,p+6))):
        raise ValueError("noncanonical residues")
    x,y,z=residues
    u2=((y-x)*c12)%(p+2)
    u3=((((z-x)*c13)%(p+6)-u2)*c23)%(p+6)
    return x+p*u2+p*(p+2)*u3
