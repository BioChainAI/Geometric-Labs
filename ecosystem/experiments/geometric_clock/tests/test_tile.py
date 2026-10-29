import json
from pathlib import Path
import random
import pytest

from geometric_clock import EinsteinTile
from geometric_clock.engine.tile import FIELD_LAYOUT


def test_einstein_tile_packing():
    tile = EinsteinTile(cycle_step=2, wheel_unit=3, structure_selector=1, gate_byte=36,
                        step_mux=6, form_id=0, stream_slot=12, scale_reg=0, core_word=0x12345678)
    assert tile.pack() == 0x4d2460c012345678
    assert tile.to_bytes() == bytes.fromhex('4d2460c012345678')
    assert EinsteinTile.unpack(tile.pack()) == tile
    assert EinsteinTile.from_bytes(tile.to_bytes()) == tile


def test_every_bit_and_seeded_word_round_trips_without_holes():
    rng = random.Random(553)
    for word in [0, (1<<64)-1, *(1<<bit for bit in range(64)), *(rng.getrandbits(64) for _ in range(100))]:
        assert EinsteinTile.unpack(word).pack() == word
    maximums = {name: (1<<width)-1 for name, _, width in FIELD_LAYOUT}
    assert EinsteinTile(**maximums).pack() == (1<<64)-1


def test_existing_local_golden_envelopes_unchanged():
    root = Path(__file__).resolve().parents[4]
    fixture = json.loads((root/'spec_sync/golden_vectors/v1_tiles_forms_0_15.json').read_text())
    aliases = {'wheel_idx':'wheel_unit', 'struct_sel':'structure_selector', 'payload':'core_word'}
    for row in fixture['data']['forms']:
        tile = EinsteinTile.unpack(int(row['hex'], 16))
        assert tile.to_bytes().hex() == row['hex']
        assert all(getattr(tile, aliases.get(name,name)) == value for name, value in row['decoded'].items())


@pytest.mark.parametrize('name,shift,width', FIELD_LAYOUT)
def test_invalid_field_values_do_not_truncate(name, shift, width):
    for value in (-1, 1<<width, True, 1.0):
        with pytest.raises(ValueError): EinsteinTile(**{name:value})


@pytest.mark.parametrize('word', [-1,1<<64,True,1.0])
def test_invalid_wire_word_rejected(word):
    with pytest.raises(ValueError): EinsteinTile.unpack(word)


@pytest.mark.parametrize('data', [b'',bytes(7),bytes(9),bytearray(8),0])
def test_wrong_wire_width_or_type_rejected(data):
    with pytest.raises(ValueError): EinsteinTile.from_bytes(data)
