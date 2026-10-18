"""Order-preserving Blelloch scan and right-acting three-gear holonomy.

O(n) work, O(log n) dependency depth; Python execution is sequential.
"""
from ..hurwitz import H_ONE, HQuat, h_mul, h_inv_unit
from .qcc_delta_chain import encode_chain

def prefix_scan(items: list[HQuat]) -> list[HQuat]:
    """Inclusive chronological products, padded power-of-two Blelloch tree."""
    if not items:
        return []
    n=1<<(len(items)-1).bit_length()
    a=list(items)+[H_ONE]*(n-len(items))
    stride=1
    while stride<n:
        for end in range(2*stride-1,n,2*stride):
            a[end]=h_mul(a[end-stride],a[end])
        stride*=2
    a[-1]=H_ONE
    stride=n//2
    while stride:
        for end in range(2*stride-1,n,2*stride):
            left=a[end-stride];prefix=a[end]
            a[end-stride]=prefix
            a[end]=h_mul(prefix,left)
        stride//=2
    return [h_mul(p,q) for p,q in zip(a,items)]

def product(items: list[HQuat]) -> HQuat:
    return prefix_scan(items)[-1] if items else H_ONE

def middle_gear_partition() -> list[list[int]]:
    return [[m for m in range(72) if 10*m//72==l] for l in range(10)]

def holonomy(states: list[HQuat]) -> dict[str,HQuat]:
    if len(states)!=720:
        raise ValueError("three-gear reference requires 720 states")
    deltas=encode_chain(states)
    outer=product(deltas[::-1])
    middle_deltas=[h_inv_unit(product(deltas[m:m+10][::-1])) for m in range(0,720,10)]
    middle=product(middle_deltas)
    inner=product([product([middle_deltas[m] for m in group]) for group in middle_gear_partition()])
    h=h_mul(inner,h_mul(middle,outer))
    expected=h_mul(states[0],h_inv_unit(states[-1]))
    if h_mul(middle,outer)!=H_ONE or h!=expected:
        raise ArithmeticError("holonomy does not telescope")
    return {'outer':outer,'middle':middle,'inner':inner,'holonomy':h,'expected':expected}
