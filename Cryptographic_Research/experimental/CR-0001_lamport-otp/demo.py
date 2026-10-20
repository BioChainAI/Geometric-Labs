#!/usr/bin/env python3
"""CR-0001 walkthrough: a Lamport session over SHD-CCP tile frames, then the
E1 negative control showing a quaternion-walk anchor gives up its password.

    python3 demo.py --length 5 --seed demo
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve()
sys.path[:0] = [str(HERE.parent / "src"), str(HERE.parents[3] / "src")]
import argparse
import hashlib
from geometric_lamport.hurwitz_walk import recover_digest, walk_encode
from geometric_lamport.lamport import LamportClient, LamportServer, new_seed
from geometric_lamport.tile_frame import FRAME_PROFILE, FrameVerifier, encode_frame

ROUTING = {"struct_sel": 1, "stream_slot": 4, "gate_byte": 0x3C}


def short(value: bytes) -> str:
    return value.hex()[:16] + "..."


def run(length: int, seed: bytes) -> None:
    client = LamportClient(seed, length)
    server = LamportServer(client.anchor, length)
    verifier = FrameVerifier(server, **ROUTING)
    print(f"Anchor stored by the server: {short(client.anchor)}  (chain length {length})")
    print(f"Frame profile: {FRAME_PROFILE}, routing {ROUTING}\n")

    captured = None
    for login in range(1, length + 1):
        index = server.challenge()
        frame = encode_frame(index, client.password_for(index), **ROUTING)
        captured = captured or frame
        verdict = "accepted" if verifier.verify_frame(frame) else "rejected"
        print(f"  login {login}: challenge {index}  header {frame[0]:016x}"
              f"  first fragment {frame[1]:016x}  ->  {verdict}")

    print("\nReplay of the first captured frame:",
          "accepted" if verifier.verify_frame(captured) else "rejected")

    print("\nE1 negative control: publish a quaternion walk of a password instead of a hash.")
    victim = LamportClient(seed, length).password_for(length - 1)
    anchor = walk_encode(victim)
    print(f"  walk anchor norm = 5**111, w coordinate has {abs(anchor[0]).bit_length()} bits")
    recovered = recover_digest(anchor, 32)
    print(f"  attacker factors the anchor and recovers {short(recovered)}"
          f"  ({'MATCHES' if recovered == victim else 'differs from'} the next password)")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="CR-0001 Lamport OTP over SHD-CCP tiles")
    parser.add_argument("--length", type=int, default=5)
    parser.add_argument("--seed", help="text seed for a reproducible run")
    args = parser.parse_args(argv)
    if args.length < 1:
        parser.error("length must be at least 1")
    seed = hashlib.sha256(args.seed.encode()).digest() if args.seed else new_seed()
    run(args.length, seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
