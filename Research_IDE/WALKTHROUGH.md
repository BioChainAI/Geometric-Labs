# Walkthrough: from a PDF to a verified library entry

This guide takes one research paper through the whole pipeline. You start with a PDF and end with a catalogued library entry in git: a checked transcription, an audit, a flowchart, a Lean 4 module and a Cosmo-ID, each with a recorded hash.

You do every step in two places:

* **The IDE** (`index.html` in your browser) is where you read, transcribe, audit and formalize.
* **The library** (`make` commands in this folder) is where the results are filed, hashed and indexed.

For the full reference of every IDE control, the LaTeX rules and the agent DOM API, see [docs/MASTER_OPERATION_GUIDE.md](docs/MASTER_OPERATION_GUIDE.md). Section numbers below such as "Guide §2.5" point into it.

---

## Before you start

**You need**

* A Chromium browser (Chrome, Edge or Brave). Firefox and Safari work, but they download files instead of letting you choose where to save.
* Python 3.10+ and `make`. Both are already required by the rest of this repository.
* An Internet connection. The IDE loads Tailwind, KaTeX, Marked, PDF.js, Three.js and Lucide from public CDNs (listed in `ide.lock.json`).
* Optional: an API key for Google AI Studio or OpenRouter, or a local Ollama, for AI transcription.
* Optional, for Step 12: Lean 4 through [`elan`](https://github.com/leanprover/elan).

**Three rules that prevent lost work**

1. **The IDE keeps everything in memory.** Reloading or closing the tab discards your transcription, flowchart edits and Cosmo-ID history. Export early and often (Step 4 makes this painless).
2. **The IDE does not run Lean.** The InfoView, the `PASS` badges and the node status (`✓ Proven`, `⚡ Tactic Ready`, `🚧 Scaffold`) are labels you set. The 9 built-in flowchart nodes start as `✓ Proven`. A proof counts as checked only after Step 12.
3. **API keys are stored in the browser's `localStorage` in plain text.** Use your own machine and browser profile. Never paste a key into a file in this repository.

---

## Step 1: Launch the IDE

From the repository root:

```sh
cd Research_IDE
make serve            # same as: python3 -m http.server 8080 --bind 127.0.0.1
```

Open <http://localhost:8080/> in Chrome. Use another port with `make serve PORT=9000` if 8080 is busy.

You should see the **SHD-CCP IDE v3.2** badge in the top-left and five zones:

| Zone | Where | What it is |
| :--- | :--- | :--- |
| 1 | Left sidebar | **Corpus Explorer**: workspace tabs, paper list, search, page navigator |
| 2 | Left-centre | **PDF Inspector**: `Visual` canvas or `Raw Text` view of the current page |
| 3 | Centre | **Markdown + LaTeX editor** with line numbers and snippet buttons |
| 4 | Right | Four tabs: **Live Render**, **LaTeX Deck**, **Audit**, **Cosmo-ID** |
| 5 | Modal | **Flowchart & Lean 4** workbench (opened from the top bar) |

Serving over `http://localhost` rather than opening the file directly lets Chrome's **Save to Repo** dialog write files where you choose.

---

## Step 2: Configure AI (optional)

Skip this step if you only want the local, zero-API extraction.

1. Click **`AI: Auto`** in the top-right toolbar.
2. Pick a provider in **AI Provider / Inference Mode**:

   | Option | Setup | Best for |
   | :--- | :--- | :--- |
   | Google AI Studio | Key from <https://aistudio.google.com/apikey>. Model `gemini-2.5-flash` (default), `gemini-3-flash-preview` or `gemini-2.5-pro` | Best vision + maths quality |
   | OpenRouter Free Tier | `sk-or-v1-…` key. Uses `qwen/qwen2.5-vl-72b-instruct:free` | Free cloud alternative |
   | Local Ollama | `ollama pull qwen2.5vl:7b`, then `OLLAMA_ORIGINS="http://localhost:8080" ollama serve`. URL defaults to `http://localhost:11434/api/generate` | Fully offline; nothing leaves your machine |
   | Deterministic Heuristic OCR | Nothing | No network calls at all |

3. Click **Save Configuration**.

> Cloud providers receive the page images and text you send them. Do not use them for papers you are not allowed to share.

---

## Step 3: Create the paper's library entry

Choose a short kebab-case **slug** and a **tier**:

* `core`: a constitution paper of the Geometric Engine (would live in `docs/papers/core/`)
* `series`: a domain, metrology or blockchain paper (`docs/papers/series/`)
* `external`: anything else we are working through (the default)

```sh
make new SLUG=fifteen-lemmas TITLE="The Fifteen Lemmas of the Geometric Engine" TIER=core
```

This prints `Created papers/RP-0001_fifteen-lemmas`. IDs are assigned in order (`RP-0001`, `RP-0002`, …) and never reused. The command also updates `CATALOG.json` and `CATALOG.md`.

Now file the original PDF so the source is preserved next to its outputs:

```sh
python3 tools/library.py ingest RP-0001 ~/Downloads/Fifteen_Lemmas.pdf
```

Then open `papers/RP-0001_fifteen-lemmas/manifest.json` and fill in `authors` and `source` (`citation`, `url`, `license`, `pages`). Open its `README.md` and fill in the citation and a two-line summary.

> PDFs over 95 MiB cannot be pushed to GitHub, and `make check` rejects them. For those, put the URL in `manifest.json` → `source.url` and keep the file out of git (or use Git LFS).

---

## Step 4: Point your downloads at `inbox/`

Every IDE export is a browser download. Send them all to one place:

* **Chrome / Edge / Brave:** Settings → Downloads → turn on **Ask where to save each file before downloading**. When the dialog opens, choose `Research_IDE/inbox/`. Chrome remembers the last folder.
* **Save to Repo** and **Save Audit Prompt v2** open a save dialog in Chrome. Choose `inbox/` there too.

`inbox/` is git-ignored, so half-finished exports are never committed by accident. Step 11 files them into the paper.

---

## Step 5: Load the paper into the IDE

1. In the left sidebar, stay on the **Research Desk** tab (it starts empty). Click its pencil icon to rename it after your paper ID, for example `RP-0001 Fifteen Lemmas`, so screenshots and exports are easy to match up.
2. Click **Upload PDF** (or drag the PDF onto the window).
   * Page 1 renders on the canvas immediately.
   * The IDE scans the **first 15 pages** into the editor automatically. The paper's Markdown filename is the PDF name in lowercase with `_` separators, for example `Fifteen_Lemmas.pdf` → `fifteen_lemmas.md`. Every later export reuses this base name.
3. For papers that are already Markdown or LaTeX, use **Upload .MD** instead (`.md`, `.markdown`, `.tex`, `.txt`). A `.tex` file has its preamble stripped and is converted to Markdown headings with `$…$` / `$$…$$` math.
4. For long papers, use the navigator under the file card: **‹ Prev**, the **Page X of N** dropdown, **Next ›**, and the page-range windows (`1–12`, `13–24`, …).

---

## Step 6: Transcribe to Markdown + LaTeX

The goal is a Markdown file whose maths is valid LaTeX and matches the PDF exactly. Choose the tool by how hard the page is (Guide §2.3):

| Button | Where | Scope | Engine |
| :--- | :--- | :--- | :--- |
| **Page → MD** | Bottom PDF bar | Current page | Local spatial OCR, no API |
| **All Pages (Local)** | Bottom PDF bar | Pages 1…N | Local spatial OCR, no API |
| **AI Page → LaTeX** / **AI Append** | Top bar / bottom bar | Current page | Your AI provider (vision + text) |
| **AI All Pages (1..N)** | Top bar | Pages 1…N | Your AI provider, page by page, with stop/resume |
| **Normalize Math OCR** | Top bar | Whole editor | Deterministic clean-up of Unicode maths and `$` delimiters |

A reliable routine:

1. Run **All Pages (Local)** to get a full first draft quickly.
2. Run **Normalize Math OCR**.
3. Go page by page. Compare the **Visual** canvas with the **Live Render** tab. Where matrices, piecewise definitions or tables came out wrong, use **AI Page → LaTeX** on that page and fix the rest by hand.
4. Use the snippet buttons above the editor for common constructs: `$$..$$`, `\mathcal{C}_0`, `ℤ/30ℤ`, `aff(3)`, `+Lemma`.
5. Follow the typesetting rules in Guide §3.1. The one that bites most often: **inside a Markdown table, never write `|` in maths.** Use `\lvert x \rvert` and `\lVert v \rVert` instead, or the table splits.

**Save as you go.** Click **Save to Repo** every few pages and save into `inbox/`. Replace the previous copy when asked. **Clear MD** needs two clicks, and nothing can undo it.

---

## Step 7: Review equations in the LaTeX Deck

Open the **LaTeX Deck** tab (Zone 4, tab 2). It lists every LaTeX span in the editor (Guide §2.4).

1. Keep the filter on **Core Math** to hide single-letter tokens such as `$x$`. Switch to **Display $$** to see only display equations.
2. Change the grouping to check the paper from different angles:
   * **By Section / Lemma**: does every section have the equations it should?
   * **By Engine Subsystem (Layers I–V)**: which part of the Geometric Engine does each equation feed?
   * **By Rational Trig Tier (0–4)**: is anything that should be exact (Tier 0–3) written with floats or transcendental functions?
3. Click any equation's `#N • Lx` badge to jump to its source line in the editor and fix it there.

---

## Step 8: Audit the transcription

Open the **Audit** tab (Zone 4, tab 3). It runs the SHD-CCP v2 convention rules on the editor text every time you edit (Guide §2.5).

1. Read every finding:
   * **Red `ERROR`** / **amber `WARNING`**: each card explains what it found, what it breaks, and which paper section, `src/geometric_labs/` module and test it relates to.
   * **Blue `CONTRASTIVE PROOF OK`**: the paper states a rejected convention on purpose, as a counterexample. That is fine (whitelist `C1…C15`, Guide §3.4).
   * **Green `OK` / `100% Aligned`**: nothing triggered.
2. For a genuine error, click **Auto-Repair in Editor**. Then read the repaired line yourself. Auto-repair is a pattern rewrite, not a proof.
3. If the paper itself is wrong (not the transcription), **do not repair it.** Write it down instead (item 6 below).
4. Export the audit material into `inbox/`:
   * **Save Audit Prompt v2 (.md)** → `Geometric_Engine_Lemma_Audit_Prompt_v2.md`
   * **Registry (69)** → `canonical_registry.json`
5. For a deeper audit, give an external model (Gemini 2.5 Pro, o3, Claude, …) the audit prompt plus your transcription. Save its full reply as `inbox/YYYY-MM-DD_llm-audit_<model>.md`.
6. Write your own conclusions in `inbox/YYYY-MM-DD_audit-notes.md`: what was checked, what was fixed, what the paper gets wrong, and the epistemic tag for each claim (`[PROVEN]`, `[COMPUTED]`, `[CORRESPONDENCE]`, `[OPEN]`, … Guide §3.4).

> **Seeded-fault self-test.** **Audit v2 Manual** → **Plant S1–S11 Seeded Faults** appends 11 deliberate errors to the editor to show the auditor catching them. Only do this on a throw-away paper (**New Paper**), never on a transcription you are going to save.

---

## Step 9: Build the flowchart and Lean 4 module

Click **Flowchart & Lean 4** in the top bar (Guide §2.7). The workbench has three panes.

1. **Left: Interactive DAG flowchart.** It starts with the canonical 15-lemma blueprint (9 nodes). Adapt it to your paper:
   * **+ Node** adds a theorem node. Use the **Causal Edges** footer and **+** to connect nodes with a labelled arrow.
   * **Layout: TD / LR** switches direction. **Reset** returns to the 15-lemma blueprint and discards your edits.
2. **Centre: Step-by-step logical breakdown** for the selected node.
   * Edit its title, layer, Einstein Tile bit field and exactness tier.
   * Click **Sync LaTeX Deck** (top bar) to attach the paper's equations to matching nodes. Use **+ Attach Eq** for one equation and **+ Add Step** for prose steps. Reorder with ↑ / ↓.
3. **Right: Lean 4 proof editor.**
   * Insert tactics with the buttons (`decide`, `ring`, `omega`, `norm_num`, `linarith`, `group`, `field_simp`), click **+ Append All N Step `have` Blocks**, or use **AI Synthesize Lean 4**.
   * **Set the status honestly.** Leave a node on `🚧 Scaffold (sorry)` until its code really has no `sorry` and has compiled in Step 12. Remember that built-in nodes start as `✓ Proven` whatever their code says.
4. Export into `inbox/`:
   * **Export Lean 4 (.lean)** → `GeometricLabs_<paper>.lean`
   * **Export JSON Bundle** → `Flowchart-Lean4-Bundle-<paper>.json` (Markdown source, nodes, edges, equations, Lean code and the registry summary in one file; this is the richest record of the session)
   * **Export Mermaid + Lean (.md)** → `Guided-Flowchart-Lean4-Walkthrough-<paper>.md` (renders as a diagram on GitHub)

---

## Step 10: Mint a Cosmo-ID snapshot

Open the **Cosmo-ID** tab (Zone 4, tab 4). A Cosmo-ID is a 64-bit word computed from the editor text, displayed as a sigil and a 3D voxel cube (Guide §2.6).

1. Choose the spin state that describes this snapshot:

   | Button | Use it when |
   | :--- | :--- |
   | `+Z (1+2k) DRAFT / INGEST` | First transcription |
   | `+X (1+2i) AUDIT REVIEW` | After the audit |
   | `-Z (1-2k) CANONICAL FINAL` | Transcription, audit and Lean all done |
   | `-X (1-2i) BRANCH / FORK` | A variant or alternative reading |
   | `+Y (1+2j) MERKLE-12 SEAL` / `-Y (1-2j) QRE DEEP LATTICE` | Reserved for SHD-CCP/QRE workflows |

2. Click **Mint State** (or **Mint Cosmo-ID** in the top bar). Snapshots stack up in the version list. Select an older one to see a line diff, and click **Restore** to bring it back into the editor.
3. Export into `inbox/`: **Export Cosmo JSON** → `CosmoID-Ledger-<paper>.json` (all snapshots and their text), and **PNG ↓** → `SHD-CCP-CosmoID-<hex>.png`.

> The Cosmo-ID is derived with FNV-1a, a fast non-cryptographic hash. It labels versions and is not tamper evidence. The library records a SHA-256 for every file, and git history is the audit trail.

---

## Step 11: File the exports into the paper

Your `inbox/` should now hold something like:

```text
inbox/
├── fifteen_lemmas.md
├── Geometric_Engine_Lemma_Audit_Prompt_v2.md
├── canonical_registry.json
├── 2026-10-23_audit-notes.md
├── GeometricLabs_fifteen_lemmas.lean
├── Flowchart-Lean4-Bundle-fifteen_lemmas.json
├── Guided-Flowchart-Lean4-Walkthrough-fifteen_lemmas.md
├── CosmoID-Ledger-fifteen_lemmas.json
└── SHD-CCP-CosmoID-24a81100194a2c05.png
```

File the session:

```sh
make ingest PAPER=RP-0001
```

Each line of the report tells you what happened:

| Prefix | Meaning |
| :--- | :--- |
| `ADD` | New file filed and hashed |
| `REPL` | Replaced an older version (only with `--replace`) |
| `SAME` | Identical to what is already filed; removed from inbox |
| `KEEP` | A **different** file with that name is already filed. Nothing changed; the file stays in `inbox/` |

Handle the exceptions:

* **How your own files are sorted.** Names containing `audit` (`.md`, `.txt`) go to `audits/`, names containing `workflow` go to `workflows/`, other `.md` files go to `markdown/`, and anything else unknown goes to `postprocessing/`.
* **A file landed in the wrong folder.** Re-file it with `--to`; the file and its record move together: `python3 tools/library.py ingest RP-0001 papers/RP-0001_fifteen-lemmas/markdown/llm-reply.md --to audits`. Folders are `source markdown audits lean flowcharts cosmo workflows postprocessing`.
* **A newer transcription after more editing:** `python3 tools/library.py ingest RP-0001 --replace`. The old content is still in git history.
* **Files you created directly inside the paper folder** (for example a Python check in `postprocessing/`): `make track PAPER=RP-0001`. If you edited a filed artifact in place: `python3 tools/library.py track RP-0001 --update`.

Do not let more than one paper's exports pile up in `inbox/`. `ingest` files everything there into the paper you name.

---

## Step 12: Verify the Lean outside the IDE

This is the only step that proves anything. Set up a Mathlib project once:

```sh
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh   # once
lake new geolabs math        # a Lean project that depends on Mathlib
cd geolabs
lake exe cache get           # download prebuilt Mathlib (several GB; avoids hours of compiling)
cat lean-toolchain           # note this version for the record below
```

**Fix the imports first.** The IDE's export repeats `import Mathlib.Tactic` inside each node, after other code. Lean only accepts `import` lines at the very top of a file. Keep one import at the top:

```sh
P=../Geometric-Labs/Research_IDE/papers/RP-0001_fifteen-lemmas/lean
{ echo 'import Mathlib.Tactic'; grep -v '^import Mathlib\.Tactic$' "$P/GeometricLabs_fifteen_lemmas.lean"; } \
  > GeometricLabs_fifteen_lemmas.lean
lake env lean GeometricLabs_fifteen_lemmas.lean
```

The file passes when the command exits with no errors **and** prints no `declaration uses 'sorry'` warnings. Fix what fails: by hand, in the IDE workbench, or with an AI assistant. Then file the working version back into the paper:

```sh
cp GeometricLabs_fifteen_lemmas.lean "$P/GeometricLabs_fifteen_lemmas.lean"
cd ../Geometric-Labs/Research_IDE
python3 tools/library.py track RP-0001 --update
```

Record the result. `lake-verified` needs the toolchain, the exact command and who ran it:

```sh
python3 tools/library.py set RP-0001 --lean-status lake-verified \
  --toolchain "$(cat ~/geolabs/lean-toolchain)" \
  --command "lake env lean GeometricLabs_fifteen_lemmas.lean" \
  --by "your-github-handle"
```

If the module compiles but still has `sorry`, use `--lean-status draft`. If it has no `sorry` but you have not compiled it, use `--lean-status sorry-free`. `make check` refuses `sorry-free` and `lake-verified` while any filed `.lean` file contains `sorry` outside comments.

---

## Step 13: Record results and set the stage

1. **`papers/RP-0001_…/README.md`**: fill the **Key results** table, one row per claim with its paper reference, epistemic tag and where it was checked (audit note, Lean theorem name, `verification/` test). Add open questions.
2. **`RESEARCH_LOG.md`**: append a dated entry with what you did, what you found and what you decided. Never rewrite old entries; add a correction instead.
3. **Set the stage** to the furthest one you have evidence for:

   ```sh
   python3 tools/library.py set RP-0001 --stage verified --tag hurwitz --tag garner-crt
   ```

   `set` prints a `WARNING` for anything the stage still lacks, such as `stage 'audited' needs at least one audits/ artifact`.
4. Run the full check:

   ```sh
   make check
   ```

   It validates every manifest, every SHA-256, untracked files, stage evidence, Lean status, catalog freshness and the IDE hash, then runs the tool's tests. It must print `OK`.

---

## Step 14: Promote and commit

**Promote (optional).** When the paper is a core or series paper and has reached `verified`, copy its transcription into the canonical paper set used by the reference engine:

```sh
cp papers/RP-0001_fifteen-lemmas/markdown/fifteen_lemmas.md ../docs/papers/core/01_fifteen_lemmas_of_the_geometric_engine.md
```

Then update `../docs/papers/README.md`. Follow its Phase 2 note: reconcile section citations and rerun `make verify-all` at the repository root.

**Commit** on a branch and open a pull request:

```sh
git checkout -b research/RP-0001-fifteen-lemmas
git add Research_IDE/papers/RP-0001_fifteen-lemmas Research_IDE/CATALOG.json Research_IDE/CATALOG.md
git commit -m "Research_IDE: RP-0001 Fifteen Lemmas verified"
git push -u origin research/RP-0001-fifteen-lemmas
```

CI reruns `make -C Research_IDE check` on the pull request.

---

## Finding things later

```sh
make list                                              # every paper
python3 tools/library.py list --stage audited          # by stage
python3 tools/library.py list --lean-status draft      # Lean still to finish
python3 tools/library.py list --tier core --tag hurwitz
```

* **`CATALOG.md`** is a browsable table on GitHub with stage counts, Lean status and artifact counts per paper.
* **`CATALOG.json`** is the machine index. Each paper's **`manifest.json`** has the full record, including every artifact's kind, path and SHA-256. For example, with `jq`:

  ```sh
  jq -r '.papers[] | select(.lean_status=="lake-verified") | .id + "  " + .title' CATALOG.json
  jq -r '.artifacts[] | select(.kind=="flowchart-bundle") | .path' papers/RP-*/manifest.json
  ```

* The JSON bundles in `flowcharts/` contain each paper's full Markdown, equations with their tier and registry key, and Lean code. They are the best input for later cross-paper analysis.

## Returning to a paper

The IDE does not remember past sessions, so reload the paper's latest files:

1. **Upload .MD** with `papers/RP-…/markdown/<paper>.md` to continue the transcription.
2. Upload the PDF from `source/` too if you need the page view.
3. Flowchart edits are not reloaded from the JSON bundle. Re-open the workbench, rebuild from **Sync LaTeX Deck**, and paste Lean code back from `lean/`.
4. Export again into `inbox/`, then run `python3 tools/library.py ingest RP-… --replace` so the new versions supersede the filed ones.

## Updating the IDE

1. Replace `index.html` with the new build.
2. Run `make lock-ide` to record its SHA-256 in `ide.lock.json`, and update `ide_version` and `upload_name` there.
3. Add a `CHANGELOG.md` entry naming the new version and what changed. If the export file names changed, update `EXPORT_RULES` in `tools/library.py` and the tests.
4. `make check` fails until step 2 is done, so an unrecorded IDE change cannot slip into a commit.

## Troubleshooting

| Symptom | Fix |
| :--- | :--- |
| Page is unstyled, or the PDF canvas stays blank | CDN scripts are blocked. Check the browser console and your network or ad-blocker. |
| **Save to Repo** downloads instead of opening a dialog | Your browser lacks the File System Access API (Firefox, Safari), or the page is not served from `http://localhost`. Download to `inbox/` instead. |
| AI buttons fall back to local extraction or report an error | Check the key and model in **AI: Auto**. For Ollama, confirm `OLLAMA_ORIGINS` includes `http://localhost:8080` and the model is pulled. |
| Table cells split in **Live Render** | A raw `\|` inside maths in a table row. Use `\lvert … \rvert`. |
| `ingest` says `KEEP` | A different file with that name is already filed. Use `--replace` if the new one supersedes it. |
| `check`: `untracked file` | Run `make track PAPER=RP-…`. |
| `check`: `changed since it was recorded` | You edited a filed artifact. Run `track RP-… --update`, or re-ingest with `--replace`. |
| `check`: `CATALOG.json is stale` | You edited a manifest by hand. Run `make index`. |
| `check`: `index.html does not match ide.lock.json` | See **Updating the IDE**. |
| Lean: `invalid 'import' command` | The duplicate imports from the IDE export. See Step 12. |

## Automating with agents

Everything in Steps 5–10 can be driven headlessly through the IDE's global functions: `extractAllPagesDeterministic()`, `runConventionAuditor()`, `syncEquationsFromCurrentPaperToFlowchart()`, `buildStructuredFlowchartBundle()`, `createVersionSnapshot()` and more. See Guide §5.1 for the table and §5.3 for the loop. An agent then finishes with the same library commands as a person: `ingest`, `track`, `set` and `check`. Keep agent prompts and run logs in the paper's `workflows/` folder.
