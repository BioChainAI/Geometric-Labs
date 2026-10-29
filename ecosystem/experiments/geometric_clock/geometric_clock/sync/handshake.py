"""Parity verification of two local logical clocks and supplied exact histories.

Wire words are actually serialized/deserialized at k=2/6. Full epoch/frame,
counter, uncertainty and history observations are supplied out of band by this
local harness: eight bytes alone cannot attest these values or authenticate peers.
"""
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Tuple

from ..core.holonomy import QuaternionDelta
from ..core.invariants import GeometricEngineInvariants, require_nonnegative_int
from ..core.parity import Channel, ParityMap
from ..core.spinor import SpinorClock
from ..engine.clock import ClockState, IntrinsicClock
from ..engine.tile import EinsteinTile, SEMANTIC_PROFILE_ID, WIRE_FORMAT_ID

Transport = Callable[[str, bytes], bytes]


class HandshakeError(ValueError):
    """Incompatible or inconsistent simulated peer observation; no resync occurs."""


@dataclass(frozen=True)
class HandshakeExchange:
    pulse_count: int
    spinor_step: int
    channel_id: int
    transverse_amplitude: float
    clock1_word: int
    clock2_word: int


@dataclass(frozen=True)
class HandshakeReport:
    success: bool
    start_pulse: int
    end_pulse: int
    exchanges: Tuple[HandshakeExchange, ...]
    phase_drift: Fraction
    holonomy1: QuaternionDelta
    holonomy2: QuaternionDelta
    epoch_id: str
    frame_id: str

    def __bool__(self) -> bool:
        return self.success


class ParityHandshakeTest:
    @staticmethod
    def verify_30node_closure() -> ClockState:
        clock = IntrinsicClock()
        state, _ = clock.advance(30)
        if (state.accumulated_cycles != 4_596_315_885 or state.atomic_residual != 0
                or state.elapsed_seconds != Fraction(1, 2) or state.node != 0):
            raise HandshakeError('30-node exact closure failed')
        return state

    @staticmethod
    def _compare(a: ClockState, b: ClockState) -> None:
        for state in (a, b):
            p = state.pulse_count
            if type(p) is not int or p < 0:
                raise HandshakeError('invalid absolute pulse counter')
            cycles = p*GeometricEngineInvariants.cycles_per_pulse
            if ((state.node, state.spinor_step, state.channel) != (p % 30, p % 8, Channel.for_pulse(p))
                    or state.accumulated_cycles != cycles or state.atomic_residual != cycles % 1
                    or state.elapsed_seconds != Fraction(p, 60)
                    or any(type(v) is not Fraction for v in (state.accumulated_cycles,
                           state.elapsed_seconds, state.atomic_residual, state.time_uncertainty))):
                raise HandshakeError('peer state violates exact pulse/phase invariants')
        if (a.epoch_id, a.frame_id) != (b.epoch_id, b.frame_id):
            raise HandshakeError('epoch/frame mismatch; explicit shared references required')
        if a.time_uncertainty != 0 or b.time_uncertainty != 0:
            raise HandshakeError('zero-phase assertion requires zero declared simulation uncertainty')
        if (a.pulse_count, a.elapsed_seconds, a.accumulated_cycles) != (b.pulse_count, b.elapsed_seconds, b.accumulated_cycles):
            raise HandshakeError('pulse/phase drift; clocks were not resynchronized')
        if (a.node, a.spinor_step, a.channel, a.atomic_residual) != (b.node, b.spinor_step, b.channel, b.atomic_residual):
            raise HandshakeError('C3 × C2 parity or phase mismatch')
        if a.parity_residual != ParityMap.map_braid(a.channel.braid):
            raise HandshakeError('braid parity differs from atomic residual')
        if (a.structure_selector, a.stream_slot) != (b.structure_selector, b.stream_slot):
            raise HandshakeError('structure/stream mismatch')

    @staticmethod
    def verify_cross_node_sync(clock1: IntrinsicClock, clock2: IntrinsicClock, *,
                               pulses: int = 30, transport: Transport | None = None) -> HandshakeReport:
        """Advance both clocks; check both windows, exact peer state and H=+1.

        Success describes this controlled simulation under common declared
        references. A failure leaves the already advanced pulses intact.
        """
        require_nonnegative_int(pulses, 'pulses')
        if pulses == 0:
            raise HandshakeError('positive pulse interval required')
        if (not isinstance(clock1, IntrinsicClock) or not isinstance(clock2, IntrinsicClock)
                or clock1 is clock2):
            raise HandshakeError('two independent IntrinsicClock instances required')
        for clock in (clock1, clock2):
            if clock.semantic_profile_id != SEMANTIC_PROFILE_ID or clock.wire_format_id != WIRE_FORMAT_ID:
                raise HandshakeError('clock wire/semantic profile mismatch')
            if not clock.pump.open_holonomy.is_identity():
                raise HandshakeError('supplied orientation history has nonidentity open holonomy')
        initial1, _ = clock1.read(); initial2, _ = clock2.read()
        ParityHandshakeTest._compare(initial1, initial2)
        transfer = transport if transport is not None else lambda direction, word: word
        exchanges = []
        for _ in range(pulses):
            a, tile1 = clock1.step_pulse(); b, tile2 = clock2.step_pulse()
            ParityHandshakeTest._compare(a, b)
            spinor = SpinorClock(a.spinor_step)
            if not (spinor.is_onload_window() or spinor.is_offload_window()):
                continue
            for direction, outgoing, peer in (('clock1-to-clock2', tile1, b), ('clock2-to-clock1', tile2, a)):
                try:
                    incoming = EinsteinTile.from_bytes(transfer(direction, outgoing.to_bytes()))
                except (ValueError, TypeError) as exc:
                    raise HandshakeError('invalid 64-bit peer envelope') from exc
                if incoming != peer.to_tile():
                    raise HandshakeError('peer envelope differs from expected pulse/profile; tamper or replay')
            exchanges.append(HandshakeExchange(a.pulse_count, a.spinor_step, a.channel.channel_id,
                                                spinor.get_transverse_amplitude(), tile1.pack(), tile2.pack()))
        if {e.spinor_step for e in exchanges} != {2, 6}:
            raise HandshakeError('interval must exercise both onload and offload windows')
        end1 = clock1.state; end2 = clock2.state
        ParityHandshakeTest._compare(end1, end2)
        if not clock1.pump.open_holonomy.is_identity() or not clock2.pump.open_holonomy.is_identity():
            raise HandshakeError('orientation history changed to nonidentity holonomy during exchange')
        return HandshakeReport(True, initial1.pulse_count, end1.pulse_count, tuple(exchanges),
                               end1.elapsed_seconds-end2.elapsed_seconds,
                               clock1.pump.open_holonomy, clock2.pump.open_holonomy,
                               end1.epoch_id, end1.frame_id)
