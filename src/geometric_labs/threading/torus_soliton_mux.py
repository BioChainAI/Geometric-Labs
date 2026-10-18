"""Exact torus covering determinants and rational disjoint phase rectangles.

Allocation occurs on the auxiliary torus; no unprovided physical PDE is assumed.
"""
from fractions import Fraction
J_G = (3,1,1,5)

def mat2_mul(a: tuple[int,...],b: tuple[int,...]) -> tuple[int,...]:
    return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])

def covering_determinants(count: int = 5) -> list[int]:
    if type(count) is not int or count<0:
        raise ValueError("nonnegative count required")
    curr=(1,0,0,1);result=[]
    for _ in range(count):
        curr=mat2_mul(curr,J_G)
        a,b,c,d=curr
        result.append(abs((a-1)*(d-1)-b*c))
    return result

def allocate_rectangles(count: int) -> list[tuple[Fraction,...]]:
    """Strictly separated rectangles inside [0,1)^2; exact rational bounds."""
    if type(count) is not int or count<0:
        raise ValueError("nonnegative count required")
    return [(Fraction(3*i+1,3*count),Fraction(3*i+2,3*count),Fraction(1,3),Fraction(2,3)) for i in range(count)]

def rectangles_disjoint(rectangles: list[tuple[Fraction,...]]) -> bool:
    if any(not (0<=x0<x1<=1 and 0<=y0<y1<=1) for x0,x1,y0,y1 in rectangles):
        raise ValueError("rectangles must be nonwrapping torus subsets")
    return all(a[1]<b[0] or b[1]<a[0] or a[3]<b[2] or b[3]<a[2] for i,a in enumerate(rectangles) for b in rectangles[i+1:])

def color_conflicts(adjacency: dict[int,set[int]]) -> dict[int,int]:
    if any(v not in adjacency or u not in adjacency[v] or u==v for u,neighbors in adjacency.items() for v in neighbors):
        raise ValueError("simple undirected conflict graph required")
    colors={}
    for node in sorted(adjacency):
        used={colors[n] for n in adjacency[node] if n in colors}
        colors[node]=next(c for c in range(len(used)+1) if c not in used)
    return colors
