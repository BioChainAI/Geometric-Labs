"""Cramer real-air model transcribed from the supplied reference, Cubit §3.1.

Floating-point physical metrology is separate from exact lattice arithmetic.
The six GUM contributions must be supplied; no instrument budget was attached.
"""
import math
def cramer_sound_speed(temp_c: float, rh_frac: float = 0.5, p_pa: float = 101325.0, x_c: float = 0.00042) -> float:
    """
    Cramer (1993) speed of sound in real air (0 to 30 C) as specified in Cubit Proposal §3.1.
    """
    if not (0 <= temp_c <= 30 and 0 <= rh_frac <= 1 and p_pa > 0 and 0 <= x_c <= 1):
        raise ValueError("outside supported real-air domain")
    T = temp_c + 273.15
    # Enhancement factor f and saturation vapour pressure p_sv
    f = 1.00062 + 3.14e-8 * p_pa + 5.6e-7 * (temp_c**2)
    p_sv = math.exp(1.2811805e-5 * (T**2) - 1.9509874e-2 * T + 34.04926034 - 6.3536311e3 / T)
    x_w = rh_frac * f * p_sv / p_pa

    c0, c1, c2, c3 = 331.5024, 0.603055, -0.000528, 51.471935
    c4, c5, c6, c7 = 0.1495874, -0.000782, -1.82e-7, 3.73e-8
    c8, c9, c10, c11 = -2.93e-10, -85.20931, -0.228525, 5.91e-5
    c12, c13, c14, c15 = -2.835149, -2.15e-13, 29.179762, 0.000486

    v = (
        c0
        + c1 * temp_c
        + c2 * (temp_c**2)
        + (c3 + c4 * temp_c + c5 * (temp_c**2)) * x_w
        + (c6 + c7 * temp_c + c8 * (temp_c**2)) * p_pa
        + (c9 + c10 * temp_c + c11 * (temp_c**2)) * x_c
        + c12 * (x_w**2)
        + c13 * (p_pa**2)
        + c14 * (x_c**2)
        + c15 * x_w * p_pa * x_c
    )
    return v

def local_cubit(temp_c: float, rh_frac: float = .5, p_pa: float = 101325., x_c: float = .00042, f_cal: float = 40.) -> float:
    if f_cal<=0:
        raise ValueError("positive calibration frequency required")
    return cramer_sound_speed(temp_c,rh_frac,p_pa,x_c)/(16*f_cal)

def gum_uncertainty(sensitivities: tuple[float,...], standard_uncertainties: tuple[float,...], k: float = 2.) -> tuple[float,float]:
    """Independent six-term first-order GUM: returns (standard, expanded)."""
    if len(sensitivities)!=6 or len(standard_uncertainties)!=6 or k<=0 or any(u<0 for u in standard_uncertainties):
        raise ValueError("six independent nonnegative uncertainties required")
    u=math.sqrt(sum((c*s)**2 for c,s in zip(sensitivities,standard_uncertainties)))
    return u,k*u

def room_mode(mode: tuple[int,int,int], cubits: tuple[int,int,int], f_cal: float = 40.) -> float:
    if len(mode)!=3 or len(cubits)!=3 or any(n<=0 for n in cubits) or f_cal<=0:
        raise ValueError("positive enclosure dimensions required")
    return 8*f_cal*math.sqrt(sum((l/n)**2 for l,n in zip(mode,cubits)))
