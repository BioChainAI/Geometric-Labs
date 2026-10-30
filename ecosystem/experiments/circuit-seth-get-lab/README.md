# Circuit-SETH GET experimental lab

[OPEN] Research scaffold based on the supplied blueprint. Compiler passes,
benchmarks, theorem guardrails and proof files are placeholders; Python module
entry points deliberately raise `NotImplementedError`. No SAT solver or Circuit-SETH
result is claimed. Numbered directories 00–05 represent specifications plus five layers.

Run the structural and source-integrity check from the repository root:

```sh
python3 ecosystem/experiments/circuit-seth-get-lab/validate_scaffold.py
```

Python 3.11+ is planned for research implementations. Optional research dependencies
are listed in `pyproject.toml`; the scaffold validator uses only the standard library.
The three uploads are preserved unchanged in `sources/`. The supplied blueprint is
also available as `circuit_seth_experimental_scaffold.md`. Its instructions describe
the proposed research workflow, not authority to execute or promote its claims.

The four planned passes are Twistor null-cone lifting, torsional pump telescoping,
orbital CRT routing, and dual-helix Ramanujan residual search. Their filenames and
responsibilities follow the blueprint. See the source blueprint for full equations,
C1–C5 obligations, experiments and obstruction I–VII definitions.

## Experimental registration

`05_proofs_and_monographs/registered_reports/preregistration_draft.md` preserves the
five hypotheses, measurements and decision rules. This is a draft copied before
implementation, not an immutable or independently timestamped preregistration.
No experiment has run. Each future run must record seed, circuit family, input size,
exact verification, preprocessing/table costs, bit growth, work and parallel depth.
Finite-size observations cannot establish an asymptotic speedup.

## Compatibility and evidence

The existing local profile defines Form 3 as IEEE-754 binary32; the blueprint
proposes a branch codec there. That proposal needs a distinct versioned profile and
golden vectors before implementation. Existing core and tile semantics are untouched.
A modular rank calculation alone does not certify rational rank or locked Boolean
variables; clause-to-sphere equivalence needs a proof. Norm preservation alone does
not bound coordinate bit width. Mixing alone does not certify SAT witnesses.

Use [OPEN], [HEURISTIC], [COMPUTED], [PROVEN], [SUPERSEDED] consistently. Normalize
blueprint [CONJECTURAL] hypotheses to [OPEN]. [COMPUTED] needs reproducible evidence;
[PROVEN] needs a reviewed mathematical proof, beyond passing tests. Theorem 5.1 and
5.14 citations remain source claims pending review. All seven automated guardrails
are planned, not implemented; `validate_scaffold.py` checks only this scaffold.

## Visual guides

The companion tutorial source is `site/circuit-seth/index.html`; the unchanged
uploaded visual explorer is `site/circuit-seth/explorer.html`. The Pages builder
publishes both under `circuit-seth/` with a homepage navigation link.
The tutorial distinguishes planned research modules from browser teaching models.
