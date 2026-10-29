from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from dataclasses import FrozenInstanceError
import pytest

from geometric_clock import Channel, IntrinsicClock, ParityMap


def test_30node_parity_closure():
    clock = IntrinsicClock()
    assert clock.state.pulse_count == 0 and not clock.state.traversal_complete
    for pulse in range(1, 31):
        state, tile = clock.step_pulse()
        assert state.pulse_count == pulse
        assert state.node == pulse % 30 and state.spinor_step == pulse % 8
        assert state.accumulated_cycles == Fraction(9_192_631_770*pulse, 60)
        assert state.atomic_residual == Fraction(pulse % 2, 2)
        assert state.parity_residual == ParityMap.map_braid(state.channel.braid)
        assert tile.gate_byte == state.node and tile.core_word == pulse
    assert state.accumulated_cycles == 4_596_315_885
    assert state.elapsed_seconds == Fraction(1, 2)
    assert state.remainder == 0.0 and state.net_residual == 0.0
    assert state.traversal_complete and state.node == 0 and state.spinor_step == 6
    # Thirty nodes are not the shortest atomic fractional-closure period.
    assert IntrinsicClock().advance(2)[0].atomic_residual == 0


def test_arbitrary_precision_atomic_accumulation_and_deliberate_wire_rollover():
    pulses = (1 << 100) + 1
    state, tile = IntrinsicClock().advance(pulses)
    assert state.accumulated_cycles == Fraction(pulses*306_421_059, 2)
    assert state.atomic_residual == Fraction(1, 2)
    assert tile.core_word == 1
    assert state.pulse_count == pulses


def test_channel_product_group_and_six_node_traversal():
    assert len(Channel) == 6
    assert {Channel.for_pulse(p) for p in range(6)} == set(Channel)
    assert {c.channel_id for c in Channel} == set(range(6))
    for a in Channel:
        assert a.compose(Channel.FORWARD_0) == a
        for b in Channel:
            assert a.compose(b) == b.compose(a)
            assert a.compose(b).braid == a.braid*b.braid
            for c in Channel:
                assert a.compose(b).compose(c) == a.compose(b.compose(c))


@pytest.mark.parametrize('value', [-1, True, 0.5, '3'])
def test_invalid_pulse_counts_rejected(value):
    with pytest.raises(ValueError): ParityMap.get_parity_residual(value)
    with pytest.raises(ValueError): IntrinsicClock().advance(value)


@pytest.mark.parametrize('braid', [0, 2, True, 1.0])
def test_invalid_braid_rejected(braid):
    with pytest.raises(ValueError): ParityMap.map_braid(braid)


def test_snapshot_immutable_and_zero_advance_preserves_state():
    clock = IntrinsicClock()
    previous = clock.state
    assert clock.advance(0)[0] == previous
    with pytest.raises(FrozenInstanceError): previous.pulse_count = 10
    clock.step_pulse()
    assert previous.pulse_count == 0


def test_concurrent_steps_do_not_lose_ticks_or_mix_snapshot_tiles():
    clock = IntrinsicClock()
    with ThreadPoolExecutor(max_workers=4) as pool:
        outputs = list(pool.map(lambda _: clock.step_pulse(), range(120)))
    assert {state.pulse_count for state, _ in outputs} == set(range(1, 121))
    assert all(tile == state.to_tile() for state, tile in outputs)
    assert clock.pulse_count == 120
