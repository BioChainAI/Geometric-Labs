# Research workflow

## Starting an item

```sh
make -C Cryptographic_Research new SLUG=<kebab-case> TITLE="<title>"
```

This copies `templates/experiment` into `experimental/CR-NNNN_<slug>/`, registers the item as `[OPEN]` at version 0.0.1, and advances `next_id`. Then:

1. **Pin the upstream.** Record the URL, a full commit SHA and the license in `manifest.json`. If there is no license, write `"none declared"`, use the upstream as a behavioural reference only, and do not copy its code.
2. **Write `docs/00_upstream_analysis.md`.** Cover what the upstream does, numbered observations, and how equivalence will be tested.
3. **Write `docs/01_threat_model.md`** before any geometric variant exists.

## The research loop

For each idea, open a **track** (E1, E2, …) in `manifest.json` and `docs/02_geometric_adaptation.md`:

1. Write the construction and the falsifiable hypothesis.
2. Implement it in `src/`, using exact integer arithmetic where the repository does (`geometric_labs.hurwitz`, `garner_crt`, `tile_codec`).
3. Write tests that would **refute** the hypothesis, not only confirm it. Include an attack or inversion attempt whenever the track touches the one-way core.
4. Record the outcome as a tagged track status and a research-log entry. A refuted track stays in the code as a negative control.

## Binding to SHD-CCP tiles

* Use `geometric_labs.tile_codec`. Never hand-pack header bits.
* Never truncate a secret or a digest to fit one tile. Spread it across a frame.
* Name the profile (`cr-NNNN.<name>.vN`) and its base tile profile.
* Every rejection rule in `docs/03_shd_ccp_tile_binding.md` gets a negative test.
* Header labels (South Halo, gate byte, routing) never authenticate anything.

## Golden vectors

Vectors must be deterministic: no timestamps, and seeds derived from fixed labels. Encode uint64 tiles as fixed-width hex. Arbitrary-width integers follow the base profile convention. `--check` must fail on drift without writing anything.

## Before every commit

```sh
make -C Cryptographic_Research check
make verify-all          # repository suite must stay green
```

Bump the version and add a CHANGELOG entry when behaviour or bytes change (see [VERSIONING.md](VERSIONING.md)).

## Promotion checklist

- [ ] Every open question is closed or explicitly deferred, with a reason.
- [ ] Wire profiles are frozen and the vectors are final.
- [ ] The threat model has been reviewed by someone other than the author.
- [ ] Ports or conformance plans exist for the `SHD-CCP/geometric-engine-*` bindings, where relevant.
- [ ] The tile layout has been proposed to the SHD-CCP Kernel Ontology incubator, if it defines new Form semantics.
- [ ] The `[PROVEN]` claim, if any, names its Lean theorems or the standard assumption it reduces to.
- [ ] `make check` and `make verify-all` pass in CI.
