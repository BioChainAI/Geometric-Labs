from math import sqrt
import pytest

from geometric_clock import SpinorClock


def test_exact_gaussian_cycle_and_preserved_double_cover_sign():
    expected = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
    clock = SpinorClock()
    for state in expected:
        assert clock.reduced_state == state
        assert all(value in (-1,0,1) for value in state)
        clock.advance()
    assert clock.k == 0 and clock.reduced_state == (1,0)
    assert SpinorClock.gaussian_power(4) == (-4,0)
    assert SpinorClock.gaussian_power(8) == (16,0)


@pytest.mark.parametrize('k,expected', [(0,0.0),(1,sqrt(.5)),(2,1.0),(3,sqrt(.5)),
                                      (4,0.0),(5,sqrt(.5)),(6,1.0),(7,sqrt(.5))])
def test_handshake_windows(k, expected):
    clock = SpinorClock(k)
    assert clock.is_onload_window() == (k == 2)
    assert clock.is_offload_window() == (k == 6)
    assert clock.get_transverse_amplitude() == expected


@pytest.mark.parametrize('k', [-1,8,True,2.0])
def test_invalid_spinor_step_and_assignment_rejected(k):
    with pytest.raises(ValueError): SpinorClock(k)
    with pytest.raises(ValueError): SpinorClock().k = k
