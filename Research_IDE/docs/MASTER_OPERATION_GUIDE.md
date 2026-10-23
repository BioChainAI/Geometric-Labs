# Geometric Labs PDF-to-Markdown, LaTeX & Lean 4 Research IDE (`v3.2`) — Master Operation, SHD-QL & Agentic Execution Manual

> **System Designation:** Geometric Labs SHD-CCP Research IDE (`index.html` v3.2) & Integrated **SHD-QL** (*Symbolic High Dimensional Query & Quaternion Language*) Pipeline  
> **Governing Protocol:** Symbolic High Dimensional Context Compression Protocol (**SHD-CCP**, 64-Bit Cubic Einstein Tile Form) & Quaternionic Runtime Environment (**QRE**)  
> **Target Audiences:**  
> 1. **Human Researchers & Mathematical Engineers** (Interactive UI, PDF-to-LaTeX OCR, Flowcharting & Lean 4 Proof Authoring)  
> 2. **Large Language Models (LLMs)** (Multimodal PDF-to-LaTeX Transcription, 7-Stage Auditing & Lean 4 Tactic Synthesis)  
> 3. **Autonomous Coding & Verification Agents** (Headless DOM Automation, SHD-QL Querying, Python `src/geometric_labs/` & Lean 4 CI Pipelines)

---

## Table of Contents

