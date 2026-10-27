# Official ecosystem publication collection

[Read the official catalog](CATALOG.md) · [Machine-readable catalog](CATALOG.json)

The repository owner designated fifteen Academia publications as the official paper
collection on 2026-10-27. The Research IDE now opens **Official releases** by default,
using this generated catalog. Its former six built-in sample excerpts are removed
from the active corpus; their original build remains in Git history.

Select a publication to see its source metadata, repository relevance and labels.
**Open PDF in IDE** retrieves the preserved source, checks SHA-256, then opens its
pages through PDF.js and makes a working transcription in memory. **Academia** and
**Source PDF** provide direct links. Export working edits before reloading the page.
The initial metadata card is not presented as the paper's full text or an audited
transcription. No AI provider is called merely by browsing or opening an official PDF.

Use **Upload PDF**, **Upload .MD**, or **New Paper** for older archived material.
Those actions switch to the separate Research Desk and never promote the imported
document. The default official list contains only the designated current collection.

## Sources and matching decisions

The owner supplied fifteen publication URLs and fifteen uploads. The two Sparsemax
uploads have identical bytes, so one existing entry is used. Delta Encoding, the
Mathematical Model pump, Sparsemax, the full Offload Pump and the Orbital Calculator
also exactly match preserved archive entries and are designated in place.

The short-named Fokker upload is the **companion**, matched to Academia 179087320.
The main sieve publication 179087267 uses the title-matched, 38-page source PDF already
preserved as RP-0008. Its source note explicitly records that provenance; remote
Academia PDF bytes were not verified. New PDFs for the Cubit and Fifteen Lemmas are
preserved as RP-0018 and RP-0020, with the earlier RP-0011 and RP-0006 retained.
Distinct PDF bytes do not by themselves prove changed scientific content or a
publication-version sequence. Unspecified publication dates/versions stay null.

Nine new distinct PDFs plus the existing eleven give twenty preserved document
entries. Fifteen are in the current official collection; five remain archived
references. Publication IDs, filenames, SHA-256 hashes, work families and RP IDs
are separate identifiers.

## Designation, inheritance and status

The `archive.release_record` in each manifest records an
`owner-designated-publication` basis, Academia URL/ID, designation authority/date,
exact source hash and a tracked designation note. This is the user's explicit
publication selection. It does **not** claim peer review, compiler verification,
an approved software release or a newly granted reuse license. Licensing remains
unspecified unless the owner supplies it. Existing technical approval records keep
their separate version/license/evidence requirements.

Current-reference replacements copy repository relevance, tags and topics, with
the older source ID/hash and a metadata snapshot retained in `inheritance`.
The old manifest points to `current_reference`; its original PDF is unchanged.
The official release filter excludes superseded/withdrawn entries. A related
companion can inherit a useful mapping without replacing the main paper.

```sh
# From Research_IDE/. Source ingest and family matching happen first.
python3 tools/releases.py designate RP-0021 \
  --publication-url https://www.academia.edu/123456/Actual_Title \
  --date 2026-10-27 --inherit RP-0006 --replaces RP-0006
make index
make check
python3 tools/releases.py list
python3 tools/releases.py resolve RP-0006  # RP-0020 in this intake
```

Use designation commands only after the owner identifies the official publication
and its relation to existing material. Do not guess replacements from filenames.
`--replaces` requires a reviewed common WORK family. Existing labels and mappings
must survive; explicit current primary ownership wins conflicts, with historical
roles kept in the inheritance record. Component source code, protocol profiles
and registry approvals are not modified by this metadata transfer.

## Validation and publication

`make check` validates the full library, source hashes, official identities,
inheritance, replacement resolution, IDE/loader locks and generated catalogs.
The browser catalog contains only official entries, not the full archive.
Pages copies exactly the selected PDFs plus the local loader and catalog. It
does not publish arbitrary archive files. Both `research-ide/index.html` and the
`Research_IDE/index.html` compatibility redirect remain supported.

Additional local checks:

```sh
node --test Research_IDE/tests/official-corpus.test.cjs  # from repository root
python3 Research_IDE/tools/browser_smoke.py \
  --site-dir /tmp/geometric-official-pages \
  --dependency-dir /tmp/geometric-official-browser-deps \
  --output-dir /tmp/geometric-official-ide-browser
```

The optional browser tool requires Playwright/Chromium and local `pdf.min.js` plus
`pdf.worker.min.js` from **pdfjs-dist@3.11.174**. It blocks other CDNs to exercise
fallbacks and checks real PDF loading and manual imports; it is not a visual
certification of CDN styling, the 3D viewer or AI calls. The Python CI remains
standard-library only. See the wave status report for actual executed checks.
