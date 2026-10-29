"""[PROVEN, exact unit inputs] Ordered open-boundary three-gear telescoping.

720 orientation frames mean 719 transitions plus an identity boundary delta.
No Markov transition matrix, stationary distribution or memory compression
guarantee is inferred from this rotation-history representation.
"""
from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence, Tuple, Union

Exact = Union[int, Fraction]


def exact(value: Exact) -> Fraction:
    if type(value) not in (int, Fraction):
        raise ValueError('explicit integer or Fraction required; floats are not exact inputs')
    return Fraction(value)


@dataclass(frozen=True)
class QuaternionDelta:
    w: Exact = 1
    x: Exact = 0
    y: Exact = 0
    z: Exact = 0

    def __post_init__(self) -> None:
        for name in ('w', 'x', 'y', 'z'):
            object.__setattr__(self, name, exact(getattr(self, name)))

    @classmethod
    def identity(cls) -> 'QuaternionDelta':
        return cls()

    def as_tuple(self) -> Tuple[Fraction, Fraction, Fraction, Fraction]:
        return Fraction(self.w), Fraction(self.x), Fraction(self.y), Fraction(self.z)

    @property
    def norm_squared(self) -> Fraction:
        return sum((v*v for v in self.as_tuple()), Fraction(0))

    def is_unit(self) -> bool:
        return self.norm_squared == 1

    def is_identity(self) -> bool:
        return self == QuaternionDelta.identity()

    def inverse(self) -> 'QuaternionDelta':
        norm = self.norm_squared
        if norm == 0:
            raise ValueError('zero quaternion is not invertible')
        return QuaternionDelta(self.w/norm, -self.x/norm, -self.y/norm, -self.z/norm)

    def __mul__(self, other: 'QuaternionDelta') -> 'QuaternionDelta':
        if not isinstance(other, QuaternionDelta):
            raise TypeError('Hamilton multiplication requires QuaternionDelta operands')
        a, b, c, d = self.as_tuple()
        e, f, g, h = other.as_tuple()
        return QuaternionDelta(a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g,
                               a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e)


def unit(value: QuaternionDelta) -> QuaternionDelta:
    if not isinstance(value, QuaternionDelta) or not value.is_unit():
        raise ValueError('unit QuaternionDelta required')
    return value


def product_right(items: Sequence[QuaternionDelta]) -> QuaternionDelta:
    """q0 q1 ... qN, preserving chronological RIGHT multiplication."""
    result = QuaternionDelta.identity()
    for item in items:
        result = result * unit(item)
    return result


def product_left(items: Sequence[QuaternionDelta]) -> QuaternionDelta:
    """qN ... q1 q0, preserving chronological LEFT updates."""
    result = QuaternionDelta.identity()
    for item in items:
        result = unit(item) * result
    return result


def prefixes_right(items: Sequence[QuaternionDelta]) -> Tuple[QuaternionDelta, ...]:
    result = QuaternionDelta.identity()
    frames = []
    for item in items:
        result = result * unit(item)
        frames.append(result)
    return tuple(frames)


@dataclass(frozen=True, init=False)
class TorsionalMarkovPump:
    fine_frames: Tuple[QuaternionDelta, ...]
    fine_deltas: Tuple[QuaternionDelta, ...]
    block_products: Tuple[QuaternionDelta, ...]
    middle_deltas: Tuple[QuaternionDelta, ...]
    inverse_frames: Tuple[QuaternionDelta, ...]
    coarse_groups: Tuple[Tuple[int, ...], ...]
    coarse_deltas: Tuple[QuaternionDelta, ...]
    coarse_frames: Tuple[QuaternionDelta, ...]

    def __init__(self, fine_frames: Sequence[QuaternionDelta] | None = None) -> None:
        frames = tuple(fine_frames) if fine_frames is not None else (QuaternionDelta.identity(),)*720
        if len(frames) != 720:
            raise ValueError('exactly 720 fine orientation frames required')
        for frame in frames:
            unit(frame)
        deltas = (QuaternionDelta.identity(),) + tuple(q*p.inverse() for p, q in zip(frames, frames[1:]))
        blocks = tuple(product_left(deltas[10*m:10*m+10]) for m in range(72))
        middle = tuple(block.inverse() for block in blocks)
        groups = tuple(tuple(m for m in range(72) if 10*m//72 == ell) for ell in range(10))
        coarse = tuple(product_right(tuple(middle[m] for m in group)) for group in groups)
        for name, value in (('fine_frames', frames), ('fine_deltas', deltas), ('block_products', blocks),
                            ('middle_deltas', middle), ('inverse_frames', prefixes_right(middle)),
                            ('coarse_groups', groups), ('coarse_deltas', coarse),
                            ('coarse_frames', prefixes_right(coarse))):
            object.__setattr__(self, name, value)
        if not (self.middle_product*self.outer_product).is_identity():
            raise ArithmeticError('inverse compensation failed')
        if self.holonomy != self.open_holonomy:
            raise ArithmeticError('ordered holonomy failed to telescope')

    @classmethod
    def from_deltas(cls, initial: QuaternionDelta, deltas: Sequence[QuaternionDelta]) -> 'TorsionalMarkovPump':
        """Decode 720 deltas with delta[0]=1, the declared open boundary."""
        unit(initial)
        deltas = tuple(deltas)
        if len(deltas) != 720 or deltas[0] != QuaternionDelta.identity():
            raise ValueError('720 deltas with identity delta[0] required')
        q = initial
        frames = []
        for delta in deltas:
            q = unit(delta)*q
            frames.append(q)
        return cls(frames)

    @property
    def outer_product(self) -> QuaternionDelta:
        return product_left(self.fine_deltas)

    @property
    def middle_product(self) -> QuaternionDelta:
        return self.inverse_frames[-1]

    @property
    def inner_product(self) -> QuaternionDelta:
        return self.coarse_frames[-1]

    @property
    def holonomy(self) -> QuaternionDelta:
        return self.inner_product*(self.middle_product*self.outer_product)

    @property
    def open_holonomy(self) -> QuaternionDelta:
        """[PROVEN] H=q0·q719⁻¹, retaining noncommutative order and spinor sign."""
        return self.fine_frames[0]*self.fine_frames[-1].inverse()

    @property
    def is_closed(self) -> bool:
        return self.open_holonomy.is_identity()
