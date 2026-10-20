# Changelog: Cryptographic_Research

This file covers the folder structure, tooling and conventions. Each research item keeps its own CHANGELOG.

## [Unreleased]

## [0.1.0] - 2026-10-19

### Added
- Folder scaffold: `experimental/`, `published/`, `archived/`, `templates/experiment/`.
- `VERSIONING.md` (IDs, stages, epistemic tags, semver, git conventions, promotion), `CONTRIBUTING.md` and `ROADMAP.md`.
- `REGISTRY.json` and `tools/registry.py` (`check`, `list`, `new`) with tests.
- `Makefile` targets `check`, `registry`, `test`, `check-vectors`, `list`, `new` and `demo-cr0001`.
- CI workflow `.github/workflows/cryptographic-research.yml`.
- First research item, CR-0001 (Lamport OTP), at v0.1.0.
