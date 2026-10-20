#!/usr/bin/env python3
"""Deterministic CR-0001 golden vectors. --check never rewrites the file."""
from pathlib import Path
import sys
HERE = Path(__file__).resolve()
sys.path[:0] = [str(HERE.parents[1] / "src"), str(HERE.parents[4] / "src")]
import argparse
import hashlib
import json
from geometric_lamport.hurwitz_walk import digest_to_path, walk_encode
from geometric_lamport.lamport import build_chain
from geometric_lamport.tile_frame import BASE_PROFILE, FRAME_PROFILE, encode_frame

OUTPUT = HERE.parent / "cr0001_v0.json"
SEED_LABEL = b"CR-0001 golden seed"
LENGTH = 8
ROUTING = {"cycle_step": 1, "wheel_idx": 0, "struct_sel": 2, "gate_byte": 0x5A,
           "stream_slot": 7, "scale_reg": 0}


def build() -> dict:
    seed = hashlib.sha256(SEED_LABEL).digest()
    chain = build_chain(seed, LENGTH)
    frames = [{"index": k, "tiles": [f"{t:016x}" for t in encode_frame(k, chain[k], **ROUTING)]}
              for k in range(LENGTH - 1, -1, -1)]
    walk_input = chain[LENGTH - 1]
    return {
        "schema_version": 1,
        "research_id": "CR-0001",
        "profiles": {"frame": FRAME_PROFILE, "tile": BASE_PROFILE},
        "integer_encoding": "bytes and uint64 tiles are fixed-width hex; quaternions are "
                            "doubled-coordinate JSON decimal integers (bigint reader required)",
        "data": {
            "hash": "sha256",
            "seed_derivation": f"sha256({SEED_LABEL.decode()!r})",
            "length": LENGTH,
            "chain_hex": [h.hex() for h in chain],
            "routing": ROUTING,
            "frames_in_login_order": frames,
            "walk_negative_control": {
                "input_hex": walk_input.hex(),
                "path": digest_to_path(walk_input),
                "product": list(walk_encode(walk_input)),
                "note": "invertible by unique factorization; not a hash",
            },
        },
    }


def render() -> str:
    return json.dumps(build(), indent=1) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail on drift, write nothing")
    args = parser.parse_args(argv)
    text = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text() != text:
            print(f"vector drift: {OUTPUT.name}; run without --check to regenerate")
            return 1
        print(f"Checked {OUTPUT.name}.")
        return 0
    OUTPUT.write_text(text)
    print(f"Wrote {OUTPUT.name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
