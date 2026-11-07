# Wave overhaul-g1: Research IDE dependency and storage update

Branch: `claude/focused-shannon-fa4g77`, based on main `3e63eabe7127`.
Scope: the published Research IDE (`Research_IDE/index.html`, served at
`research-ide/index.html`) and the Circuit-SETH explorer (`site/circuit-seth/explorer.html`),
plus the Pages builder checks that keep them that way. Scientific code, vectors,
catalogs, registries and the dated checkpoint are unchanged.

## Changes

- **Pinned CDN files with integrity hashes.** Every external script and stylesheet on the two
  pages is an exact-version jsDelivr npm file with `integrity` (SHA-384) and
  `crossorigin="anonymous"`. IDE: KaTeX 0.18.11, Marked 18.1.1, DOMPurify 3.4.17 (new),
  PDF.js 4.10.38, Three.js 0.128.0 (r128, as before), Lucide 1.61.0. Explorer: KaTeX 0.18.11.
  The hashes were computed from the npm registry tarballs (each tarball checked against the
  registry's SHA-512); the three KaTeX hashes also match the values in KaTeX's own README.
  `Research_IDE/ide.lock.json` records every URL with its hash.
- **Tailwind runtime script replaced.** The Tailwind v3 runtime script cannot carry an integrity
  hash. Both pages now load a stylesheet prebuilt with Tailwind CSS v3.4.19 from their original
  configuration (`tools/pages/tailwind/`, `build.sh`): `Research_IDE/ide-tailwind.css` and
  `site/circuit-seth/explorer-tailwind.css`. A live-DOM class audit over several IDE states and
  all explorer tabs found no class that the runtime script would have styled and the prebuilt file
  does not (see `tools/pages/tailwind/README.md` for the class names with no v3 rule either way).
- **Content-Security-Policy.** Both pages carry a CSP `<meta>` with `default-src 'none'`.
  IDE: scripts and styles from `'self'` and the exact pinned jsDelivr files (each file listed by
  path, not the whole host), fonts only from KaTeX's pinned `fonts/` folder; network calls to
  `'self'`, `generativelanguage.googleapis.com`, `openrouter.ai` and Ollama at `localhost:11434` /
  `127.0.0.1:11434`; images only from `'self'`, `data:` and `blob:`; no workers, objects, forms or
  base changes. Explorer: its two KaTeX scripts and stylesheet by path, the Google Fonts stylesheet
  (`fonts.googleapis.com/css2`) and font host, KaTeX's font folder; no network calls. `'self'` is
  the shared `biochainai.github.io` origin, which every project site on it shares.
- **PDF.js 4.10.38** as ES modules. The worker module is still preloaded, so parsing stays on the
  page thread as before (no cross-origin Worker); `getDocument` is called with
  `isEvalSupported: false`. The legacy build of the same release was also checked.
- **Rendering of untrusted text.** The Markdown preview (fed by uploaded Markdown/LaTeX, text
  extracted from PDFs and AI responses) now goes through `IdeSafety.renderMarkdown`: LaTeX spans
  are protected, restored as text, and the whole result is sanitised with DOMPurify (HTML profile;
  no style, class, form or script content; named properties prefixed) before display; KaTeX then
  typesets the math. Markdown is parsed by a private Marked instance that writes GFM task markers
  as text and turns images from web addresses into links; links to anchors in the same document
  stay in the tab and point at the prefixed ids. Formula text shown in the LaTeX Deck and the
  flowchart inspector is escaped, and the LaTeX Deck's Copy button passes an index instead of
  embedding the TeX.
- **API keys in memory only.** Gemini and OpenRouter keys are no longer written to or read from
  `localStorage`. Keys saved by earlier builds are deleted on load and the user is told once. The
  Gemini key is sent in the `x-goog-api-key` header instead of the URL query. Provider, model and
  Ollama URL preferences are still remembered.
- **Builder and CI.** `tools/pages/build.py` publishes the new local assets and fails the artifact
  when a published page has an external script/stylesheet (including a scheme-relative one) that is
  not pinned with integrity, or a CSP that is not the single policy in `<head>` ahead of every script
  and stylesheet, or whose script/style sources are anything other than the exact pinned files in
  use and an allowlist of keywords and hashes; font sources must sit inside a pinned stylesheet's
  package. Inline module imports of remote files, import maps and `<base>` are refused. `--verify-remote-integrity` downloads
  each pinned file and compares it with its hash; the Pages workflow runs it on every build.
  The Research IDE workflow runs the new Node tests.
- **Docs.** IDE `CHANGELOG.md`, `README.md`, `WALKTHROUGH.md`, `official/README.md`;
  `site/README.md`; the Circuit-SETH lab README. The explorer's unchanged upload stays in
  `ecosystem/experiments/circuit-seth-get-lab/sources/` with its recorded hash.

## User-visible effects

- **Live Render task lists** show text markers (ballot-box characters U+2611 and U+2610) instead
  of disabled checkboxes; the sanitiser does not allow form controls.
- **Links to an anchor in the same document** (`[text](#id)`) stay in the tab and jump to it; other
  links open in a new tab.
- **Images from web addresses are not loaded in Live Render.** The policy allows images only from
  `'self'`, `data:` and `blob:`, so untrusted Markdown cannot make the browser contact other
  sites. A Markdown image from a web address appears as a link `[image: alt text]`; a raw HTML
  image keeps its alt text. Images embedded as `data:` URIs still render.
- **Reading PDFs needs Chrome or Edge 119, Firefox 121 or Safari 17.4 or later.** PDF.js 4.10.38
  calls `Promise.withResolvers`; on older browsers the IDE says which versions are needed, and
  **Source PDF** still opens official papers.

## Executed checks

| Check | Before (3e63eab) | After |
| :--- | :--- | :--- |
| `make verify-all` | PASS: 16 master checks, 40 tests, 5 vector files | PASS: same counts |
| `make -C Research_IDE check` | PASS: 34 tests | PASS: 48 tests (new `test_ide_security.py`, lock-asset test) |
| `node --test` Research IDE | PASS: 4 tests | PASS: 16 tests (new `ide-safety.test.cjs`) |
| `python -m unittest discover -s tools/pages/tests` | PASS: 15 tests | PASS: 22 tests |
| `tools/pages/build.py` | PASS (clean clone) | PASS (working tree; `--require-clean` runs in CI after commit) |
| `Research_IDE/tools/browser_smoke.py` (Chromium) | not run | PASS, updated for PDF.js 4.10.38 modules |
| `tools/pages/browser_smoke.py` (Chromium) | not run | PASS |

A further Chromium check (outside the repository) served the built artifact locally and answered
jsDelivr requests with the npm tarball bytes: 35 of 35 checks passed. It covered library loading
under the integrity hashes; the Cosmo-ID 3D viewer and the flowchart workbench; no CSP violations
and no console errors on either page; a stored key
deleted on load with a one-time notice; keys never reaching localStorage, sessionStorage, cookies
or IndexedDB; markup in Markdown, an uploaded `.tex` file, a PDF text layer and an AI reply rendered
as inert text while math and code blocks still render; the Gemini key travelling only in the
header; an official PDF and a fixture PDF rendering; an altered DOMPurify file being refused by
the browser, with the preview falling back to escaped text; and the legacy PDF.js build.

After the review changes (path-scoped policy, builder rules, preview behaviour, PDF browser note), a
second Chromium check with the same setup passed 16 of 16: every library and the PDF.js worker
module load under the path-scoped policy and KaTeX's fonts load from the pinned folder; scripts from
other jsDelivr paths (`/gh/`, another npm package) are refused and are the only violations; task
markers, same-document anchor links, image links and raw-image handling behave as described above,
with no request to the image host and no console errors across re-renders; a fixture PDF parses;
with `Promise.withResolvers` removed, opening a PDF shows the browser-version message; the
explorer typesets with no violations.

Not verified from this environment: the live jsDelivr bytes (the session's network refused the
host; CI's `--verify-remote-integrity` step performs this check), Firefox and WebKit (not
installed; the PDF browser floor was checked only by removing `Promise.withResolvers` in
Chromium), Python 3.10 (CI's oldest Research IDE matrix entry; 3.11 to 3.13 pass here), and the Google AI documentation page (unreachable; the Gemini endpoint's CORS
preflight was checked and allows `x-goog-api-key` from `https://biochainai.github.io`).

## Decisions and remaining items

- PDF.js 4.10.38 rather than 5.x/6.x: from 5.x the JPEG 2000 and from 6.x the JBIG2/CCITT
  decoders are separate WebAssembly or JavaScript files fetched at run time, which cannot carry an
  integrity hash from a CDN. In 4.10.38 every decoder sits inside the two hashed modules. The npm
  advisory database lists no advisory for 4.10.38. Moving to a newer release means hosting PDF.js
  from this site; that is left as a follow-up.
- The IDE's CSP keeps `'wasm-unsafe-eval'` for the JPEG 2000 decoder embedded in the PDF.js worker
  module. It does not allow string evaluation.
- Both pages still need `'unsafe-inline'` for scripts: the IDE has about 120 inline event-handler
  attributes. Moving them to `addEventListener` would allow a hash-based policy (follow-up).
- The explorer keeps the Google Fonts stylesheet, which varies by browser and cannot carry an
  integrity hash; the CSP limits it to `fonts.googleapis.com/css2` and the `fonts.gstatic.com`
  font host. Self-hosting the two fonts is a follow-up.
- PDF.js keeps its modern build. The legacy build of 4.10.38 carries its own polyfills and would
  lower the browser floor for PDF reading only; the rest of the page has not been checked on older
  engines. The floor is documented and shown to the user instead; switching later means new
  hashes, lock entries and test updates.
- The builder requires a CSP only on pages that load an external file. The home page and the
  Circuit-SETH tutorial load same-origin files only, and the dated checkpoint is immutable.
- Ollama on a host or port other than `localhost:11434` / `127.0.0.1:11434` is refused by the
  IDE's CSP (documented in the walkthrough).

## Publication state

The branch is prepared for a reviewable pull request; nothing is merged or deployed. Pages
deploys only after review and merge to main, per this repository's AGENTS.md.
