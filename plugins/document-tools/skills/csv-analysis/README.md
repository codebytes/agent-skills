# CSV analysis presentation fixture

This resource-backed skill is a teaching adaptation, not the maintained
[codebytes/skills CSV skill](https://github.com/codebytes/skills/tree/main/skills/csv-analysis).
It shares that repository's explicit `USE FOR` / `DO NOT USE FOR` routing,
workflow/safety/exit-criteria sections, and separate trigger/capability evaluation
layers.

The deliberate demo differences are a deterministic Python profiler, explicit
encoding selection rather than a permissive fallback, and no source mutation.
The complete fixture is distributed inside `document-tools`; keep this whole
directory when installing the skill independently.

| Resource | Load or use when |
|---|---|
| `SKILL.md` | The skill is selected |
| `scripts/profile_csv.py` | Execute for local counts and numeric summaries |
| `references/methodology.md` | Explain nulls, inferred types, sampling, and outliers |
| `assets/report.md` | Format the measured report |
| `evals/csv-analysis/eval.yaml` | Run an explicitly requested Vally capability evaluation |

The package's example data and offline report live in `../../examples/`.
See the repository's [quality-check instructions](../../../../evals/README.md)
for Waza, deterministic tests, and Vally commands. The root project license is MIT.
