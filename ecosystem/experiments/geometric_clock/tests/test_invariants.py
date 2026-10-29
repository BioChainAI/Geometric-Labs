from fractions import Fraction
from dataclasses import FrozenInstanceError
import pytest

from geometric_clock import GeometricEngineInvariants, StatorTier


def test_winding_invariant():
    model = GeometricEngineInvariants()
    assert [t.W_n for t in model.tiers] == [16, 14, 12, 10, 8]
    assert model.winding_sum == 60
    assert model.verify_winding_invariant()
    assert model.major_radii == (15, 35, 65, 105, 155)
    assert model.minor_radii == (4, 6, 8, 10, 12)
    assert model.f_geo == 60.0 and model.tau_Q == 1/60
    assert model.nu_Cs == 9_192_631_770
    assert model.cycles_per_pulse == Fraction(306_421_059, 2)


@pytest.mark.parametrize('n', [-1, 5, True, 1.0, '1'])
def test_tiers_reject_invalid_indices(n):
    with pytest.raises(ValueError): StatorTier(n)


def test_tier_data_is_immutable():
    with pytest.raises(FrozenInstanceError): StatorTier(0).W_n = 0
