# Archive CI preservation fix and Pages diagnosis

Date: 2026-10-27 (America/Chicago). Base:
`30301853ef7d` (merge of archive PR #7); branch `codex/fix-archive-preservation`.

## Reproduced failure and correction

`make -C ecosystem test` failed before dependency restoration because the Wave 00
preservation test froze the bytes of every original tracked file, including two
navigation documents intentionally updated in archive PR #7. It first reported
a SHA-256 mismatch for root `README.md`; `docs/papers/README.md` also changed.
This reproduces the failure independently of the Python version. The previous
archive pre-push validation missed the ecosystem suite; its library/Pages/core
passes did not establish an ecosystem pass.

The original 66-entry `preservation.v1.json` remains unchanged. A preservation
policy now explicitly permits edits to those two navigation documents and
continues checking all other 64 original files. New or unknown snapshot paths
are immutable by default. Regression tests reject changed/deleted scientific
source, tests, vectors, the architecture blueprint, Makefile and original workflow.
No mathematical source, frozen vector, upstream SHA or protocol semantics changed.

The GEOT verifier's expected offline-test count advances from 20 to 23 to include
the three new preservation regression tests. Its other exact counts stay intact.
The acceptance report now describes untested Python versions relative to the
actually recorded interpreter instead of always claiming Python 3.10 was untested.

## Validation

Full pinned acceptance passes on **Python 3.10.22 and Python 3.12.14**. Both runs
execute baseline/pillars/vectors, 23 offline tests, geometry, doctor, repeated sync,
lock validation, four real-checkout integration tests, 183 packet cases and the
three-agent demo with exact TQF result 576. Original checkout SHAs remain pinned.

The GEOT verifier also passes: 89 unique test methods, protocol checks, synthetic
visual interoperability and lock validation. Research library/archive checks pass
(27 tests), and Pages unit tests pass (14). The real-browser smoke check
passes on desktop and mobile using the `/Geometric-Labs/` project subpath, including
homepage/assets/data and the Research IDE/checkpoint/maintenance routes. It also
visits the exact reported `Research_IDE/index.html` URL and verifies that it
redirects to the canonical `research-ide/index.html` route.

Logs and reports were generated under `/tmp/geometric-fix-final-310/`,
`/tmp/geometric-fix-final-312/`, `/tmp/geometric-fix-geot-checks/`, and
`/tmp/geometric-fix-browser/`; summaries and hashes are in
[machine-readable evidence](archive-ci-pages-validation.json).

## Pages findings and remaining limit

GitHub's public Actions summary records successful build **and deployment** for
[main run 40455672449](https://github.com/BioChainAI/Geometric-Labs/actions/runs/40455672449)
at archive merge `3030185`, with public environment URL:

- Homepage: https://biochainai.github.io/Geometric-Labs/
- Explicit index: https://biochainai.github.io/Geometric-Labs/index.html
- Research IDE: https://biochainai.github.io/Geometric-Labs/research-ide/index.html

The builder copies source `site/index.html` to artifact-root `index.html`.
The reported failing URL was
`https://biochainai.github.io/Geometric-Labs/Research_IDE/index.html`.
That repository-case directory did not exist in the published artifact: the IDE
was published at lower-case `research-ide/index.html`. Pages paths are case-sensitive.
A small static redirect now preserves the reported URL, with a canonical link and
clickable fallback. Artifact validation rejects a missing alias or a wrong/escaping
redirect, and the browser test exercises the redirect under the project subpath.
Root README and the site guide link to the canonical URLs. No deployment workflow
was changed; the alias becomes live after this feature branch is reviewed, merged
and deployed through the existing workflow.

This environment's network proxy denies `biochainai.github.io`
requests with a tunnel 403, so a live-site HTTP status cannot be verified here.
That proxy denial is not the user's reported website 404. API log access is also
denied; public GitHub summary pages were readable. Local browser results and a
successful earlier Actions deployment do not establish that this new redirect is
already deployed. Only the identified compatibility route was added.

The earlier five untracked architecture-investigation artifacts remain separate.
Publication follows a feature-branch push and review; no automatic main merge.
