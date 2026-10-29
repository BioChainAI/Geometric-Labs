"""Complete 64-bit envelope; payload interpretation requires an explicit profile.

The clock uses local `geometric-clock-pulse-v1`, not the unresolved upstream
Form-0 quaternion proposal. Generic packing validates widths, not shape semantics.
"""
from dataclasses import dataclass
from typing import ClassVar, Tuple

WIRE_FORMAT_ID = 'einstein-tile/1'
SEMANTIC_PROFILE_ID = 'geometric-clock-pulse-v1'
FIELD_LAYOUT: Tuple[Tuple[str, int, int], ...] = (
    ('cycle_step', 61, 3), ('wheel_unit', 58, 3), ('structure_selector', 56, 2),
    ('gate_byte', 48, 8), ('step_mux', 44, 4), ('form_id', 40, 4),
    ('stream_slot', 36, 4), ('scale_reg', 32, 4), ('core_word', 0, 32))


@dataclass(frozen=True)
class EinsteinTile:
    cycle_step: int = 0
    wheel_unit: int = 0
    structure_selector: int = 0
    gate_byte: int = 0
    form_id: int = 0
    core_word: int = 0
    step_mux: int = 0
    stream_slot: int = 0
    scale_reg: int = 0
    wire_format_id: ClassVar[str] = WIRE_FORMAT_ID

    def __post_init__(self) -> None:
        for name, _, width in FIELD_LAYOUT:
            value = getattr(self, name)
            if type(value) is not int or not 0 <= value < 1 << width:
                raise ValueError(f'{name} must be uint{width}')

    def pack(self) -> int:
        word = 0
        for name, shift, _ in FIELD_LAYOUT:
            word |= getattr(self, name) << shift
        return word

    @classmethod
    def unpack(cls, word: int) -> 'EinsteinTile':
        if type(word) is not int or not 0 <= word < 1 << 64:
            raise ValueError('word must be uint64')
        return cls(**{name: (word >> shift) & ((1 << width)-1) for name, shift, width in FIELD_LAYOUT})

    def to_bytes(self) -> bytes:
        return self.pack().to_bytes(8, 'big')

    @classmethod
    def from_bytes(cls, data: bytes) -> 'EinsteinTile':
        if type(data) is not bytes or len(data) != 8:
            raise ValueError('exactly eight big-endian bytes required')
        return cls.unpack(int.from_bytes(data, 'big'))
