# Geometric Labs Pages landing page and update pipeline

Branch: `codex/geometric-labs-pages`, based on main `00a0056d7d28`.
The checkpoint artifacts from the preceding overview task are included in this
review branch; original source/math/vectors/catalogs/registries remain unchanged.
The user's `.github/workflows/static.yml` is deliberately revised to build an
allowlisted site artifact rather than upload the entire checkout.

## Changes

- `site/index.html`, assets and favicon: responsive project landing page with
  project-area cards, development loop, filters, path search, recent commits,
  recorded-evidence panel and Research IDE/checkpoint navigation.
- `site/sections.json`: reviewed ownership/status/path classification. New source
  areas require classification; longest prefixes win and unknown roots fail.
- `tools/pages/build.py`: stdlib scanner, curated artifact builder, history/source
  identity, source/evidence revision distinction, output safety and link validation.
- `tools/pages/tests/`: 12 offline tests, including invalid metadata/evidence,
  directory preservation, build repeatability, output allowlist and dirty-preview gate.
- `tools/pages/browser_smoke.py`: optional repeatable real-Chromium UI checks.
- `site/README.md`: scan/update/evidence/formatting/publication and rollback procedure.
- Pages workflow: read-only PR build and validation, full Git history, clean build,
  artifact upload, separately permissioned main-only Pages deployment. Existing
  scientific workflows stay intact; no automated merge or production model rollout.

## Executed checks

- Existing root make verify-all: PASS (40 methods + master pillars/vector checks).
- Site unit tests: PASS (12 methods).
- Real Chromium via Playwright: PASS on 1440px desktop and 390px mobile, including
  project subpath, filtering, path search, empty/error state, loop selection/reset,
  keyboard skip link, no horizontal mobile overflow, and evidence labels.
- Homepage has no third-party resource requests and no runtime page errors.
- Injected HTML in a commit subject remains inert text; external URLs are not
  automatically fetched by the scanner or homepage.
- Published checkpoint, IDE HTML and maintenance guide routes resolve.
- JavaScript syntax and workflow structure reviewed; deploy-pages v5 tag exists.
- Local build and artifact repeatability/link validation PASS. The clean production
  build is checked after committing this branch. Actual GitHub action/deployment
  execution is not implied by these local checks.

The displayed 140 scientific/checkpoint tests and 183 packet cases retain their
original evidence SHA/date; the site build does not rerun or refresh those results.
Browser evidence is recorded separately, not relabeled as a Lean or scientific pass.

## Publication state and next action

Feature branch is prepared for a reviewable push/PR. Deployment occurs only once
the reviewed changes reach main and GitHub Pages completes its action. A local
preview, artifact, feature-branch push or draft PR is not a live deployment.
This follows the repository's AGENTS.md instruction not to auto-merge main.
