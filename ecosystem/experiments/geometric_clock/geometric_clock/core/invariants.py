"""[PROVEN within the model] Finite tier laws and their arithmetic sums.

The 60 Hz value is an explicit SI anchoring convention, not a frequency
measurement derived from dimensionless geometry.
"""
from dataclasses import dataclass, field
from fractions import Fraction
from typing import ClassVar, Tuple


def require_nonnegative_int(value: int, name: str) -> int:
    """Reject bools and approximate numeric inputs at exact integer boundaries."""
    if type(value) is not int or value < 0:
        raise ValueError(f'{name} must be a nonnegative integer')
    return value


@dataclass(frozen=True)
class StatorTier:
    n: int
    W_n: int = field(init=False)
    R_n: int = field(init=False)
    r_n: int = field(init=False)

    def __post_init__(self) -> None:
        require_nonnegative_int(self.n, 'tier index')
        if self.n > 4:
            raise ValueError('tier index must be in 0..4')
        object.__setattr__(self, 'W_n', 16 - 2*self.n)
        object.__setattr__(self, 'R_n', 5*self.n**2 + 15*self.n + 15)
        object.__setattr__(self, 'r_n', 2*self.n + 4)


@dataclass(frozen=True)
class GeometricEngineInvariants:
    f_geo: ClassVar[float] = 60.0
    tau_Q: ClassVar[float] = 1.0 / 60.0
    nu_Cs: ClassVar[int] = 9_192_631_770
    pulse_hz: ClassVar[int] = 60
    tau_Q_exact: ClassVar[Fraction] = Fraction(1, 60)
    cycles_per_pulse: ClassVar[Fraction] = Fraction(9_192_631_770, 60)
    tiers: Tuple[StatorTier, ...] = field(default_factory=lambda: tuple(StatorTier(n) for n in range(5)), init=False)

    @property
    def winding_sum(self) -> int:
        return sum(t.W_n for t in self.tiers)

    @property
    def major_radii(self) -> Tuple[int, ...]:
        return tuple(t.R_n for t in self.tiers)

    @property
    def minor_radii(self) -> Tuple[int, ...]:
        return tuple(t.r_n for t in self.tiers)

    def verify_winding_invariant(self) -> bool:
        """[PROVEN] Σ(16−2n), n=0..4, equals 5·16−2·10 = 60."""
        return self.winding_sum == 60
