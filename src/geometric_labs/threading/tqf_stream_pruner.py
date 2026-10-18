"""Lossless integer second-difference pruning; blueprint Proposition 8.3."""

def prune(stream: list[int]) -> list[tuple[int,int]]:
    if any(type(x) is not int for x in stream):
        raise ValueError("integer samples required")
    return [(k,v) for k,v in enumerate(stream) if k in (0,len(stream)-1) or stream[k-1]-2*v+stream[k+1]!=0]

def interpolate(knots: list[tuple[int,int]], length: int) -> list[int]:
    if type(length) is not int or length<0:
        raise ValueError("nonnegative length required")
    if length==0:
        if knots:
            raise ValueError("empty stream cannot have knots")
        return []
    if not knots or knots[0][0]!=0 or knots[-1][0]!=length-1 or any(type(k) is not int or type(v) is not int for k,v in knots):
        raise ValueError("integer endpoints required")
    if any(a[0]>=b[0] for a,b in zip(knots,knots[1:])):
        raise ValueError("strictly increasing knot indices required")
    out=[knots[0][1]]*length
    for (k0,v0),(k1,v1) in zip(knots,knots[1:]):
        for k in range(k0,k1+1):
            numerator=(v1-v0)*(k-k0)
            q,r=divmod(numerator,k1-k0)
            if r:
                raise ValueError("interpolation is not an integer sample")
            out[k]=v0+q
    return out
