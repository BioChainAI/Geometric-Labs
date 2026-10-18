"""Bottom-up twelve-layer SHA-256 chain; blueprint Lemma 15.

This is the supplied chain construction, not a binary Merkle proof tree.
"""
import hashlib
import struct
import zlib

def compute_merkle_12_root(layers: list[int]) -> bytes:
    if len(layers)!=12 or any(type(x) is not int or not 0<=x<2**64 for x in layers):
        raise ValueError("exactly twelve uint64 layers required")
    tau=hashlib.sha256(struct.pack('>Q',layers[-1])).digest()
    for layer in reversed(layers[:-1]):
        tau=hashlib.sha256(struct.pack('>Q',layer)+tau).digest()
    return tau

def crc32_forgery(a: bytes, b: bytes, c: bytes) -> tuple[bytes,int]:
    """Equal-length affine CRC identity; does not forge SHA-256."""
    if not len(a)==len(b)==len(c):
        raise ValueError("equal-length messages required")
    forged=bytes(x^y^z for x,y,z in zip(a,b,c))
    predicted=zlib.crc32(a)^zlib.crc32(b)^zlib.crc32(c)
    return forged,predicted


def forge_crc32_suffix(message: bytes, target: int) -> bytes:
    """Append four bytes to reach any chosen CRC-32 via exact GF(2) elimination.

    Demonstrates why an unkeyed CRC cannot authenticate hostile packets.
    """
    if type(target) is not int or not 0 <= target < 2**32:
        raise ValueError("uint32 target required")
    baseline = zlib.crc32(message + bytes(4))
    basis: dict[int, tuple[int, int]] = {}
    for bit in range(32):
        vector = zlib.crc32(message + (1 << bit).to_bytes(4, 'little')) ^ baseline
        mask = 1 << bit
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = vector, mask
                break
            row, coefficients = basis[pivot]
            vector ^= row
            mask ^= coefficients
    residual = target ^ baseline
    solution = 0
    while residual:
        pivot = residual.bit_length() - 1
        if pivot not in basis:
            raise ArithmeticError("CRC patch matrix is singular")
        row, coefficients = basis[pivot]
        residual ^= row
        solution ^= coefficients
    return message + solution.to_bytes(4, 'little')
