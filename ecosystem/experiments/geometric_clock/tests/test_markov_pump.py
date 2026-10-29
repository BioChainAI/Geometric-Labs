from fractions import Fraction
import random
import pytest

from geometric_clock import QuaternionDelta as Q, TorsionalMarkovPump

I = Q.identity()
X, Y, Z = Q(0,1,0,0), Q(0,0,1,0), Q(0,0,0,1)
R = Q(Fraction(1,2), Fraction(1,2), Fraction(1,2), Fraction(1,2))


def history(closed=True):
    rng = random.Random(381)
    frames = [rng.choice([I,X,Y,Z,R,R.inverse()]) for _ in range(720)]
    frames[0] = R
    frames[-1] = R if closed else Y
    return frames


def test_markov_pump_telescoping():
    frames = history()
    pump = TorsionalMarkovPump(frames)
    assert len(pump.fine_frames) == len(pump.fine_deltas) == 720
    assert len(pump.inverse_frames) == len(pump.middle_deltas) == 72
    assert len(pump.coarse_frames) == len(pump.coarse_deltas) == 10
    for m, block in enumerate(pump.block_products):
        assert block == frames[10*m+9]*frames[max(0,10*m-1)].inverse()
        assert pump.middle_deltas[m] == block.inverse()
    assert pump.middle_product*pump.outer_product == I
    assert pump.holonomy == I and pump.is_closed
    assert [n for group in pump.coarse_groups for n in group] == list(range(72))
    assert {len(group) for group in pump.coarse_groups} == {7,8}
    assert TorsionalMarkovPump.from_deltas(frames[0], pump.fine_deltas).fine_frames == tuple(frames)


def test_open_noncommutative_history_is_not_forced_closed():
    frames = history(False)
    pump = TorsionalMarkovPump(frames)
    assert X*Y == Z and Y*X == Q(0,0,0,-1)
    assert pump.holonomy == frames[0]*frames[-1].inverse()
    assert not pump.holonomy.is_identity() and not pump.is_closed
    assert pump.holonomy != frames[-1].inverse()*frames[0]
    wrong_order = I
    for delta in pump.middle_deltas:
        wrong_order = delta*wrong_order
    assert wrong_order*pump.outer_product != I


def test_spinor_minus_identity_is_not_positive_identity():
    frames = [I]*720; frames[-1] = Q(-1,0,0,0)
    pump = TorsionalMarkovPump(frames)
    assert pump.holonomy.is_unit() and not pump.is_closed
    assert pump.holonomy.w == -1


def test_general_inverse_is_exact_and_unit_histories_fail_closed():
    q = Q(2,1,0,0)
    assert q*q.inverse() == I
    with pytest.raises(ValueError): Q(0,0,0,0).inverse()
    with pytest.raises(ValueError): Q(1.0,0,0,0)
    with pytest.raises(ValueError): TorsionalMarkovPump([q]*720)
    with pytest.raises(ValueError): TorsionalMarkovPump([I]*719)
    with pytest.raises(ValueError): TorsionalMarkovPump.from_deltas(I, [X]+[I]*719)