1. [Executive Overview & System Architecture](#1-executive-overview--system-architecture)
2. [Part I: Human Operator Tutorial — End-to-End Workflow](#2-part-i-human-operator-tutorial--end-to-end-workflow)
   - [2.1 Local Setup, Hosting & Free AI Provider Configuration](#21-local-setup-hosting--free-ai-provider-configuration)
   - [2.2 Corpus Explorer Tabs & Multi-Format Ingestion (`.pdf`, `.md`, `.tex`)](#22-corpus-explorer-tabs--multi-format-ingestion-pdf-md-tex)
   - [2.3 Dual-Engine PDF Scanning & Mathematical OCR Normalization](#23-dual-engine-pdf-scanning--mathematical-ocr-normalization)
   - [2.4 Navigating the Hierarchical LaTeX Deck (2,500+ Spans)](#24-navigating-the-hierarchical-latex-deck-2500-spans)
   - [2.5 Running the SHD-CCP v2 7-Stage Auditor & S1–S11 Self-Test](#25-running-the-shd-ccp-v2-7-stage-auditor--s1s11-self-test)
   - [2.6 Minting 64-Bit Einstein Tile Cosmo-IDs & Holographic Versioning](#26-minting-64-bit-einstein-tile-cosmo-ids--holographic-versioning)
   - [2.7 Operating the Flowchart Organizer & Lean 4 Proof Assistant Workbench](#27-operating-the-flowchart-organizer--lean-4-proof-assistant-workbench)
3. [Part II: LLM Specification — LaTeX Conversion, Auditing & Rational Trigonometry](#3-part-ii-llm-specification--latex-conversion-auditing--rational-trigonometry)
   - [3.1 Non-Negotiable Markdown & LaTeX Typesetting Rules](#31-non-negotiable-markdown--latex-typesetting-rules)
   - [3.2 Canonical Mathematical Invariants of the Fifteen Lemmas](#32-canonical-mathematical-invariants-of-the-fifteen-lemmas)
   - [3.3 Rational Trigonometry Laws & Exactness Tiers ($0 \dots 4$)](#33-rational-trigonometry-laws--exactness-tiers-0--4)
   - [3.4 Contrastive-Proof Whitelist ($C_1 \dots C_{15}$) & Epistemic Status Tags](#34-contrastive-proof-whitelist-c_1--c_15--epistemic-status-tags)
4. [Part III: SHD-QL Integrated Code & Algebra Reference](#4-part-iii-shd-ql-integrated-code--algebra-reference)
   - [4.1 SHD-QL Data Types & Doubled Hurwitz Integer Arithmetic ($2q \in \mathbb{Z}^4$)](#41-shd-ql-data-types--doubled-hurwitz-integer-arithmetic-2q-in-mathbbz4)
   - [4.2 64-Bit Einstein Tile Bit-Layout & Form-Dependent Gate Byte](#42-64-bit-einstein-tile-bit-layout--form-dependent-gate-byte)
   - [4.3 SHD-QL Query & Pipeline Syntax for Equations, Tiles & Streams](#43-shd-ql-query--pipeline-syntax-for-equations-tiles--streams)
   - [4.4 Translation Matrix: LaTeX $\leftrightarrow$ Python (`src/geometric_labs/`) $\leftrightarrow$ Lean 4](#44-translation-matrix-latex-leftrightarrow-python-srcgeometric_labs-leftrightarrow-lean-4)
5. [Part IV: Autonomous Agentic Playbook — DOM Hooks, Multi-Export Schemas & CI](#5-part-iv-autonomous-agentic-playbook--dom-hooks-multi-export-schemas--ci)
   - [5.1 Programmatic JavaScript / Playwright DOM API in `index.html`](#51-programmatic-javascript--playwright-dom-api-in-indexhtml)
   - [5.2 Complete Multi-Export Specification (8 Artifacts)](#52-complete-multi-export-specification-8-artifacts)
   - [5.3 Autonomous Agent End-to-End Execution Loop](#53-autonomous-agent-end-to-end-execution-loop)

---

## 1. Executive Overview & System Architecture

The **Geometric Labs PDF-to-Markdown & LaTeX Research IDE (`index.html`)** is a zero-dependency, single-file web application purpose-built to solve the **$>25\text{ MB}$ academic PDF bottleneck** and **floating-point / OCR drift** when translating mathematical monographs into executable codebases (`src/geometric_labs/`) and formal proofs (**Lean 4**).

### The 5-Zone Workspace Topology

| Zone | UI Component | Core Responsibility | Key DOM / State Anchor |
| :--- | :--- | :--- | :--- |
| **Zone 1** | **Corpus Explorer Sidebar** | Dual-tab document manager (`Research Desk` custom workspace + `BioChain AI` constitution corpus), live search/grep, and modular windowed page navigator ($P_1 \dots P_N$). | `#leftSidebar`, `papersState`, `switchCorpusTab()` |
| **Zone 2** | **PDF & Document Inspector** | Dual-mode visual canvas (`PDF.js` offscreen-buffered renderer) and spatial $(x,y)$ raw text stream inspector with local & AI page-level or batch (`1..N`) extraction triggers. | `#pdfRenderCanvas`, `#pdfRawTextArea`, `extractStructuredPdfPageText()` |
| **Zone 3** | **Markdown + LaTeX Code Editor** | Line-numbered source editor with one-click SHD-CCP LaTeX snippets (`$$..$$`, `\mathcal{C}_0`, `\mathbb{Z}/30\mathbb{Z}`, `\mathfrak{aff}(3)`, `+Lemma`), synchronized scroll, and 2-click `Clear MD` safety. | `#markdownEditor`, `#editorLineGutter`, `handleEditorInput()` |
| **Zone 4** | **4-Tab Verification & Version Deck** | **Tab 1 (`Live Render`):** Protected Markdown + KaTeX rendering.<br>**Tab 2 (`LaTeX Deck`):** Hierarchical, filterable equation registry.<br>**Tab 3 (`Audit`):** 7-Stage v2 Auditor (69 checks).<br>**Tab 4 (`Cosmo-ID`):** 64-bit Einstein Tile version control, 2D S-Plane sigil, 3D $\mathcal{V}=[-2,2]^3$ voxel cube, and Git diff. | `#rightPane_preview`, `#rightPane_formulas`, `#rightPane_audit`, `#rightPane_versions` |
| **Zone 5** | **Flowchart & Lean 4 Workbench** | Full-screen 3-pane modal combining an **Interactive SVG DAG Flowchart**, **Step-by-Step Logical Breakdown**, and **Lean 4 Proof Assistant & InfoView**. | `#flowchartStudioModal`, `customFlowchartNodes`, `customFlowchartEdges` |

---

## 2. Part I: Human Operator Tutorial — End-to-End Workflow

### 2.1 Local Setup, Hosting & Free AI Provider Configuration

1. **Running Locally (Recommended for Native Disk Saving):**
   - Place `index.html` inside your repository (e.g., `interactive/index.html` or `docs/index.html`).
   - Start a local HTTP server from your terminal:
     ```bash
     python3 -m http.server 8080
     ```
   - Open `http://localhost:8080/interactive/index.html` in a Chromium-based browser (Chrome, Edge, Brave) to unlock the native **File System Access API** (`window.showSaveFilePicker`), allowing the **`Save to Repo`** button to write `.md` files directly into `docs/papers/core/` or `docs/papers/series/`.
2. **Configuring Your AI Transcription & Synthesis Engine (`AI: Auto` Button):**
   - Click the **`AI: Auto`** gear button in the top-right toolbar to open the AI Configuration Modal (`#aiConfigModal`).
   - Choose one of the four supported inference modes:
     - **Option A — Google AI Studio Free Tier (`gemini-2.5-flash` / `gemini-3-flash-preview` / `gemini-2.5-pro`):** Paste your API key from `aistudio.google.com/apikey`. Best overall multimodal vision + mathematical group-theory reasoning.
     - **Option B — OpenRouter Free Tier (`qwen/qwen2.5-vl-72b-instruct:free`):** Paste your OpenRouter key (`sk-or-v1-...`). Uses Alibaba's 72B document-vision model at zero cost.
     - **Option C — Local Offline Ollama (`qwen2.5vl:7b`):** Run `ollama pull qwen2.5vl:7b` and start Ollama with `OLLAMA_ORIGINS="*" ollama serve`. Runs $100\%$ offline on your local GPU.
     - **Option D — Deterministic Heuristic OCR (`Zero API`):** Uses the built-in spatial $(x,y)$ baseline reconstructor and Unicode-to-LaTeX state machine with zero network calls.

---

### 2.2 Corpus Explorer Tabs & Multi-Format Ingestion (`.pdf`, `.md`, `.tex`)

1. **Dual-Tab Workspace Organization:**
   - **`Research Desk` (Default Empty Tab):** Opens cleanly on startup so you can focus on a single new paper without clutter. Click the **pencil icon** on the tab to rename it to your active research sprint.
   - **`BioChain AI` (Pre-Loaded SHD-CCP Constitution Tab):** Contains the 6 canonical reference documents (`01_fifteen_lemmas_of_the_geometric_engine.md`, `02_fokker_planck_prime_sieve_release.md`, `03_memory_in_the_twelve_engine_hierarchy.md`, `04_standardization_of_the_cubit.md`, `06_linear_ledgers_to_toroidal_matrices.md`, and `README.md`).
2. **Three Ways to Ingest Research Documents:**
   - **Upload PDF (`Upload PDF` blue button or drag-and-drop):** Loads any `.pdf` (even $>25\text{ MB}$ monographs), renders Page 1 immediately onto the visual canvas, and auto-scans up to the first 15 pages into structured Markdown + LaTeX.
   - **Upload Processed Markdown or LaTeX (`Upload .MD` green button or drag-and-drop):** Accepts one or multiple `.md`, `.markdown`, `.tex`, or `.txt` files. Raw `.tex` files are automatically stripped of preamble boilerplate and converted into Markdown headings with `$...$` and `$$...$$` math blocks.
   - **Create Blank Paper (`+ New Paper`):** Initializes a fresh `.md` template pre-configured with a 64-bit Einstein Tile Cosmo-ID.
3. **Modular Adaptive Page Navigation (For 36+ Page Monographs):**
   - When a multi-page PDF or Markdown document is active in the **Corpus Explorer**, a compact navigator appears beneath the file card featuring **`‹ Prev`**, a **`Page X of N`** dropdown, **`Next ›`**, range window selectors (`1–12`, `13–24`, `25–36`), and a 6-column quick-jump grid (`P1` $\dots$ `P12`).

---

### 2.3 Dual-Engine PDF Scanning & Mathematical OCR Normalization

When converting a research PDF into Markdown + LaTeX, you have four granular controls:

| Button / Action | Scope | Engine Used | When to Use It |
| :--- | :--- | :--- | :--- |
| **`Page -> MD`** (Bottom PDF bar) | Current Page | Local Spatial $(x,y)$ OCR | Instant extraction of the active page without using API quota. |
| **`All Pages (Local)`** (Bottom PDF bar) | Pages $1 \dots N$ | Local Spatial $(x,y)$ OCR | Instant full-document extraction of all 36+ pages in seconds. |
| **`AI Page -> LaTeX`** (Top bar) / **`AI Append`** | Current Page | Multimodal Vision + Text LLM | Rewriting pages with complex multi-line matrices, piecewise fractions (e.g., Page 22 $c_{13}$), or dense tables. |
| **`AI All Pages (1..N)`** (Top bar) | Pages $1 \dots N$ | Multimodal Vision + Text LLM | Sequential full-monograph AI transcription with live progress and 1-click stop/resume. |
| **`Normalize Math OCR`** (Top bar) | Active Editor | Deterministic Sanitizer | Repairs raw Unicode symbols, wraps unwrapped standalone equations in `$$...$$`, and wraps inline variables in `$...$`. |

---

### 2.4 Navigating the Hierarchical LaTeX Deck (2,500+ Spans)

A 36-page mathematical monograph like *The Fifteen Lemmas of the Geometric Engine* contains **2,491 LaTeX spans** (~350 load-bearing equations and ~2,140 single-letter variable references like `$x$`, `$n$`, `$p$`). To keep the **LaTeX Deck** (Tab 2 on the right) fast and organized:

1. **Use the 3-Mode Complexity Filter:**
   - **`Core Math` (Default):** Displays only standalone `$$...$$` blocks and inline formulas containing mathematical operators/relations (`=`, `\equiv`, `\in`, `\subset`, `\mapsto`, `\frac`, etc.), hiding single-letter prose tokens.
   - **`Display $$`:** Isolates only major display equations.
   - **`All Tokens`:** Shows all 2,491 spans.
2. **Switch the Grouping Selector:**
   - **`Group: By Section / Lemma`:** Organizes equations under their exact Markdown `#` / `##` / `###` section headings.
   - **`Group: By Engine Subsystem (Layers I–V)`:** Sorts equations into the 5 deductive layers of the Geometric Engine (`Layer I: Synthetic & Projective` through `Layer V: Multi-Engine FCC Stack & 64-Stream Balancer`).
   - **`Group: By Rational Trig Tier (0–4)`:** Sorts equations by their algebraic number field (from `Tier 0: Q / Z Exact` to `Tier 4: Transcendental / Float`).
3. **Click-to-Focus Synchronization:**
   - Clicking any equation's **`#N • Lx`** badge (or clicking the rendered KaTeX box itself) scrolls the Markdown editor (`#markdownEditor`) smoothly to that exact line, selects the LaTeX source text, and illuminates the line numbers in blue in the left gutter.

---

### 2.5 Running the SHD-CCP v2 7-Stage Auditor & S1–S11 Self-Test

Click the **`Audit`** tab (Tab 3 on the right) to inspect your document's compliance with the **SHD-CCP v2 7-Stage Specification** and the **69 exact checks** of `canonical_registry.json`:

1. **Green `OK` / `100% Aligned` State:** Indicates zero mathematical convention errors, zero OCR formula corruptions, and balanced LaTeX delimiters.
2. **Blue `CONTRASTIVE PROOF OK` Cards:** Recognizes when your monograph intentionally states a rejected convention (such as corner-anchored $[0,4]^3$ on Page 3 or left-acting $\delta_{71}\cdots\delta_0$ on Page 19) as a counterexample to prove why the canonical rule is required (**Whitelist $C_1 \dots C_{15}$**).
3. **Red `ERROR` / Amber `WARNING` Cards & One-Click Auto-Repair:**
   - Every finding explains **What the Audit Found**, **What This Breaks in the Geometric Engine**, and **Connected Repository Architecture** (exact paper section, `src/geometric_labs/` Python modules, and `verification/` unit tests).
   - Click **`Auto-Repair in Editor`** on any finding card to automatically rewrite the offending expression into canonical LaTeX.
4. **Testing the Auditor (`Audit v2 Manual` $\to$ `Plant S1–S11 Seeded Faults`):**
   - Click **`Audit v2 Manual`** in the top-right of the Audit tab, then click **`Plant S1–S11 Seeded Faults`**. This appends all 11 canonical test faults from Appendix A of the v2 Audit Prompt into the editor so you can watch the auditor catch and repair every single one.

---

### 2.6 Minting 64-Bit Einstein Tile Cosmo-IDs & Holographic Versioning

Click the **`Cosmo-ID`** tab (Tab 4 on the right) to manage document revisions using the **SHD-CCP 64-Bit Einstein Tile (§6.1)** holographic state tracker:

1. **Select an $S_5$ Spin State Perspective:**
   - Choose one of the 6 multiplier-free $S_5 = \{1 \pm 2i, 1 \pm 2j, 1 \pm 2k\}$ hyperbolic Cayley tree generators to classify your snapshot:
     - **`+Z (1+2k)`:** `DRAFT / INGEST`
     - **`+X (1+2i)`:** `AUDIT REVIEW`
     - **`-Z (1-2k)`:** `CANONICAL FINAL`
     - **`-X (1-2i)`:** `BRANCH / FORK`
     - **`+Y (1+2j)`:** `MERKLE-12 SEAL`
     - **`-Y (1-2j)`:** `QRE DEEP LATTICE`
2. **Mint State (`Mint Cosmo-ID` / `Mint State`):**
   - Computes a deterministic 64-bit hex word partitioned into four 16-bit segments (`TILE [63:48]`, `MUX [47:32]`, `2q in Z^4 [31:16]`, `CRT [15:0]`), updates the **2D S-Plane Sigil** (Square Core $\mathcal{K}$, 8-unit Wheel-30 Circle, and Eisenstein $120^\circ$ Triangle) and the **3D Origin-Centered $\mathcal{V}=[-2,2]^3$ Voxel Cube**, and logs an immutable snapshot for line-by-line Git diffing and 1-click **`Restore`**.

---

### 2.7 Operating the Flowchart Organizer & Lean 4 Proof Assistant Workbench

Click **`Flowchart & Lean 4`** in the top toolbar (or **`Flowchart Studio & Export`** inside the LaTeX Deck) to open the full-screen 3-pane formal verification workbench:

1. **Left Pane (`1. Interactive DAG Flowchart`):**
   - Click any of the 9 canonical subsystem nodes (`NODE_L1_L3` through `NODE_S6_S7`) to inspect its logical steps and Lean 4 proofs.
   - Click **`Layout: TD / LR`** to toggle between Top-Down and Left-to-Right DAG layouts.
   - Click **`+ Node`** in the top bar to add a custom theorem node, or use the **Causal Edges** footer to connect any two nodes with a directed arrow and payload label.
2. **Center Pane (`2. Step-by-Step Logical Breakdown`):**
   - Edit the active node's Title, Deductive Layer, Einstein Tile Bit-Field, and Exactness Tier.
   - Use **`Import Equation from Active Paper's LaTeX Deck`** (`+ Attach Eq`) or **`Sync LaTeX Deck`** in the top bar to pull equations directly from your scanned paper into ordered derivation steps (`Step 1`, `Step 2`, ...), complete with auto-generated Lean 4 `have` obligations.
   - Reorder steps with `↑` / `↓`, edit their LaTeX or prose explanations in place, or click **`+ Add Step`**.
3. **Right Pane (`3. Lean 4 Proof Assistant & InfoView`):**
   - Inspect the live **Lean 4 InfoView Goal State** (showing context, hypotheses, the focused step's `have` obligation, the target $\vdash$ goal, and live `PASS` badges from the 69-check `canonical_registry.json`).
   - Click any tactic button (`decide`, `ring`, `omega`, `norm_num`, `linarith`, `group`, `field_simp`) to insert it into the **Lean 4 Proof Module Editor**, click **`+ Append All Step have Blocks`**, or click **`AI Synthesize Lean 4`** to generate a complete Mathlib4-compatible proof module.

---

## 3. Part II: LLM Specification — LaTeX Conversion, Auditing & Rational Trigonometry

> **Instruction for LLMs:** When invoked by the IDE (via `transcribeCurrentPageWithAiOrFallback()` or `triggerAiLean4Synthesis()`) or when auditing a paper using `Geometric_Engine_Lemma_Audit_Prompt_v2.md`, you must enforce the following mathematical and syntactic rules without exception.

### 3.1 Non-Negotiable Markdown & LaTeX Typesetting Rules

1. **Strict LaTeX Delimiters:**
   - Every inline mathematical variable, symbol, group, or expression must be enclosed in single dollar signs: `$ ... $`.
   - Every standalone equation, multi-line derivation, piecewise definition (`\begin{cases}...\end{cases}`), or matrix (`\begin{pmatrix}...\end{pmatrix}`) must be enclosed in display math blocks:
     ```markdown
     $$
     \mathbf{U}_{\text{even}} = \operatorname{Rot}_y\left(\frac{\pi}{2}\right)\operatorname{Rot}_x\left(-\frac{\pi}{2}\right) = \begin{pmatrix} 0 & -1 & 0 \\ 0 & 0 & 1 \\ -1 & 0 & 0 \end{pmatrix}
     $$
     ```
   - Never emit raw Unicode mathematical symbols outside `$ ... $` or `$$ ... $$` delimiters.
2. **The Markdown Table Pipe-in-Math Rule (Stage A Lint #2 / Seeded Fault `S8`):**
   - Inside any Markdown table row (`| cell 1 | cell 2 |`), **never** write a raw vertical bar `|` inside `$ ... $` (such as `$|g'(v)| \le 1$` or `$|a_k| < 2^b$`), because GitHub Flavored Markdown parses `|` as a column separator *before* MathJax/KaTeX runs, splitting the table cell in half.
   - **Mandatory Replacement:** Always write `\lvert ... \rvert` for absolute values/cardinality and `\lVert ... \rVert` for norms inside Markdown tables:
     - Correct: `$\lVert g'(v) \rVert \le 1$` and `$\lvert a_k \rvert < 2^b$`.
3. **Canonical Symbol Distinctions:**
   - Always distinguish the local acoustic cubit $\mathcal{C}_0$ (`\mathcal{C}_0`), the dimensional winding span $\mathcal{W}_n = W_n \mathcal{C}_0$ (`\mathcal{W}_n`), the dimensionless integer winding count $W_n = 16 - 2n$, the dimensional minor radius $\varrho_n = r_n \mathcal{C}_0$ (`\varrho_n`), and the dimensionless minor radius $r_n = 2n + 4$.

---

### 3.2 Canonical Mathematical Invariants of the Fifteen Lemmas

Every LLM transcription, audit, or Lean 4 proof synthesis must verify and preserve these exact identities from `canonical_registry.json`:

| Registry Key | Governing Lemma / Section | Canonical Mathematical Identity |
| :--- | :--- | :--- |
| `[L1.isotomic_BD=CX=s-b]` | Lemma 1 (Zhao §1) | $BD = CX = s - b \iff BX = CD = s - c, \quad s = \frac{a+b+c}{2}$ |
| `[L2.spiral_center_formula]` | Lemma 2 (Zhao §2) | $\alpha = \frac{c-d}{a-b}, \quad z_0 = \frac{ad-bc}{a-b-c+d}$ |
| `[L3.harmonic_(B,C;E,F)=-1]` | Lemma 3 (Zhao §3) | $\frac{BF}{FC} = \frac{EB}{EC} = \frac{Q_3}{Q_2} \implies (B,C;E,F) = -1, \quad MB^2 = MF \cdot ME$ |
| `[L4.tiers]` | Lemma 4 Part 1 | $R_n = 5n^2+15n+15 \in \{15,35,65,105,155\}, \; r_n = 2n+4, \; W_n = 16-2n, \; r_n+W_n=20, \; W_\Sigma=60$ |
| `[L4.h_powers]` | Lemma 4 Part 4 | $h = \frac{1-i+j+k}{2} \in \mathcal{H}_1, \quad h^2 = -\bar{h}, \; h^3 = -1, \; h^4 = -h, \; h^5 = \bar{h}, \; h^6 = +1$ |
| `[L4.wheel_legendre]` | Lemma 4 Part 5 | $(\mathbb{Z}/30\mathbb{Z})^\times = \mathcal{B}_+ \sqcup \mathcal{B}_-, \quad \mathcal{B}_+ = \{1,11,19,29\}, \quad \mathcal{B}_- = \{7,13,17,23\}$ |
| `[L4.Jg]` | Lemma 4 Part 6 | $J_g = \begin{pmatrix} 3 & 1 \\ 1 & 5 \end{pmatrix}, \quad \det J_g = 14, \quad \lambda = 4 \pm \sqrt{2}, \quad \det(J_g^k - I) = 7, 161, 2569, 37513, 533057$ |
| `[L5.box_primes]` | Lemma 5 Part 4 | $N_{\mathcal{H}}(q) = n \text{ has } 24\sigma_{\text{odd}}(n) \text{ states}; \quad \text{Primes in } [-2,2]^4 = \{2,3,5,7,13\}, \quad \max N = 16$ |
| `[L5.gram_128bit]` | Lemma 5 Part 6(a) | $A_R = 4\left(\lVert u \rVert^2 \lVert v \rVert^2 - \langle u,v \rangle^2\right) = 4(Q_2 Q_3 - \langle u,v \rangle^2) < 2^{86} \quad (\text{two } 64\times 64 \to 128\text{-bit products})$ |
| `[L6.jacobian_degenerate_alphas]` | Lemma 6 Part 4 | $\det J(M,I,J,S,C_p) \neq 0 \iff \alpha \notin \left\{-\frac{1}{2}, \frac{1}{2}, \frac{3}{2}\right\}$ |
| `[L7.valve_current]` | Lemma 7 Part 3 | $\dim\mathfrak{aff}(3) = 9+3=12, \quad H_4 = (H_1 H_2 H_3)^{-1} = \bar{H}_3\bar{H}_2\bar{H}_1, \quad J = \frac{(1-\rho_{ba}\rho_{cb}\rho_{ac})\Pi_+}{Z} > 0$ |
| `[L8.honeycomb_a2=phi^-3]` | Lemma 8 Prop. 6.4 | $a^2 = \sqrt{5}-2 = \phi^{-3}, \quad \cosh\vartheta = \phi, \quad \sinh\vartheta = \sqrt{\phi}, \quad c = \frac{1}{12}, \quad r_{\text{Klein}} = \frac{8}{17} \approx 0.4706 < a \approx 0.4859$ |
| `[L9.max_10bit_triplet]` | Lemma 9 Part 2 | $(p,p+2,p+6) = (881,883,887), \quad M = 690{,}017{,}701, \quad (c_{12},c_{23},c_{13}) = \left(\frac{p+1}{2}, \frac{3p+17}{4}, \frac{5p+29}{6}\right) = (441,665,739)$ |
| `[L10.shells_gaps]` | Lemma 10 Parts 2–3 | $\text{Shells } [11,19], [29,41], [57,73], [95,115], [143,167]\,\mathcal{C}_0; \quad \text{dist}(V,T_0) = (11-2\sqrt{3})\mathcal{C}_0 \approx 7.536\,\mathcal{C}_0 \approx 4.050\text{ m}$ |
| `[L11.windows]` | Lemma 11 Prop. 11.4 | $\nu_{\text{Cs}} = 9{,}192{,}631{,}770 = 2\cdot 3^2 \cdot 5 \cdot 7^2 \cdot 47 \cdot 44{,}351 \equiv 30 \pmod{60}; \quad \text{Windows } (2, 6, 10, 30)\text{ pulses}$ |
| `[L12.right_acting]` | Lemma 12 Parts 1–3 | $(|A_0|,\dots,|A_9|) = (8,7,7,7,7,8,7,7,7,7), \quad Q^{(10)} = \delta_0 \delta_1 \cdots \delta_{71} = (Q^{(12)})^{-1}, \quad H = q_0^{(12)}(q_{719}^{(12)})^{-1}$ |
| `[L13.(1+i)^k]` | Lemma 13 Parts 2–4 | $\operatorname{ord}(q) \in \{1,2,3,4,6\}, \quad (1+i)^2 = 2i, \quad (1+i)^4 = -4, \quad (1+i)^8 = +16$ |
| `[L15.preimages]` | Lemma 15 Parts 1–3 | $64^{12}/2^{64} = 2^{72}/2^{64} = 256, \quad 2^{56}/2^8 = 2^{48}\text{ South Halo fiber}, \quad \tau_d(G) = H(G_d \parallel \tau_{d+1}(G))$ |
| `[S7.balancer_closure_and_Re]` | §7.6–7.7 | $A_j I_j A_j^{-1} E_j = 1 \implies E_j = A_j I_j^{-1} A_j^{-1}, \quad \operatorname{Re}(E_j) = \operatorname{Re}(I_j), \quad E_4 E_3 E_2 E_1 = 1, \quad 4\times 16 = 64\text{ streams}$ |

---

### 3.3 Rational Trigonometry Laws & Exactness Tiers ($0 \dots 4$)

All exact execution paths in the Geometric Engine replace Euclidean distance with **quadrance** $Q(A,B) = \sum_k (a_k - b_k)^2$ and angle with **spread** $s(u,v) = 1 - \frac{(u \cdot v)^2}{Q(u)Q(v)} = \sin^2\theta$.

1. **The Five Laws of Rational Trigonometry (`[RT.*]`):**
   - **Triple Quad Formula (Collinearity):** $(Q_1 + Q_2 + Q_3)^2 = 2(Q_1^2 + Q_2^2 + Q_3^2)$
   - **Pythagoras' Theorem:** $s_3 = 1 \iff Q_1 + Q_2 = Q_3$
   - **Spread Law:** $\frac{s_1}{Q_1} = \frac{s_2}{Q_2} = \frac{s_3}{Q_3}$
   - **Cross Law:** $(Q_1 + Q_2 - Q_3)^2 = 4 Q_1 Q_2 (1 - s_3)$
   - **Triple Spread Formula:** $(s_1 + s_2 + s_3)^2 = 2(s_1^2 + s_2^2 + s_3^2) + 4 s_1 s_2 s_3$
   - **Archimedes' Quadrea & Weitzenböck Bound:** $A_R = (Q_1+Q_2+Q_3)^2 - 2(Q_1^2+Q_2^2+Q_3^2) = 16\,\text{Area}^2$ and $\chi^2 = \frac{A_R}{S^2} \le \frac{1}{3}$.
2. **Exactness Tiers ($0 \dots 4$):**
   - **Tier 0 ($\mathbb{Q}$ / $\mathbb{Z}$ Exact):** Tier laws, harmonic lengths $\frac{1}{3}, \frac{2}{3}, \frac{4}{3}\mathcal{C}_0$, spreads of $90^\circ$ ($1$), $120^\circ$ ($\frac{3}{4}$), $60^\circ$ ($\frac{3}{4}$), $45^\circ$ ($\frac{1}{2}$), $30^\circ$ ($\frac{1}{4}$), Hurwitz integers, Garner CRT constants, and the Ghost Map $G(p)$ at rational $p$.
   - **Tier 1 (Quadratic Fields $\mathbb{Q}(\sqrt{2}), \mathbb{Q}(\sqrt{3}), \mathbb{Q}(\sqrt{5})$):** Apollonius radius $2\sqrt{2}$, corner radius $2\sqrt{3}$, separation gap $11-2\sqrt{3}$, golden ratio $\phi$, Klein cell $a^2 = \sqrt{5}-2 = \phi^{-3}$, and $72^\circ$ dihedral spread $\frac{5+\sqrt{5}}{8}$.
   - **Tier 2 (Quartic Field $\mathbb{Q}(\sqrt{\phi})$, degree 4):** Hyperbolic honeycomb boost entry $\sinh\vartheta = \sqrt{\phi}$ and Ghost coordinates.
   - **Tier 3 (Cubic Field $\mathbb{Q}(\cos\frac{2\pi}{9})$, degree 3):** $C_9$ $40^\circ$ offsets (spread is a root of $64x^3 - 96x^2 + 36x - 3 = 0$) and Step 1 lift $x(s)$.
   - **Tier 4 (Transcendental / Float-Only):** Gibbs factor $e^{-\beta V(x)}$, $\operatorname{arccosh}\phi$, $\operatorname{artanh}\phi^{-3/2}$, and $\ln$ in BCH expansions. Allowed **only** in Helix A (heuristic sampler), `[COMPUTED]` physical lengths, or descriptive remarks.
3. **Critical Rule E4.1 (`[RT.45deg_spread_rational_but_rotation_not]`):**
   - A rational spread does **not** make a rotation rational. Even though $s(45^\circ) = \frac{1}{2} \in \mathbb{Q}$, a 3D rotation by $\theta$ is rational iff $\tan(\theta/2) \in \mathbb{Q}$, and $\tan(22.5^\circ) = \sqrt{2}-1 \notin \mathbb{Q}$.

---

### 3.4 Contrastive-Proof Whitelist ($C_1 \dots C_{15}$) & Epistemic Status Tags

When auditing a paper, never flag a rejected convention (`C1`–`C15`) as an error if the document adopts the canonical rule and cites the rejected convention as a counterexample (`CONTRASTIVE_OK`). Simultaneously, enforce the 9 Epistemic Status Tags (`[PROVEN]`, `[ESTABLISHED]`, `[CORRESPONDENCE]`, `[DEFINITION]`, `[COMPUTED]`, `[EMPIRICAL]`, `[HEURISTIC]`, `[CONJECTURAL]`, `[OPEN]`)—in particular, equal counts like **64 voxels $\leftrightarrow$ 64 real plane sextic isotopy classes** or **64 streams $\leftrightarrow$ 64 tile bits** must be tagged `[CORRESPONDENCE]`, never `[PROVEN]`.

---

## 4. Part III: SHD-QL Integrated Code & Algebra Reference

**SHD-QL** (*Symbolic High Dimensional Query & Quaternion Language*) is the unified symbolic and integer-exact execution layer that binds the IDE's Cosmo-ID engine, the Python reference package (`src/geometric_labs/`), and the Lean 4 formal verification modules (`GeometricLabs.*.lean`).

### 4.1 SHD-QL Data Types & Doubled Hurwitz Integer Arithmetic ($2q \in \mathbb{Z}^4$)

To guarantee **zero floating-point drift** across all CPU/GPU architectures, SHD-QL represents every Hurwitz quaternion $q = (w, x, y, z) \in \mathcal{H} = \mathbb{Z}^4 \cup (\mathbb{Z} + \frac{1}{2})^4$ in **doubled integer coordinates**:

$$
D = 2q = (d_w, d_x, d_y, d_z) \in \mathbb{Z}^4, \qquad d_w \equiv d_x \equiv d_y \equiv d_z \pmod{2}
$$

- **Lipschitz Integers ($\mathbb{Z}^4$):** All four components $(d_w, d_x, d_y, d_z)$ are **even**.
- **Half-Integer Hurwitz Units ($\mathcal{H}_1 \setminus \{\pm 1, \pm i, \pm j, \pm k\}$):** All four components are **odd** (e.g., the order-6 tier spinor $h = \frac{1-i+j+k}{2}$ has doubled representation $2h = (1, -1, 1, 1)$).
- **Exact Integer Multiplication & Quadrance:**
  $$
  2(pq) = \frac{(2p)(2q)}{2}, \qquad N(q) = \frac{d_w^2 + d_x^2 + d_y^2 + d_z^2}{4} \in \mathbb{Z}_{\ge 0}
  $$
- **Multiplier-Free $S_5$ Hyperbolic Cayley Tree Stepping:**
  For the 6 Lipschitz generators of norm $5$, $S_5 = \{1 \pm 2i, 1 \pm 2j, 1 \pm 2k\}$, every child step $q \mapsto q \cdot g$ executes using only binary left-shifts (`<< 1`) and integer additions/subtractions.

---

### 4.2 64-Bit Einstein Tile Bit-Layout & Form-Dependent Gate Byte

Every 64-bit SHD-QL / Einstein Tile word $T_{64} \in \{0,1\}^{64}$ is partitioned as follows (`[S6.bit_partition]`):

$$
T_{64} = \underbrace{[k_{63:61} \mid u_{60:58} \mid S_{57:56} \mid G_{55:48}^{(\text{Form})} \mid M_{47:44} \mid F_{43:40} \mid J_{39:36} \mid R_{35:32}]}_{\text{32-Bit Deterministic Header (Bits 63:32)}} \parallel \underbrace{P_{31:0}^{(\text{Form})}}_{\text{32-Bit Core Word (Bits 31:0)}}
$$

| Bit Range | Width | SHD-QL Field Identifier | Encoding & Form-Dependent Semantics |
| :--- | :--- | :--- | :--- |
| **`63:61`** | 3 bits | `TILE.cycle_step` ($k$) | $k \in \{0,\dots,7\} \leftrightarrow \theta_{k+1} = (k+1)\frac{\pi}{4}$ and projective spinor $(1+i)^{k+1}$. Top 8 bits `63:56` form the $O(1)$ **South Halo** cache pre-filter (`SH_ID`). |
| **`60:58`** | 3 bits | `TILE.wheel_unit` ($u$) | Index into $(\mathbb{Z}/30\mathbb{Z})^\times = \{1,7,11,13,17,19,23,29\}$, partitioned by $\left(\frac{u}{5}\right)$ into $\mathcal{B}_+$ and $\mathcal{B}_-$. |
| **`57:56`** | 2 bits | `TILE.structure` ($S$) | Single engine: `00,01,10` = $\mathcal{M}^{(1..3)}$, `11` = $H_4 = (H_1 H_2 H_3)^{-1}$. Four-structure balancer (§7.6): `00` = Input $I$, `01` = Balancer $A$, `10` = Inverse $\bar{A}$, `11` = Emergent $E$. |
| **`55:48`** | 8 bits | `TILE.gate_byte` ($G$) | **Strictly Form-Dependent (§6.1 Table 5):**<br>• **Forms 0–2:** Geometric Gate — Bits `55:53` Locus ($0..4 = T_0..T_4$, $5=K$, $6=V$, $7=W$), Bits `52:50` $C_9/D_3$ sector + sense $\sigma_r$, Bits `49:48` Harmonic flag (`00`=$C_0$, `01`=$\frac{4}{3}C_0$, `10`=Apollonius, `11`=Holonomy $H$).<br>• **Form 3:** Bits `55:54` Quad-slice component $(w,x,y,z)$ + Bits `53:48` 6-bit slice counter.<br>• **Forms 4–15:** 8-bit Codex Sub-Region Index. |
| **`47:44`** | 4 bits | `TILE.step_mux` ($M$) | Steps 1–2: circle phase $s \in \mathbb{Z}/9\mathbb{Z}$; Step 3: half-cube $0..15$; Step 6: Ghost cell $0..6$; other steps: $\mathfrak{aff}(3)$ coordinate $0..11$. |
| **`43:40`** | 4 bits | `TILE.form_id` ($F$) | `0`: Smallest-three; `1`: Doubled Hurwitz $2Q$; `2`: Prime-Triplet CRT $(881,883,887)$; `3`: Exact IEEE-754 binary32; `4..15`: Codex shapes. |
| **`39:36`** | 4 bits | `TILE.stream_slot` ($J$) | `0..11`: Engine position in 12-engine cuboctahedral ring; `12..15`: Orthogonal projections $(w,x,y,z)$. Combines with Bits `57:56` to form the 6-bit Stream ID ($0..63$). |
| **`35:32`** | 4 bits | `TILE.scale_reg` ($R$) | Dyadic level $l$, Fibonacci index $m \le 15$ ($F_{15}=610$), or geodesic frequency $\nu$ (Form 8). |
| **`31:0`** | 32 bits | `TILE.core_word` ($P$) | Decoded according to `TILE.form_id` ($F$). |

---

### 4.3 SHD-QL Query & Pipeline Syntax for Equations, Tiles & Streams

Agents and power users can filter and pipeline equations, Cosmo-IDs, and 64-stream states using SHD-QL expressions in the IDE search bars (`#corpusSearchInput`, LaTeX Deck filter) or in Python/Lean scripts:

```sql
-- 1. Query Core Equations in Layer III belonging to Exactness Tier 0 or Tier 2
SELECT formula_index, latex, registry_key, rt_label
FROM LatexDeck
WHERE role != 'Inline Symbol ($x$)'
  AND subsystem LIKE 'Layer III%'
  AND rt_tier IN (0, 2);

-- 2. Verify Form 2 Garner CRT Tile Reconstruction over M = 690,017,701
DECODE TILE 0x24A81100_194A2C05
  WITH FORM = 2,
       PRIME_TRIPLET = (881, 883, 887),
       INVERSES = (441, 665, 739)
  ASSERT south_halo_match(0x24) AND garner_roundtrip == TRUE;

-- 3. Verify 64-Stream Four-Structure Balancer Closure at Cycle Step k = 6 (Offload Window)
VERIFY STREAM_MATRIX (I[0..11], A[0..11], A_bar[0..11], E[0..11])
  WHERE cycle_step == 6 AND spinor_reduced == '-i'
  ASSERT ALL j IN 0..11 SATISFY (A[j] * I[j] * A_bar[j] * E[j] == 1)
  AND Re(E[j]) == Re(I[j])
  AND (E[3] * E[2] * E[1] * E[0] == 1);
```

---

### 4.4 Translation Matrix: LaTeX $\leftrightarrow$ Python (`src/geometric_labs/`) $\leftrightarrow$ Lean 4

Use this side-by-side rosetta stone when converting mathematical statements from the IDE's Markdown/LaTeX editor into Python verification code and Lean 4 formal proofs:

#### Example 1: Doubled Hurwitz Spinor $h = \frac{1-i+j+k}{2}$ Order-6 Identity (`[L4.h_powers]`)

* **Canonical LaTeX (Zone 3 / LaTeX Deck):**
  $$
  2h = (1, -1, 1, 1) \in \mathbb{Z}^4, \qquad 2(pq) = \frac{(2p)(2q)}{2}, \qquad h^3 = -1, \qquad h^6 = +1
  $$
* **Python Reference (`src/geometric_labs/hurwitz.py`):**
  ```python
  def h_mul_2q(p: tuple[int, int, int, int], q: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
      pw, px, py, pz = p
      qw, qx, qy, qz = q
      return (
          (pw * qw - px * qx - py * qy - pz * qz) // 2,
          (pw * qx + px * qw + py * qz - pz * qy) // 2,
          (pw * qy - px * qz + py * qw + pz * qx) // 2,
          (pw * qz + px * qy - py * qx + pz * qw) // 2,
      )

  H_SPINOR_2Q = (1, -1, 1, 1)
  ONE_2Q = (2, 0, 0, 0)
  NEG_ONE_2Q = (-2, 0, 0, 0)
  ```
* **Lean 4 Formal Proof (Zone 5 / `GeometricLabs.LayerII`):**
  ```lean4
  structure Hurwitz2Q where
    dw : Int
    dx : Int
    dy : Int
    dz : Int
    deriving DecidableEq, Repr

  def mul2Q (p q : Hurwitz2Q) : Hurwitz2Q :=
    { dw := (p.dw * q.dw - p.dx * q.dx - p.dy * q.dy - p.dz * q.dz) / 2
    , dx := (p.dw * q.dx + p.dx * q.dw + p.dy * q.dz - p.dz * q.dy) / 2
    , dy := (p.dw * q.dy - p.dx * q.dz + p.dy * q.dw + p.dz * q.dx) / 2
    , dz := (p.dw * q.dz + p.dx * q.dy - p.dy * q.dx + p.dz * q.dw) / 2 }

  def h_spinor : Hurwitz2Q := ⟨1, -1, 1, 1⟩
  def one2Q : Hurwitz2Q := ⟨2, 0, 0, 0⟩
  def negOne2Q : Hurwitz2Q := ⟨-2, 0, 0, 0⟩

  theorem lemma4_spinor_order6 :
      let h2 := mul2Q h_spinor h_spinor
      let h3 := mul2Q h2 h_spinor
      let h6 := mul2Q h3 h3
      h3 = negOne2Q ∧ h6 = one2Q := by
    decide
  ```

#### Example 2: Closed-Form Garner CRT Reconstruction for $(881, 883, 887)$ (`[L9.max_10bit_triplet]`)

* **Canonical LaTeX (Zone 3 / LaTeX Deck):**
  $$
  c_{12} = \frac{p+1}{2} = 441, \quad c_{23} = \frac{3p+17}{4} = 665, \quad c_{13} = \frac{5p+29}{6} = 739, \quad M = 881 \cdot 883 \cdot 887 = 690{,}017{,}701
  $$
* **Lean 4 Formal Proof (Zone 5 / `GeometricLabs.LayerIV`):**
  ```lean4
  def garnerDecode881 (x1 x2 x3 : Nat) : Nat :=
    let u1 := x1
    let u2 := ((x2 + 883 - (u1 % 883)) * 441) % 883
    let t13 := ((x3 + 887 - (u1 % 887)) * 739) % 887
    let u3 := ((t13 + 887 - (u2 % 887)) * 665) % 887
    u1 + u2 * 881 + u3 * 881 * 883

  theorem lemma9_garner_sample_roundtrip :
      let X := 424242424
      garnerDecode881 (X % 881) (X % 883) (X % 887) = X := by
    decide
  ```

---

## 5. Part IV: Autonomous Agentic Playbook — DOM Hooks, Multi-Export Schemas & CI

Autonomous browser agents (Playwright, Puppeteer, Selenium, or WebDriver) and coding agents (GPT Codex, Claude Code) can drive `index.html` programmatically without human intervention using its global `window` functions and DOM state objects.

### 5.1 Programmatic JavaScript / Playwright DOM API in `index.html`

| Agent Objective | JavaScript Function Call / Global State | Return / Side Effect |
| :--- | :--- | :--- |
| **Switch Corpus Tab** | `window.switchCorpusTab('biochain' \| 'custom')` | Switches between the pre-loaded `BioChain AI` corpus and the custom workspace tab. |
| **Select Paper by ID** | `await window.selectPaper('core_01')` | Loads paper into `#markdownEditor`, updates LaTeX Deck, Auditor, and PDF viewer. |
| **Extract All PDF Pages (Zero-API)** | `await window.extractAllPagesDeterministic()` | Runs spatial $(x,y)$ math OCR across all $1 \dots N$ PDF pages and populates `#markdownEditor`. |
| **Extract All PDF Pages (AI Vision)** | `await window.triggerAiAllPagesToLatex()` | Sequentially transcribes pages $1 \dots N$ via the configured multimodal LLM. |
| **Normalize Math OCR** | `window.runDeterministicLatexSanitizer()` | Repairs Unicode math symbols and wraps standalone/inline equations in `$$...$$` and `$...$`. |
| **Inspect Extracted LaTeX Registry** | `window.extractedFormulasRegistry` | Returns array of `{ idx, isDisplay, latex, startLine, endLine, sectionHeading, rtTier, rtLabel, subsystem, registryKey, actionSummary }`. |
| **Focus Equation in Editor** | `window.focusFormulaInEditor(formulaIdx)` | Scrolls `#markdownEditor` to the equation's exact line and highlights its source span. |
| **Run 7-Stage Convention Auditor** | `window.runConventionAuditor()` | Evaluates `SHD_CCP_AUDIT_RULES` against `#markdownEditor.value` and updates `#conventionAuditList`. |
| **Auto-Repair Audit Rule** | `window.applyAuditRuleFix('RULE_06_GARNER_CRT')` | Applies the canonical regex/AST fix for the specified rule ID directly to `#markdownEditor`. |
| **Mint 64-Bit Cosmo-ID Snapshot** | `window.selectCosmoSpin(1); window.createVersionSnapshot('Agent Verified')` | Computes `computeShdCcpCosmoId()`, updates 2D Sigil & 3D Voxel Cube, and prepends to `paper.versions`. |
| **Sync Paper Equations to Flowchart** | `window.syncEquationsFromCurrentPaperToFlowchart()` | Attaches non-trivial equations from `extractedFormulasRegistry` to matching `customFlowchartNodes`. |
| **Build Full Flowchart + Lean 4 Bundle** | `window.buildStructuredFlowchartBundle()` | Returns the complete machine-readable JSON object containing Markdown, DAG nodes/edges, equations, Lean 4 code, and the 69-check registry. |

---

### 5.2 Complete Multi-Export Specification (8 Artifacts)

The IDE produces **8 distinct, standardized output artifacts** for downstream repositories, formal theorem provers, and documentation portals:

| # | Export Button / Function | Output Filename Pattern | Format | Downstream Consumer |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **`Save to Repo`** (`saveMarkdownToDisk()`) | `<paper_filename>.md` | Markdown + LaTeX | GitHub `docs/papers/core/` & `docs/papers/series/`, GPT Codex Phase 2 |
| **2** | **`Export Lean 4 (.lean)`** (`exportLean4File()`) | `GeometricLabs_<paper>.lean` | Lean 4 (`Mathlib.Tactic`) | Lean 4 compiler (`lake build` / `leanprover/lean4:v4.12.0`) |
| **3** | **`Export JSON Bundle`** (`exportFlowchartJsonBundle()`) | `Flowchart-Lean4-Bundle-<paper>.json` | JSON (`v3.0` Schema) | Interactive Flowchart Web Apps, Automated Proof Pipelines |
| **4** | **`Export Mermaid + Lean (.md)`** (`exportFlowchartMermaidMarkdown()`) | `Guided-Flowchart-Lean4-Walkthrough-<paper>.md` | Markdown + Mermaid DAG + Lean 4 | GitHub READMEs, Obsidian, MkDocs / Docusaurus |
| **5** | **`Save Audit Prompt v2 (.md)`** (`saveGeometricEngineAuditPromptMarkdown()`) | `Geometric_Engine_Lemma_Audit_Prompt_v2.md` | Markdown Prompt | External Mathematical Auditor LLMs (Gemini 2.5 Pro, o3, Claude) |
| **6** | **`Registry (69)`** (`exportCanonicalRegistryJson()`) | `canonical_registry.json` | JSON (69 Exact Checks) | `audit_reference.py`, CI Conformance Suites |
| **7** | **`Export Cosmo JSON`** (`exportCosmoLedgerJson()`) | `CosmoID-Ledger-<paper>.json` | JSON (`SHD-CCP-CosmoID-v3.0`) | QRE Blockchain Attestation & Version History Backup |
| **8** | **`PNG ↓`** (`downloadCosmoSigilPng()`) | `SHD-CCP-CosmoID-<16_hex>.png` | PNG Image | Visual Cryptographic Verification Stamp for Releases |

---

### 5.3 Autonomous Agent End-to-End Execution Loop

When an autonomous agent is tasked with processing a new research PDF, auditing it against the Fifteen Lemmas, and verifying its Lean 4 and Python implementations, it should execute the following 6-step deterministic loop:

```text
[STEP 1: INGEST & TRANSCRIBE]
  ├── Load PDF into IDE (`loadUploadedPdfFile`)
  ├── Run `extractAllPagesDeterministic()` (or `triggerAiAllPagesToLatex()` for scanned/table-heavy PDFs)
  └── Run `runDeterministicLatexSanitizer()` to normalize symbols and balance `$` / `$$` delimiters.

[STEP 2: 7-STAGE AUDIT & AUTO-REPAIR]
  ├── Execute `runConventionAuditor()` in the IDE AND `python3 audit_reference.py` in CLI
  ├── Confirm all 69 checks in `canonical_registry.json` pass (`0 failures`)
  ├── If any `SHD_CCP_AUDIT_RULES` trigger (`status: 'triggered'`), invoke `applyAuditRuleFix(rule.id)`
  └── Confirm Contrastive Remarks (`C1..C15`) grade as `CONTRASTIVE_OK`.

[STEP 3: EQUATION CLASSIFICATION & FLOWCHART SYNC]
  ├── Inspect `extractedFormulasRegistry` (verify `rtTier` 0..4 and `registryKey` bindings)
  ├── Open Flowchart Workbench (`openFlowchartStudioModal()`)
  └── Execute `syncEquationsFromCurrentPaperToFlowchart()` to attach paper equations to DAG nodes `NODE_L1_L3` .. `NODE_S6_S7`.

[STEP 4: LEAN 4 PROOF SYNTHESIS & VERIFICATION]
  ├── For each Flowchart Node, run `appendStepHaveChainToLeanEditor()` or `triggerAiLean4Synthesis()`
  ├── Export standalone Lean 4 module via `exportLean4File()` -> `GeometricLabs_<paper>.lean`
  └── Verify all theorems compile with zero `sorry` placeholders using `decide`, `ring`, `omega`, `norm_num`, `group`, and `field_simp`.

[STEP 5: COSMO-ID ATTESTATION]
  ├── Set spin state to Canonical Final: `selectCosmoSpin(1)` (`-Z (1-2k) CANONICAL FINAL`)
  └── Mint 64-bit Einstein Tile Cosmo-ID: `createVersionSnapshot('v1.0 Canonical Audited & Lean 4 Verified')`.

[STEP 6: MULTI-EXPORT & REPOSITORY COMMIT]
  ├── Export `.md` paper to `docs/papers/core/` or `docs/papers/series/` (`saveMarkdownToDisk()`)
  ├── Export `Flowchart-Lean4-Bundle-<paper>.json` and `Guided-Flowchart-Lean4-Walkthrough-<paper>.md`
  └── Run `PYTHONPATH=src python3 verification/verify_geometric_labs_suite.py` to confirm 100% test suite alignment.
```