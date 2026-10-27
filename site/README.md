# Geometric Labs landing page: scan, review and publication

The GitHub Pages homepage is built from source metadata, not a second hand-edited
copy of the repository. `site/index.html` and `site/assets/` provide presentation;
`site/sections.json` is the reviewed section map; `tools/pages/build.py` scans Git
and writes a dedicated output outside the checkout. Only that output is uploaded.

## What updates automatically

On every push to main, pull request, or manual workflow dispatch, the Pages
workflow runs site unit checks, scans the checked-out revision, validates section
classification and local links, and builds the artifact. Pull requests validate
without deploying. Deployment runs only from main, after the build succeeds.

The scan records the exact source SHA, recent eight commits, all tracked paths,
section counts, paper-catalog and crypto-registry entry counts, build timestamp,
and the saved checkpoint evidence's own revision. The current date/build time
is not a new scientific test result. The page does not query GitHub APIs or poll
for live CI status. A deployed static page changes only when rebuilt/deployed.

## Local workflow

From repository root, Python 3.10+ standard library only:

```sh
python3 -m unittest discover -s tools/pages/tests -v
python3 tools/pages/build.py --output /tmp/geometric-labs-pages
python3 -m http.server 8000 --bind 127.0.0.1 --directory /tmp/geometric-labs-pages
```

For the repeatable optional UI check, with Playwright and a compatible Chromium
already available, run:

```sh
python3 tools/pages/browser_smoke.py --site-dir /tmp/geometric-labs-pages --output-dir /tmp/geometric-pages-browser-review
```

This checks the real project subpath, desktop/mobile interactions, errors and
inert rendering of untrusted commit text; it writes screenshots and a JSON report.
It uses a temporary loopback server and closes it afterward. The default Pages
CI stays stdlib-only and does not install browser automation. Install/validate
browser tools separately if that optional lane is adopted in CI.

Use a normal browser to inspect the locally served output. Fetching JSON may be
blocked by browsers if index.html is opened directly as a file. The server is
local-only; no user-facing cloud preview link is needed. Stop it after review.

For a release/CI build add `--require-clean`. Local uncommitted changes produce a
visible preview label: source inventory is the committed HEAD; presentation and
curated metadata can include working changes. Do not publish that as a clean
source release. Output must be outside the checkout. Repeat builds can replace
only a previously marked generated directory; unrelated directories are refused.

## Required scan and update procedure

1. **Inspect:** check branch/SHA/status; preserve local work. Fetch current main
   before choosing a new review branch. Do not auto-merge or reset it.
2. **Classify:** update `site/sections.json` when a new top-level directory or
   conceptual area appears. Each section needs a unique ID, entry file, path
   rules, role, honest status and limitations. Longer prefixes win. Unknown
   paths fail the build; do not add a blanket catch-all to hide them.
3. **Keep formatting consistent:** edit source HTML/CSS/JS and the JSON config,
   never generated status.json. Use UTF-8, valid JSON, relative asset/route links,
   semantic headings, text labels, keyboard focus and responsive layouts. Avoid
   external JS/CSS on the homepage. Treat all commit/path text as text, not HTML.
4. **Review evidence:** the current homepage uses the dated checkpoint at
   `ecosystem/docs/checkpoints/2026-10-25/`. If publishing a new test checkpoint,
   execute relevant suites, retain command exit codes/counts and exact source
   revision, create a new dated record, and deliberately update the builder's
   `CHECKPOINT` constant with the matching source schema. The displayed date is
   derived from that dated directory. Do not
   replace a date or count alone. Ordinary site scans never regenerate vectors
   or claim that historical checks were rerun.
5. **Validate:** run site tests/build; inspect desktop/mobile, search, filters,
   empty/error states, links and recorded-evidence labels. The committed site
   validator checks local root-page links and an artifact allowlist. It does not
   perform external link health checks or verify the older Research IDE browser.
6. **Review the artifact:** it should contain homepage assets/data, selected
   checkpoint files and the standalone Research IDE page—not all source, nested
   repositories, virtualenvs, credentials, raw paper uploads or model artifacts.
   Metadata and history are public site content: review paths and commit subjects
   before publishing a repository with private material.
7. **Publish through review:** commit/push a feature branch, inspect PR checks,
   then merge through the normal review process. The main-branch workflow uploads
   and deploys its validated artifact through the existing GitHub Pages setup.
   Permissions for Pages/OIDC exist only in the deployment job, not the PR build.
8. **Confirm:** inspect the Pages action's deployment result and the homepage SHA.
   A local build or feature-branch push alone does not establish a live deployment.

## Evidence/status semantics

- **Implemented:** an actual code/tool path exists; not automatic production status.
- **Experimental:** runnable research whose scientific/security outcome is unproven.
- **Reference:** context, plans, archived evidence or pedagogy.
- **Planned/blocked:** not counted as an implemented capability.
- **Recorded checkpoint:** historical validation with its own SHA. The page displays
  whether it matches the build revision; a newer commit never inherits its pass.
- The current 140 test methods and 183 packet cases are a historical checkpoint,
  not a claim that the Pages build runs those suites. Existing math/ecosystem,
  Research IDE and cryptographic CI remain independent; Torch tests still need
  their explicitly configured CPU environment.

## Published routes and maintenance

The public homepage is **https://biochainai.github.io/Geometric-Labs/** (or
`https://biochainai.github.io/Geometric-Labs/index.html`). The Research IDE is
`https://biochainai.github.io/Geometric-Labs/research-ide/index.html`.
`site/index.html` is a repository source path; the builder places the homepage
at the published site root. Opening a GitHub source-file URL is not a Pages visit.
The previously shared `/Geometric-Labs/Research_IDE/index.html` URL is preserved
as a static redirect to the canonical lower-case route, including a clickable
fallback link. Pages paths are case-sensitive.

- `index.html`: landing page; `assets/`: first-party CSS/JS.
- `data/status.json`: machine-readable build scan; exact-source GitHub links.
- `checkpoint/`: frozen historical overview/map/inventory and its evidence.
- `research-ide/index.html`: original IDE page copied unchanged. It uses its
  declared external CDN assets and manual exports; Lean is not run in the page.
- `Research_IDE/index.html`: compatibility redirect for the repository-case URL.
- `UPDATE_PROCEDURE.md`: this maintenance procedure.

The project Pages base path is supported through relative URLs (no `/assets/`
root assumptions). The builder has no network or provider-token dependency.
GitHub workflow actions themselves still require GitHub's normal network access.
If upstream APIs or deployment settings change, diagnose their actual errors;
do not disable TLS, suppress failed checks or publish an unvalidated fallback.

Rollback is a reviewed revert to prior site source/workflow followed by a new
main-branch Pages deployment. Do not delete research history or modify core
mathematics to fix presentation. Keep the dated checkpoint immutable.
