# 04: Open questions

These items block promotion of CR-0001 to `published/`. Each is closed by a research-log entry and, where code changes, a CHANGELOG entry.

| ID | Question | Blocks | Owner input needed |
| :--- | :--- | :--- | :--- |
| Q1 | Which Form ID position is canonical: 40–43 (Geometric-Labs profile), 36–39 (RFC 01 draft), or 60–63 (Kernel Ontology)? | Freezing `cr-0001.otp-frame.v0` and the ontology submission | SHD-CCP spec maintainers |
| Q2 | Which Form IDs should an authentication frame use? Telemetry (0–3) or Memory Offload (12–15)? Does the ontology need a new kernel? | Promotion | SHD-CCP Kernel Ontology |
| Q3 | Is a supersingular isogeny-graph hash (Charles–Goren–Lauter) worth a separate research item as a geometric `H`? | Nothing, since E2 is optional | Research direction |
| Q4 | Seed derivation: derive per-account, per-server, per-epoch seeds from a master secret, for example `HMAC-SHA256(master, context)` or HKDF (RFC 5869), so that `h0` disclosure and seed reuse stay contained. | Promotion | Design review |
| Q5 | Client storage versus time: replace the O(n)-per-login recompute with fractal traversal (Jakobsson 2002; Coppersmith and Jakobsson 2002) at O(log n) storage and time. | Large n only | Benchmark |
| Q6 | BioChain integration: which layer owns accounts, re-registration, rate limiting and the channel binding that defeats the RFC 2289 race attack? Per `ecosystem/` ownership rules, likely `PolyShard-Agent` (client secrets) and `Polycentric-Orchestrator` (verifier state). | Production use | BioChain architects |
| Q7 | Ports: should the frame codec join the C, Rust, Java, Elixir and JS bindings under `SHD-CCP/geometric-engine-*`, and be certified against `vectors/cr0001_v0.json`? | Cross-language conformance | Engine maintainers |
| Q8 | Domain-separated hashing (`H(tag ‖ x)`) versus raw SHA-256 for compatibility with the upstream reference. | Freezing the hash definition | Design review |
