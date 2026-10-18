"""Sign-invariant coherence and Horn rotation fitting; blueprint §9.3–9.6.

Numerical Jacobi diagonalization is used only for physical frame calibration.
The final Hurwitz snap is an exact discrete check, not a general SO(4) solver.
"""
import math
from ..hurwitz import HURWITZ_24_UNITS, h_mul, h_conj

def symmetric_eigen(matrix: list[list[float]]) -> tuple[list[float],list[list[float]]]:
    n=len(matrix)
    a=[list(row) for row in matrix]
    v=[[float(i==j) for j in range(n)] for i in range(n)]
    for _ in range(100*n*n):
        p,q=max(((i,j) for i in range(n) for j in range(i+1,n)),key=lambda ij:abs(a[ij[0]][ij[1]]))
        if abs(a[p][q])<1e-14:
            return [a[i][i] for i in range(n)],v
        theta=.5*math.atan2(2*a[p][q],a[q][q]-a[p][p])
        c,s=math.cos(theta),math.sin(theta)
        app,aqq,apq=a[p][p],a[q][q],a[p][q]
        a[p][p]=c*c*app-2*s*c*apq+s*s*aqq
        a[q][q]=s*s*app+2*s*c*apq+c*c*aqq
        a[p][q]=a[q][p]=0.
        for k in range(n):
            if k not in (p,q):
                x,y=a[k][p],a[k][q]
                a[k][p]=a[p][k]=c*x-s*y
                a[k][q]=a[q][k]=s*x+c*y
            x,y=v[k][p],v[k][q]
            v[k][p],v[k][q]=c*x-s*y,s*x+c*y
    raise ArithmeticError("Jacobi eigensolver did not converge")

def phi_m_coherence(quaternions: list[tuple[float,...]]) -> float:
    if not quaternions or any(len(q)!=4 or sum(x*x for x in q)==0 for q in quaternions):
        raise ValueError("nonzero four-vectors required")
    matrix=[[sum(q[i]*q[j]/sum(x*x for x in q) for q in quaternions)/len(quaternions) for j in range(4)] for i in range(4)]
    values,_=symmetric_eigen(matrix)
    return max(values)

def quadrance_signature(points: list[tuple[int,...]], index: int) -> tuple:
    p=points[index]
    if not p or any(len(q)!=len(p) for q in points):
        raise ValueError("inconsistent dimension")
    return (sum(x*x for x in p),tuple(sorted(sum((a-b)**2 for a,b in zip(p,q)) for j,q in enumerate(points) if j!=index)))

def match_signatures(a: list[tuple[int,...]], b: list[tuple[int,...]]) -> list[int]:
    if len(a)!=len(b):
        raise ValueError("anchor counts differ")
    sigs={quadrance_signature(a,i):i for i in range(len(a))}
    if len(sigs)!=len(a):
        raise ValueError("ambiguous anchor signatures")
    try:
        match=[sigs[quadrance_signature(b,j)] for j in range(len(b))]
    except KeyError as e:
        raise ValueError("incongruent anchor clouds") from e
    if len(set(match))!=len(a):
        raise ValueError("anchor matching is not bijective")
    return match

def horn_rotation(a: list[tuple[float,float,float]], b: list[tuple[float,float,float]]) -> tuple[float,...]:
    """Least-squares 3D rotation quaternion taking a to b; translation centered."""
    if len(a)!=len(b) or len(a)<3:
        raise ValueError("at least three paired anchors required")
    ca=[sum(p[i] for p in a)/len(a) for i in range(3)]
    cb=[sum(p[i] for p in b)/len(b) for i in range(3)]
    m=[[sum((p[i]-ca[i])*(q[j]-cb[j]) for p,q in zip(a,b)) for j in range(3)] for i in range(3)]
    xx,xy,xz=m[0];yx,yy,yz=m[1];zx,zy,zz=m[2]
    k=[[xx+yy+zz,yz-zy,zx-xz,xy-yx],
       [yz-zy,xx-yy-zz,xy+yx,xz+zx],
       [zx-xz,xy+yx,-xx+yy-zz,yz+zy],
       [xy-yx,xz+zx,yz+zy,-xx-yy+zz]]
    values,v=symmetric_eigen(k)
    j=max(range(4),key=values.__getitem__)
    return tuple(v[i][j] for i in range(4))

def snap_hurwitz(rotation: tuple[float,...]) -> tuple[int,int,int,int]:
    if len(rotation)!=4 or not any(rotation):
        raise ValueError("nonzero quaternion required")
    return max(HURWITZ_24_UNITS,key=lambda u:abs(sum(a*b for a,b in zip(u,rotation))))

def rotate_anchor(point: tuple[int,int,int,int], unit: tuple[int,int,int,int]) -> tuple[int,...]:
    doubled=tuple(2*x for x in point)
    result=h_mul(h_mul(unit,doubled),h_conj(unit))
    if any(c%2 for c in result):
        raise ValueError("rotation does not preserve integer anchors")
    return tuple(c//2 for c in result)


def octahedral_rotations() -> tuple[tuple[tuple[int, ...], ...], ...]:
    """The 24 determinant-positive signed permutation matrices of the cube."""
    from itertools import permutations, product
    result = []
    for perm in permutations(range(3)):
        inversions = sum(perm[i] > perm[j] for i in range(3) for j in range(i+1, 3))
        for signs in product((-1, 1), repeat=3):
            if (-1)**inversions * signs[0]*signs[1]*signs[2] == 1:
                result.append(tuple(tuple(signs[i] if j == perm[i] else 0 for j in range(3)) for i in range(3)))
    return tuple(result)


OCTAHEDRAL_24 = octahedral_rotations()


def apply_rotation(matrix: tuple[tuple[int, ...], ...], point: tuple[int, ...]) -> tuple[int, ...]:
    """Exact action of an octahedral matrix on an ordinary integer 3-vector."""
    if matrix not in OCTAHEDRAL_24 or len(point) != 3 or any(type(x) is not int for x in point):
        raise ValueError("octahedral matrix and integer 3-vector required")
    return tuple(sum(a*b for a,b in zip(row, point)) for row in matrix)


def snap_octahedral(rotation: tuple[float, ...]) -> tuple[tuple[int, ...], ...]:
    """Snap a Horn quaternion to all 24 SO(3) cube rotations, including 90°."""
    if len(rotation) != 4 or not any(rotation):
        raise ValueError("nonzero rotation quaternion required")
    norm = math.sqrt(sum(x*x for x in rotation))
    w,x,y,z = (v/norm for v in rotation)
    matrix = ((1-2*(y*y+z*z),2*(x*y-w*z),2*(x*z+w*y)),
              (2*(x*y+w*z),1-2*(x*x+z*z),2*(y*z-w*x)),
              (2*(x*z-w*y),2*(y*z+w*x),1-2*(x*x+y*y)))
    return max(OCTAHEDRAL_24, key=lambda candidate: sum(a*b for row, other in zip(matrix,candidate) for a,b in zip(row,other)))


def align_octahedral(a: list[tuple[int, int, int]], b: list[tuple[int, int, int]]) -> tuple[list[int], tuple]:
    """Frame-free correspondence, Horn fit, O-group snap, exact certification.

    Anchors are origin-centered with distinct signatures; translated clouds
    require centering before this protocol. A bad snap is rejected exactly.
    """
    matching = match_signatures(a, b)
    paired = [a[i] for i in matching]
    matrix = snap_octahedral(horn_rotation(paired,b))
    if [apply_rotation(matrix,p) for p in paired] != b:
        raise ValueError("anchors do not certify an exact octahedral alignment")
    return matching,matrix
