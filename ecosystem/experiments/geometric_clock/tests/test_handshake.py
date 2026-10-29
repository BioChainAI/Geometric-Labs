from fractions import Fraction
from dataclasses import replace
import json
import subprocess
import sys
import pytest

from geometric_clock import (HandshakeError, IntrinsicClock, ParityHandshakeTest,
                             QuaternionDelta as Q, TorsionalMarkovPump)


def test_30node_verifier():
    state = ParityHandshakeTest.verify_30node_closure()
    assert state.accumulated_cycles == 4_596_315_885 and state.remainder == 0.0


def test_two_independent_clocks_exchange_real_64bit_words_at_both_windows():
    transfers = []
    def transport(direction, word):
        transfers.append((direction, word))
        assert type(word) is bytes and len(word) == 8
        return bytes(bytearray(word))
    a, b = IntrinsicClock(), IntrinsicClock()
    report = ParityHandshakeTest.verify_cross_node_sync(a, b, transport=transport)
    assert report and report.phase_drift == 0
    assert report.holonomy1 == report.holonomy2 == Q.identity()
    assert report.end_pulse == a.pulse_count == b.pulse_count == 30
    assert [e.pulse_count for e in report.exchanges] == [2,6,10,14,18,22,26,30]
    assert all(e.transverse_amplitude == 1.0 for e in report.exchanges)
    assert len(transfers) == 16
    assert {d for d, _ in transfers} == {'clock1-to-clock2','clock2-to-clock1'}


def test_skew_and_tile_rollover_alias_do_not_establish_sync():
    for skew in (1,8,30,15*(1<<32)):
        a, b = IntrinsicClock(), IntrinsicClock()
        b.advance(skew)
        if skew == 15*(1<<32):
            assert a.read()[1] == b.read()[1]  # Identical words do not attest the epoch/counter.
        with pytest.raises(HandshakeError, match='drift'):
            ParityHandshakeTest.verify_cross_node_sync(a,b)
        assert b.pulse_count-a.pulse_count == skew


@pytest.mark.parametrize('changes', [{'epoch_id':'different'}, {'frame_id':'other-frame'},
                                    {'time_uncertainty':Fraction(1,1000)},
                                    {'structure_selector':1}, {'stream_slot':1}])
def test_incompatible_peer_references_or_routing_rejected(changes):
    with pytest.raises(HandshakeError):
        ParityHandshakeTest.verify_cross_node_sync(IntrinsicClock(), IntrinsicClock(**changes))


def test_open_or_spinor_inverted_histories_rejected():
    for endpoint in (Q(0,1,0,0), Q(-1,0,0,0)):
        frames = [Q.identity()]*720; frames[-1] = endpoint
        with pytest.raises(HandshakeError, match='holonomy'):
            ParityHandshakeTest.verify_cross_node_sync(IntrinsicClock(pump=TorsionalMarkovPump(frames)), IntrinsicClock())


def test_tampered_truncated_and_replayed_words_rejected():
    def tamper(direction, word):
        return (int.from_bytes(word,'big') ^ (1<<56)).to_bytes(8,'big')
    for transport in (tamper, lambda direction, word: word[:-1], lambda direction, word: 0):
        with pytest.raises(HandshakeError):
            ParityHandshakeTest.verify_cross_node_sync(IntrinsicClock(), IntrinsicClock(), transport=transport)
    cache = {}
    def replay(direction, word):
        return cache.setdefault(direction, word)
    with pytest.raises(HandshakeError, match='replay'):
        ParityHandshakeTest.verify_cross_node_sync(IntrinsicClock(), IntrinsicClock(), transport=replay)


def test_profile_mismatch_and_vacuous_single_clock_success_rejected():
    class OtherProfileClock(IntrinsicClock):
        semantic_profile_id = 'shdccp-proposed-v1'
    with pytest.raises(HandshakeError, match='profile'):
        ParityHandshakeTest.verify_cross_node_sync(IntrinsicClock(), OtherProfileClock())
    clock = IntrinsicClock()
    with pytest.raises(HandshakeError, match='independent'):
        ParityHandshakeTest.verify_cross_node_sync(clock, clock)
    with pytest.raises(HandshakeError, match='both'):
        ParityHandshakeTest.verify_cross_node_sync(IntrinsicClock(), IntrinsicClock(), pulses=2)


def test_concurrent_phase_change_during_last_exchange_is_not_a_pass():
    a, b = IntrinsicClock(), IntrinsicClock()
    def transfer(direction, word):
        if b.pulse_count == 30 and direction == 'clock2-to-clock1':
            a.step_pulse()
        return word
    with pytest.raises(HandshakeError, match='drift'):
        ParityHandshakeTest.verify_cross_node_sync(a,b,transport=transfer)


def test_matching_but_internally_wrong_peer_states_are_not_sync_evidence():
    class MisindexedClock(IntrinsicClock):
        def _snapshot(self):
            state = super()._snapshot()
            return replace(state, spinor_step=(state.spinor_step+1)%8)
    with pytest.raises(HandshakeError, match='invariants'):
        ParityHandshakeTest.verify_cross_node_sync(MisindexedClock(), MisindexedClock())


def test_cli_preserves_exact_fraction_output_and_local_handshake():
    result = subprocess.run([sys.executable,'-m','geometric_clock','--pulses','30'],
                            capture_output=True,text=True,check=True)
    state = json.loads(result.stdout)
    assert state['accumulated_cycles'] == {'numerator':'4596315885','denominator':'1'}
    result = subprocess.run([sys.executable,'-m','geometric_clock','--verify-sync'],
                            capture_output=True,text=True,check=True)
    assert json.loads(result.stdout)['exchanges'] == 8
    result = subprocess.run([sys.executable,'-m','geometric_clock','--pulses','-1'],capture_output=True,text=True)
    assert result.returncode == 2
