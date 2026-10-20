"""OTP presentation frames on 64-bit SHD-CCP tiles (track E3).

Profile ``cr-0001.otp-frame.v0`` on top of the Geometric-Labs local tile
profile ``geometric-labs-reference-v1``. See docs/03_shd_ccp_tile_binding.md.

A frame is nine uint64 tiles:

    position 0     Form 2  chain index as three CRT residues (881, 883, 887)
    positions 1-8  Form 0  the 256-bit password, 32 bits per tile, big-endian

``step_mux`` carries the position. Every other header field is a caller
routing label and must be identical on all nine tiles, so a frame cannot be
spliced from two streams. The frame carries no authenticator: a tampered
fragment is simply a wrong password, which the Lamport check rejects.
"""
from __future__ import annotations

from geometric_labs.garner_crt import MODULUS
from geometric_labs.tile_codec import FIELDS, decode_form2, decode_tile, encode_form2, encode_tile

FRAME_PROFILE = "cr-0001.otp-frame.v0"
BASE_PROFILE = "geometric-labs-reference-v1"
PASSWORD_BYTES = 32
FRAGMENTS = PASSWORD_BYTES // 4
FRAME_TILES = 1 + FRAGMENTS
INDEX_FORM = 2
FRAGMENT_FORM = 0
MAX_INDEX = MODULUS - 1
ROUTING_FIELDS = tuple(name for name in FIELDS if name not in ("form_id", "step_mux"))


def _routing(headers: dict[str, int]) -> dict[str, int]:
    unknown = set(headers) - set(ROUTING_FIELDS)
    if unknown:
        raise ValueError(f"not routing headers: {sorted(unknown)}")
    return {name: headers.get(name, 0) for name in ROUTING_FIELDS}


def encode_frame(index: int, password: bytes, **routing: int) -> list[int]:
    """Encode one password presentation as nine tiles."""
    if type(index) is not int or not 0 <= index <= MAX_INDEX:
        raise ValueError("index outside the Form-2 CRT range")
    if type(password) is not bytes or len(password) != PASSWORD_BYTES:
        raise ValueError("password must be exactly 32 bytes")
    headers = _routing(routing)
    tiles = [encode_form2(index, step_mux=0, **headers)]
    for position in range(1, FRAME_TILES):
        word = int.from_bytes(password[4 * (position - 1):4 * position], "big")
        tiles.append(encode_tile(word, form_id=FRAGMENT_FORM, step_mux=position, **headers))
    return tiles


def decode_frame(tiles: list[int]) -> tuple[int, bytes, dict[str, int]]:
    """Return (index, password, routing) or raise ValueError on any defect."""
    if not isinstance(tiles, (list, tuple)) or len(tiles) != FRAME_TILES:
        raise ValueError(f"a frame is exactly {FRAME_TILES} tiles")
    decoded = [decode_tile(tile) for tile in tiles]
    routing = {name: decoded[0][name] for name in ROUTING_FIELDS}
    for position, fields in enumerate(decoded):
        if fields["step_mux"] != position:
            raise ValueError(f"tile {position} carries step_mux {fields['step_mux']}")
        expected_form = INDEX_FORM if position == 0 else FRAGMENT_FORM
        if fields["form_id"] != expected_form:
            raise ValueError(f"tile {position} must be Form {expected_form}")
        if any(fields[name] != routing[name] for name in ROUTING_FIELDS):
            raise ValueError("routing headers differ inside one frame")
    index = decode_form2(tiles[0])
    password = b"".join(fields["payload"].to_bytes(4, "big") for fields in decoded[1:])
    return index, password, routing


class FrameVerifier:
    """Wraps a Lamport server: strict frame decode, index check, then verify.

    The index is only a pre-filter. It must equal the server challenge, and
    a matching index never substitutes for the hash check.
    """

    def __init__(self, server, **routing: int) -> None:
        self._server = server
        self._routing = _routing(routing)

    def verify_frame(self, tiles: list[int]) -> bool:
        try:
            index, password, routing = decode_frame(tiles)
            expected = self._server.challenge()
        except (ValueError, RuntimeError):
            return False
        if routing != self._routing or index != expected:
            return False
        return self._server.verify(password)
