"""Exact quaternion walks as a candidate one-way function (track E1, FAILED).

The idea: encode a digest as a non-backtracking path over the six Lipschitz
quaternions of norm 5 (1 +/- 2i, 1 +/- 2j, 1 +/- 2k, the LPS generators for
p = 5) and publish the product. The product is a quaternion of norm 5**L,
a single geometric object in the Hurwitz order.

It is not one-way. Products of non-backtracking words factor uniquely
(Lipschitz unique factorization for odd primes, Conway and Smith 2003, ch. 5),
so exactly one generator right-divides the product at each step and
``invert_walk`` peels the path off in O(L) exact divisions. Anyone holding a
walk anchor recovers the password. Reducing the walk modulo a prime gives the
LPS / Zemor-type hash, which also has published preimage attacks; see
docs/02_geometric_adaptation.md.

Coordinates are doubled, matching geometric_labs.hurwitz.
"""
from __future__ import annotations

from geometric_labs.hurwitz import H_ONE, HQuat, h_conj, h_mul, h_norm, validate

PRIME = 5
# Index i and i ^ 1 are conjugate, so i ^ 1 is the backtracking step after i.
GENERATORS: tuple[HQuat, ...] = (
    (2, 4, 0, 0), (2, -4, 0, 0),
    (2, 0, 4, 0), (2, 0, -4, 0),
    (2, 0, 0, 4), (2, 0, 0, -4),
)
BRANCHING = len(GENERATORS) - 1
# A fixed virtual predecessor gives the first step five choices too, so a
# path is a plain base-5 numeral.
VIRTUAL_PREVIOUS = 1


def walk_length(byte_length: int) -> int:
    """Smallest L with 5**L >= 256**byte_length; 111 for 32 bytes."""
    if type(byte_length) is not int or byte_length < 1:
        raise ValueError("byte length must be a positive integer")
    length, capacity, target = 0, 1, 1 << (8 * byte_length)
    while capacity < target:
        length, capacity = length + 1, capacity * BRANCHING
    return length


def _allowed(previous: int) -> list[int]:
    return [i for i in range(len(GENERATORS)) if i != previous ^ 1]


def digest_to_path(digest: bytes) -> list[int]:
    """Bijectively map a digest to generator indices (no step undoes the last)."""
    if type(digest) is not bytes or not digest:
        raise ValueError("digest must be nonempty bytes")
    value = int.from_bytes(digest, "big")
    digits = []
    for _ in range(walk_length(len(digest))):
        value, digit = divmod(value, BRANCHING)
        digits.append(digit)
    path, previous = [], VIRTUAL_PREVIOUS
    for digit in reversed(digits):
        previous = _allowed(previous)[digit]
        path.append(previous)
    return path


def path_to_digest(path: list[int], byte_length: int) -> bytes:
    """Inverse of digest_to_path for a path of the right length."""
    if len(path) != walk_length(byte_length):
        raise ValueError("path length does not match the digest length")
    value, previous = 0, VIRTUAL_PREVIOUS
    for step in path:
        allowed = _allowed(previous)
        if step not in allowed:
            raise ValueError("path backtracks")
        value = value * BRANCHING + allowed.index(step)
        previous = step
    if value >> (8 * byte_length):
        raise ValueError("path encodes a value wider than the digest")
    return value.to_bytes(byte_length, "big")


def walk_product(path: list[int]) -> HQuat:
    """Right-multiply the generators along the path, starting from one."""
    q = H_ONE
    for step in path:
        q = h_mul(q, GENERATORS[step])
    return q


def walk_encode(digest: bytes) -> HQuat:
    return walk_product(digest_to_path(digest))


def invert_walk(q: HQuat, length: int) -> list[int]:
    """Recover the unique non-backtracking path of a product (the attack)."""
    q = validate(q)
    if h_norm(q) != PRIME ** length:
        raise ValueError("norm is not 5**length")
    reversed_path = []
    for _ in range(length):
        divisors = [i for i, g in enumerate(GENERATORS)
                    if all(c % PRIME == 0 for c in h_mul(q, h_conj(g)))]
        if len(divisors) != 1:
            raise ValueError("not the product of a non-backtracking walk")
        step = divisors[0]
        q = tuple(c // PRIME for c in h_mul(q, h_conj(GENERATORS[step])))
        reversed_path.append(step)
    if q != H_ONE:
        raise ValueError("walk does not start at one")
    return reversed_path[::-1]


def recover_digest(q: HQuat, byte_length: int) -> bytes:
    """Preimage attack: the walk anchor gives back the hidden digest."""
    return path_to_digest(invert_walk(q, walk_length(byte_length)), byte_length)
