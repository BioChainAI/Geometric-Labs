"""Bounded exact rational oracle, independent of torch and learned float states."""
from fractions import Fraction


def checked(values, max_bits=256):
    values = tuple(values)
    if not values or any(type(v) not in (int,Fraction) for v in values):
        raise ValueError('explicit rational inputs required, never floats')
    out = tuple(Fraction(v) for v in values)
    if any(max(abs(v.numerator).bit_length(),v.denominator.bit_length())>max_bits for v in out):
        raise OverflowError('rational reference bit budget exceeded')
    return out


def lorentz(q, max_bits=256):
    q = checked(q,max_bits)
    if len(q)!=4 or sum(v*v for v in q)!=1 or not Fraction(1,4)<=q[0]<=Fraction(9,10):
        raise ValueError('unit rational spinor in declared scalar annulus required')
    return checked((1/q[0],*(v/q[0] for v in q[1:])),max_bits)


def hyperbolic_quadrance(x,y,max_bits=256):
    x,y = checked(x,max_bits),checked(y,max_bits)
    if len(x)!=4 or len(y)!=4 or any(v[0]<=0 or v[0]**2-sum(a*a for a in v[1:])!=1 for v in (x,y)):
        raise ValueError('future unit hyperboloid vectors required')
    inner = checked((x[0]*y[0]-sum(a*b for a,b in zip(x[1:],y[1:])),),max_bits)[0]
    return checked((inner*inner-1,),max_bits)[0]


def sparsemax(values,max_bits=256):
    values=checked(values,max_bits)
    # Translate before sorting; exact and invariant to a constant shift.
    values=checked((v-max(values) for v in values),max_bits)
    ordered=sorted(values,reverse=True)
    prefix=Fraction(0);tau=None
    for k,value in enumerate(ordered,1):
        prefix=checked((prefix+value,),max_bits)[0]
        if 1+k*value>prefix:
            tau=checked(((prefix-1)/k,),max_bits)[0]
    result=checked((max(v-tau,Fraction(0)) for v in values),max_bits)
    if sum(result)!=1:
        raise ArithmeticError('simplex invariant failed')
    return result
