"""[PROVEN] Exact projective Gaussian powers; floating envelope is display-only."""
from dataclasses import dataclass
from math import gcd, sqrt
from typing import Tuple

from .invariants import require_nonnegative_int


@dataclass
class SpinorClock:
    k: int = 0

    def __setattr__(self, name: str, value: object) -> None:
        if name == 'k' and (type(value) is not int or not 0 <= value <= 7):
            raise ValueError('spinor step must be an integer in 0..7')
        object.__setattr__(self, name, value)

    @staticmethod
    def gaussian_power(exponent: int) -> Tuple[int, int]:
        """Exact (1+i)^exponent using exponentiation by squaring."""
        require_nonnegative_int(exponent, 'exponent')
        result, base = (1, 0), (1, 1)
        while exponent:
            if exponent & 1:
                a, b = result; c, d = base
                result = (a*c-b*d, a*d+b*c)
            a, b = base
            base = (a*a-b*b, 2*a*b)
            exponent >>= 1
        return result

    @property
    def reduced_state(self) -> Tuple[int, int]:
        a, b = self.gaussian_power(self.k)
        divisor = gcd(a, b)
        return a//divisor, b//divisor

    def advance(self, steps: int = 1) -> Tuple[int, int]:
        require_nonnegative_int(steps, 'steps')
        self.k = (self.k + steps) % 8
        return self.reduced_state

    def is_onload_window(self) -> bool:
        return self.k == 2

    def is_offload_window(self) -> bool:
        return self.k == 6

    def get_transverse_amplitude(self) -> float:
        """|sin(kπ/4)|, with exact 0.0/1.0 at axial/window steps."""
        return (0.0, sqrt(0.5), 1.0, sqrt(0.5), 0.0, sqrt(0.5), 1.0, sqrt(0.5))[self.k]
