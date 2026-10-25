"""Reference-only GEOT geometry primitives; not an optimized neural network.

No claim of certified numerical exactness for torch floating-point paths. Mathematical
names distinguish triangle-TQF from triple-of-quad folded measurements. See RFC.
"""
from __future__ import annotations
import math
from fractions import Fraction
import torch


def fold_axis(x: torch.Tensor, axis: str) -> torch.Tensor:
    """Lossless permutation: halve one spatial axis and double channels."""
    if x.ndim != 4 or axis not in ('h', 'w'):
        raise ValueError('Expected BCHW tensor and axis h/w')
    b, c, h, w = x.shape
    if axis == 'h':
        if h % 2:
            raise ValueError('Height not divisible by 2')
        return x.reshape(b, c, h//2, 2, w).permute(0, 1, 3, 2, 4).reshape(b, c*2, h//2, w)
    if w % 2:
        raise ValueError('Width not divisible by 2')
    return x.reshape(b, c, h, w//2, 2).permute(0, 1, 4, 2, 3).reshape(b, c*2, h, w//2)


def unfold_axis(x: torch.Tensor, axis: str) -> torch.Tensor:
    """Inverse of fold_axis."""
    if x.ndim != 4 or x.shape[1] % 2 or axis not in ('h', 'w'):
        raise ValueError('Expected even-channel BCHW tensor, axis h/w')
    b, c, h, w = x.shape
    if axis == 'h':
        return x.reshape(b, c//2, 2, h, w).permute(0, 1, 3, 2, 4).reshape(b, c//2, 2*h, w)
    return x.reshape(b, c//2, 2, h, w).permute(0, 1, 3, 4, 2).reshape(b, c//2, h, 2*w)


def fold_three(x: torch.Tensor) -> torch.Tensor:
    """One binary fold on H, then W, then H: area/8 and channels*8."""
    for a in ('h', 'w', 'h'):
        x = fold_axis(x, a)
    return x


def unfold_three(x: torch.Tensor) -> torch.Tensor:
    for a in ('h', 'w', 'h'):
        x = unfold_axis(x, a)
    return x


def hamilton(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """Hamilton scalar-first q*r; last dimension has size 4."""
    if a.shape[-1] != 4 or b.shape[-1] != 4:
        raise ValueError('Scalar-first quaternions require four components')
    aw,av=a[...,0:1],a[...,1:]
    bw,bv=b[...,0:1],b[...,1:]
    return torch.cat((aw*bw-(av*bv).sum(dim=-1,keepdim=True),aw*bv+bw*av+torch.cross(av,bv,dim=-1)),dim=-1)


def ordered_block_product(qs: torch.Tensor) -> torch.Tensor:
    """Left-acting chronological increments: last increment multiplies on left."""
    if qs.ndim < 2 or qs.shape[-1] != 4 or qs.shape[-2] < 1:
        raise ValueError('Expected (..., time, 4)')
    result = torch.zeros_like(qs[..., 0, :]); result[..., 0] = 1
    for i in range(qs.shape[-2]):
        result = hamilton(qs[..., i, :], result)
    return result


def quaternion_conjugate(q: torch.Tensor) -> torch.Tensor:
    return torch.cat([q[..., :1], -q[..., 1:]], dim=-1)


def golden_clifford_torus(theta: torch.Tensor, psi: torch.Tensor) -> torch.Tensor:
    """2-angle torus embedded in S^3; not closed under arbitrary quaternion product."""
    phi=(1.0+math.sqrt(5.0))/2
    r1=phi/math.sqrt(1+phi*phi);r2=1/math.sqrt(1+phi*phi)
    return torch.stack([r1*torch.cos(theta),r1*torch.sin(theta),r2*torch.cos(psi),r2*torch.sin(psi)],dim=-1)


def lorentz_lift_from_spinor(q: torch.Tensor, eps: float=1e-5) -> torch.Tensor:
    """Phi(w,m)=(1/w,m/w), requiring positive-scalar unit spinors."""
    if not torch.isfinite(q).all() or q.shape[-1] != 4 or torch.any(q[...,0] <= eps):
        raise ValueError('Invalid positive-scalar spinor / annular condition')
    if not torch.allclose((q*q).sum(dim=-1), torch.ones_like(q[...,0]),rtol=1e-4,atol=1e-4):
        raise ValueError('Input is not a unit spinor')
    return torch.cat((1/q[..., :1],q[..., 1:]/q[..., :1]),dim=-1)


def hyperbolic_quadrance(x: torch.Tensor,y: torch.Tensor) -> torch.Tensor:
    """Sinh^2 geodesic distance, not a triangle-inequality metric."""
    if x.shape[-1]!=4 or y.shape[-1]!=4: raise ValueError('Expected Lorentz H3 vectors')
    for state in (x,y):
        norm=state[...,0].square()-state[...,1:].square().sum(-1)
        if not torch.isfinite(state).all() or torch.any(state[...,0]<1) or not torch.allclose(norm,torch.ones_like(norm),atol=1e-4,rtol=1e-4):
            raise ValueError('Finite future unit hyperboloid vectors required')
    inner=x[...,0]*y[...,0] - (x[...,1:]*y[...,1:]).sum(dim=-1)
    return (inner.square()-1).clamp_min(0)


def sparsemax(z: torch.Tensor, dim: int=-1) -> torch.Tensor:
    """Differentiable floating-point simplex projection, not rational-exact inference."""
    if not z.is_floating_point() or not torch.isfinite(z).all() or z.shape[dim]<1:
        raise ValueError('Finite nonempty floating candidate tensor required')
    z = z - z.amax(dim=dim, keepdim=True)
    zs, _=torch.sort(z,descending=True,dim=dim)
    cssv=zs.cumsum(dim=dim)-1
    shape=[1]*z.ndim; shape[dim]=z.shape[dim]
    ks=torch.arange(1,z.shape[dim]+1,device=z.device,dtype=z.dtype).reshape(shape)
    support=(zs*ks > cssv)
    k=support.sum(dim=dim,keepdim=True)
    tau=cssv.gather(dim=dim,index=(k-1).long())/k
    return torch.clamp(z-tau,min=0)


def triangle_tqf(p1,p2,p3):
    """16*A^2 computed exactly for 3 integer-coordinate points."""
    if any(len(p)!=3 or any(type(a)!=int for a in p) for p in (p1,p2,p3)):
        raise ValueError('Expected exact integer lattice points')
    q=lambda a,b:sum((x-y)**2 for x,y in zip(a,b))
    a=q(p1,p2);b=q(p2,p3);c=q(p1,p3)
    return 4*a*b-(a+b-c)**2


def rational_lorentz(q):
    """Exact Fraction counterpart for hardware-reference verification."""
    if len(q)!=4 or any(type(v) not in (int,Fraction) for v in q):
        raise ValueError('Exact integer/Fraction inputs required')
    q=tuple(Fraction(v) for v in q)
    if sum(v*v for v in q)!=1 or not 0<q[0]<1:
        raise ValueError('Rational unit spinor in positive scalar annulus required')
    return (1/q[0],) + tuple(v/q[0] for v in q[1:])
