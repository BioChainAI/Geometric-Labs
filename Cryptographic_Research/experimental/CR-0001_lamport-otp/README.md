# CR-0001: Lamport one-time passwords, geometric adaptation

| | |
| :--- | :--- |
| **Stage** | experimental |
| **Status** | `[HEURISTIC]` |
| **Version** | 0.1.0 (see [CHANGELOG](CHANGELOG.md)) |
| **Algorithm** | Lamport hash-chain one-time passwords (Lamport 1981; S/KEY, RFC 1760; OTP, RFC 2289) |
| **Upstream reference** | [`Hanzxc/lamport-otp`](https://github.com/Hanzxc/lamport-otp) at `e658632c850f63aeb5c14accc5d5b9fb94248e78`. Used as a behavioural reference only, because it declares no license. No upstream code is vendored. |
| **Frame profile** | `cr-0001.otp-frame.v0` on the Geometric-Labs tile profile `geometric-labs-reference-v1` |

## Question

Can the Lamport hash-chain OTP be adapted to geometric computation and carried on 64-bit SHD-CCP Einstein Tiles for BioChain, without weakening it?

## Findings so far (v0.1.0)

| Track | Question | Result | Tag |
| :--- | :--- | :--- | :--- |
| **B**: baseline | Clean-room classical Lamport, challenge-style | Reproduces every hash value in the upstream README. It also fixes an upstream desync: the upstream client burns a password even when the login message is lost. | reference |
| **E1**: geometric one-way function | Can an exact Hurwitz quaternion walk replace SHA-256 as `H`? | **No.** The walk is a bijection. Unique factorization recovers the input in O(L) exact divisions, about 3 ms for 256 bits. | `[FAILED]` |
| **E2**: reduced walks | Do walks reduced mod q (LPS / Zémor / Tillich–Zémor type) help? | Not implemented. Preimage attacks on LPS and Morgenstern hashes are already published, so this is not pursued as `H`. | `[OPEN]` (closed for LPS) |
| **E3**: SHD-CCP transport | Can an OTP presentation ride on 64-bit tiles? | Yes, as a nine-tile frame: one Form-2 CRT index tile and eight Form-0 fragments. A 32- or 52-bit truncated OTP would fall to brute force. | `[HEURISTIC]` |

Conclusion for v0.1.0: keep a standard hash as the one-way core. The geometric adaptation belongs in the representation and transport layers, not in the security assumption. Details are in [docs/02_geometric_adaptation.md](docs/02_geometric_adaptation.md).

## Layout

| Path | Contents |
| :--- | :--- |
| [`manifest.json`](manifest.json) | Machine-readable metadata, checked by `../../tools/registry.py` |
| [`RESEARCH_LOG.md`](RESEARCH_LOG.md) | Dated, append-only lab notebook |
| [`CHANGELOG.md`](CHANGELOG.md) | Versioned changes |
| [`docs/00_upstream_analysis.md`](docs/00_upstream_analysis.md) | What the upstream does and where it falls short |
| [`docs/01_threat_model.md`](docs/01_threat_model.md) | Assets, adversaries, properties and non-goals |
| [`docs/02_geometric_adaptation.md`](docs/02_geometric_adaptation.md) | Tracks E1–E3, method and results |
| [`docs/03_shd_ccp_tile_binding.md`](docs/03_shd_ccp_tile_binding.md) | Normative draft of `cr-0001.otp-frame.v0` |
| [`docs/04_open_questions.md`](docs/04_open_questions.md) | What blocks promotion |
| [`docs/references.md`](docs/references.md) | Bibliography |
| `src/geometric_lamport/` | `lamport.py` (B), `hurwitz_walk.py` (E1), `tile_frame.py` (E3) |
| `tests/` | 29 unittest cases, including negative fixtures |
| `vectors/` | Deterministic golden vectors and generator (`--check` detects drift) |
| [`demo.py`](demo.py) | Runnable walkthrough |

## Run

From this folder, using Python 3.10+ and only the standard library plus `Geometric-Labs/src`:

```sh
python3 -m unittest discover -s tests -v
python3 vectors/generate_vectors.py --check
python3 demo.py --length 5 --seed demo
```

You can also run `make -C ../.. check` from anywhere in the repository to check every research item.
