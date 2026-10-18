"""Exact geometric reference engine. See docs/specification_status.md for scope."""
from .hurwitz import HQuat, H_ONE, H_TIER, HURWITZ_24_UNITS, h_mul, h_conj, h_norm
__version__ = "0.1.0"
CORE_CUBE = (-1, 1)
VOXEL_CUBE = (-2, 2)
FIBONACCI_CUBE = (-4, 4)
