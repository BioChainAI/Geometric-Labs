"""[PROVEN] C3 × C2 group enumeration and half-cycle parity in Q/Z."""
from enum import Enum
from fractions import Fraction

from .invariants import require_nonnegative_int


class Channel(Enum):
    FORWARD_0 = (0, 1)
    INVERSE_0 = (0, -1)
    FORWARD_1 = (1, 1)
    INVERSE_1 = (1, -1)
    FORWARD_2 = (2, 1)
    INVERSE_2 = (2, -1)

    @property
    def phase_index(self) -> int:
        return int(self.value[0])

    @property
    def braid(self) -> int:
        return int(self.value[1])

    @property
    def phase_degrees(self) -> int:
        return (0, 120, -120)[self.phase_index]

    @property
    def channel_id(self) -> int:
        return 2*self.phase_index + int(self.braid == -1)

    @classmethod
    def from_components(cls, phase_index: int, braid: int) -> 'Channel':
        if type(phase_index) is not int or phase_index not in (0, 1, 2):
            raise ValueError('phase index must be 0, 1 or 2')
        ParityMap.map_braid(braid)
        return cls((phase_index, braid))

    @classmethod
    def for_pulse(cls, pulse_count: int) -> 'Channel':
        require_nonnegative_int(pulse_count, 'pulse_count')
        return cls.from_components(pulse_count % 3, -1 if pulse_count % 2 else 1)

    def compose(self, other: 'Channel') -> 'Channel':
        if not isinstance(other, Channel):
            raise TypeError('channel composition requires a Channel')
        return Channel.from_components((self.phase_index + other.phase_index) % 3, self.braid * other.braid)


class ParityMap:
    @staticmethod
    def map_braid(braid: int) -> float:
        if type(braid) is not int or braid not in (-1, 1):
            raise ValueError('braid must be +1 or -1')
        return 0.0 if braid == 1 else 0.5

    @staticmethod
    def residual_fraction(pulse_count: int) -> Fraction:
        require_nonnegative_int(pulse_count, 'pulse_count')
        return Fraction(pulse_count % 2, 2)

    @staticmethod
    def get_parity_residual(pulse_count: int) -> float:
        return float(ParityMap.residual_fraction(pulse_count))
