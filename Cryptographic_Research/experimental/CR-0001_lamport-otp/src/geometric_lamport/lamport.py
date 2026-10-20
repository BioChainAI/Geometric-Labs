"""Classical Lamport hash-chain one-time passwords (CR-0001 baseline).

Clean-room implementation of Lamport (1981) in the S/KEY challenge style
(RFC 1760, RFC 2289). The upstream behavioural reference is pinned in the
experiment manifest; no upstream code is copied.

    h0 = seed, h(k+1) = H(h(k)), anchor = h(n)

Index k is the chain position of a password. The server holds one anchor
h(k+1) and challenges for index k; it accepts p when H(p) equals the anchor,
then stores p as the next anchor. The challenge model differs from the
upstream counter model on purpose: a client that derives h(k) from the seed
for the announced index cannot fall out of step when a login message is lost.

Security rests only on the preimage resistance of H. Nothing in the
geometric layers of this experiment adds to it.
"""
from __future__ import annotations

import hashlib
import hmac
import os
from typing import Callable

HashFunction = Callable[[bytes], bytes]


def sha256(value: bytes) -> bytes:
    return hashlib.sha256(value).digest()


def _require_bytes(name: str, value: object) -> bytes:
    if type(value) is not bytes:
        raise TypeError(f"{name} must be bytes")
    return value


def chain_value(seed: bytes, index: int, hash_fn: HashFunction = sha256) -> bytes:
    """Return h(index) by hashing the seed index times; h(0) is the seed."""
    _require_bytes("seed", seed)
    if type(index) is not int or index < 0:
        raise ValueError("index must be a nonnegative integer")
    value = seed
    for _ in range(index):
        value = hash_fn(value)
    return value


def build_chain(seed: bytes, length: int, hash_fn: HashFunction = sha256) -> list[bytes]:
    """Return [h0, ..., h(length)]; the last entry is the registration anchor."""
    _require_bytes("seed", seed)
    if type(length) is not int or length < 1:
        raise ValueError("chain length must be a positive integer")
    chain = [seed]
    for _ in range(length):
        chain.append(hash_fn(chain[-1]))
    return chain


def new_seed() -> bytes:
    """A fresh 32-byte seed from the operating system CSPRNG."""
    return os.urandom(32)


class LamportClient:
    """Keeps only the seed and derives the password for any challenged index.

    Storage is O(1) and each login costs O(index) hashes. Fractal traversal
    (Jakobsson 2002) would reduce that; see docs/04_open_questions.md.
    """

    def __init__(self, seed: bytes, length: int, hash_fn: HashFunction = sha256) -> None:
        if type(length) is not int or length < 1:
            raise ValueError("chain length must be a positive integer")
        self._seed = _require_bytes("seed", seed)
        self._length = length
        self._hash = hash_fn

    @property
    def length(self) -> int:
        return self._length

    @property
    def anchor(self) -> bytes:
        """h(n), handed to the server once at registration."""
        return chain_value(self._seed, self._length, self._hash)

    def password_for(self, index: int) -> bytes:
        """Return h(index) for a server challenge, 0 <= index < length."""
        if type(index) is not int or not 0 <= index < self._length:
            raise ValueError("challenge index outside the chain")
        return chain_value(self._seed, index, self._hash)


class LamportServer:
    """Stores one anchor and the number of passwords left, never the seed."""

    def __init__(self, anchor: bytes, length: int, hash_fn: HashFunction = sha256) -> None:
        if type(length) is not int or length < 1:
            raise ValueError("chain length must be a positive integer")
        self._anchor = _require_bytes("anchor", anchor)
        self._remaining = length
        self._hash = hash_fn

    @property
    def remaining(self) -> int:
        return self._remaining

    @property
    def anchor(self) -> bytes:
        return self._anchor

    def challenge(self) -> int:
        """The index of the password the server expects next."""
        if self._remaining <= 0:
            raise RuntimeError("chain exhausted, re-registration required")
        return self._remaining - 1

    def verify(self, password: bytes) -> bool:
        """Accept p once if H(p) equals the anchor; rejections cost nothing.

        The comparison is constant time. A non-bytes password is rejected
        rather than raised, so callers cannot probe type handling.
        """
        if self._remaining <= 0 or type(password) is not bytes:
            return False
        if hmac.compare_digest(self._hash(password), self._anchor):
            self._anchor = password
            self._remaining -= 1
            return True
        return False
