# Changelog: CR-0001

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow [../../VERSIONING.md](../../VERSIONING.md).

## [Unreleased]

## [0.1.0] - 2026-10-19

### Added
- Clean-room classical Lamport baseline in the challenge style, with a pluggable hash. It is checked against the upstream README values.
- Track E1: an exact Hurwitz/Lipschitz norm-5 walk and its factorization preimage attack, kept as a negative control.
- Track E3: the frame profile `cr-0001.otp-frame.v0`, made of nine tiles (a Form-2 CRT index and eight Form-0 fragments), with a strict `FrameVerifier`.
- Golden vectors `vectors/cr0001_v0.json` and a generator with `--check`.
- Research documents 00–04, references and a runnable demo.
