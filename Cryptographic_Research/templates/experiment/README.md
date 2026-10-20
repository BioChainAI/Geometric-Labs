# {{ID}}: {{TITLE}}

| | |
| :--- | :--- |
| **Stage** | experimental |
| **Status** | `[OPEN]` |
| **Version** | 0.0.1 (see [CHANGELOG](CHANGELOG.md)) |
| **Algorithm** | TODO: name, original paper, standards |
| **Upstream reference** | TODO: URL at a full 40-hex commit, plus its license (write "none declared" if there is none) |

## Question

TODO: state the single research question this item answers.

## Findings so far

| Track | Question | Result | Tag |
| :--- | :--- | :--- | :--- |
| B: baseline | Clean-room classical implementation | TODO | reference |

## Layout

Follow [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md). Docs 00–04 are the standard sections, `src/{{PACKAGE}}/` holds the code, `tests/` holds positive and negative fixtures, and `vectors/` holds deterministic golden vectors.

## Run

```sh
python3 -m unittest discover -s tests -v
```
