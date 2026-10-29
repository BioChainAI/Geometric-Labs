"""Exact logical pulses under a declared common epoch, frame and 60 Hz anchoring.

No sleep, OS framerate, atomic measurement or automatic frame/clock alignment.
"""
from dataclasses import dataclass
from fractions import Fraction
from threading import RLock
from typing import ClassVar, Tuple

from ..core.holonomy import Exact, TorsionalMarkovPump, exact
from ..core.invariants import GeometricEngineInvariants, require_nonnegative_int
from ..core.parity import Channel, ParityMap
from ..core.spinor import SpinorClock
from .tile import EinsteinTile, SEMANTIC_PROFILE_ID, WIRE_FORMAT_ID


@dataclass(frozen=True)
class ClockState:
    pulse_count: int
    node: int
    spinor_step: int
    channel: Channel
    accumulated_cycles: Fraction
    elapsed_seconds: Fraction
    atomic_residual: Fraction
    epoch_id: str
    frame_id: str
    time_uncertainty: Fraction
    structure_selector: int
    stream_slot: int

    @property
    def remainder(self) -> float:
        return float(self.atomic_residual)

    @property
    def net_residual(self) -> float:
        return self.remainder

    @property
    def parity_residual(self) -> float:
        return ParityMap.get_parity_residual(self.pulse_count)

    @property
    def tier_index(self) -> int:
        return self.node//6

    @property
    def traversal_complete(self) -> bool:
        return self.pulse_count > 0 and self.node == 0

    def to_tile(self) -> EinsteinTile:
        """Local Form-0 counter: node in gate, low32 pulse bits in payload."""
        return EinsteinTile(cycle_step=self.spinor_step, wheel_unit=self.pulse_count % 8,
                            structure_selector=self.structure_selector, gate_byte=self.node,
                            form_id=0, core_word=self.pulse_count & 0xffffffff,
                            stream_slot=self.stream_slot)


class IntrinsicClock:
    semantic_profile_id: ClassVar[str] = SEMANTIC_PROFILE_ID
    wire_format_id: ClassVar[str] = WIRE_FORMAT_ID

    def __init__(self, *, pump: TorsionalMarkovPump | None = None,
                 epoch_id: str = 'simulated-shared-epoch', frame_id: str = 'simulated-shared-frame',
                 time_uncertainty: Exact = 0, structure_selector: int = 0, stream_slot: int = 0) -> None:
        if any(not isinstance(v, str) or not v.strip() for v in (epoch_id, frame_id)):
            raise ValueError('explicit nonempty epoch and frame IDs required')
        uncertainty = exact(time_uncertainty)
        if uncertainty < 0:
            raise ValueError('time uncertainty must be nonnegative')
        EinsteinTile(structure_selector=structure_selector, stream_slot=stream_slot)
        if pump is not None and not isinstance(pump, TorsionalMarkovPump):
            raise ValueError('pump must be a TorsionalMarkovPump')
        self._pump = pump if pump is not None else TorsionalMarkovPump()
        self._epoch_id, self._frame_id = epoch_id, frame_id
        self._time_uncertainty = uncertainty
        self._structure_selector, self._stream_slot = structure_selector, stream_slot
        self._pulse_count = 0
        self._spinor = SpinorClock()
        self._lock = RLock()

    @property
    def pump(self) -> TorsionalMarkovPump:
        """Immutable supplied orientation history; default is an identity fixture."""
        return self._pump

    @property
    def pulse_count(self) -> int:
        with self._lock:
            return self._pulse_count

    @property
    def state(self) -> ClockState:
        return self.read()[0]

    def _snapshot(self) -> ClockState:
        p = self._pulse_count
        cycles = p*GeometricEngineInvariants.cycles_per_pulse
        return ClockState(p, p % 30, self._spinor.k, Channel.for_pulse(p), cycles,
                          Fraction(p, 60), cycles % 1, self._epoch_id, self._frame_id,
                          self._time_uncertainty, self._structure_selector, self._stream_slot)

    def read(self) -> Tuple[ClockState, EinsteinTile]:
        with self._lock:
            state = self._snapshot()
            return state, state.to_tile()

    def step_pulse(self) -> Tuple[ClockState, EinsteinTile]:
        with self._lock:
            self._pulse_count += 1
            self._spinor.advance()
            return self.read()

    def advance(self, pulses: int) -> Tuple[ClockState, EinsteinTile]:
        """Exact bulk logical advance; no wall-clock delay or precision loss."""
        require_nonnegative_int(pulses, 'pulses')
        with self._lock:
            self._pulse_count += pulses
            self._spinor.advance(pulses)
            return self.read()
