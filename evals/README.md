# Skill quality checks

This talk follows the separation used in
[codebytes/skills](https://github.com/codebytes/skills): deterministic Waza trigger
coverage at root `evals/<name>/`, with Vally capability specs inside each skill.
The reference worktree was reviewed at commit
`94406df5cd7c1865cbf2b132e20afdfde052b6c2` on September 21, 2026.

This repository remains a compact teaching fixture. It does not duplicate that
repository's generated catalog, managed sync state, thumbnail pipeline, or
scheduled agent-evaluation infrastructure.

These optional checks target the resource-backed `csv-analysis` example only.
The introductory `release-note` skill contains just `SKILL.md`; it has no evals,
tests, scripts, or extra configuration. That is a complete skill, not an
incomplete production scaffold.

## Waza: deterministic trigger coverage

Use Waza **0.38.7**, matching the reference repository's pinned CI version.
Review the [official installation options](https://github.com/microsoft/waza#installation)
and verify the platform-specific release checksum before installing.

From this repository root:

```sh
SKILL=plugins/document-tools/skills/csv-analysis
waza spec verify --skill "$SKILL" --eval evals/csv-analysis/eval.yaml --fail
waza run evals/csv-analysis/eval.yaml --no-cache --no-summary
waza tokens count "$SKILL"
```

The suite uses `executor: mock`, `model: mock-model`, and the heuristic `trigger`
grader. Positive and negative cases cover the skill's `USE FOR` and
`DO NOT USE FOR` description. No model credentials are required.

**A passing mock trigger suite does not prove that a live model will select the
skill or calculate the correct answer.** Requirement coverage can match task
descriptions; it is not a measure of how representative your prompts are.
Token counts describe files with the tool's tokenizer, not the live context
window or the user's bill. Its warning thresholds are repository policy, not
Agent Skills specification limits.

On September 21, 2026, Waza 0.38.7 covered all **8/8 extracted requirements** and
passed **4/4 mock cases** for this fixture. Negative cases correctly have low
trigger-match scores; the aggregate score is not a model-accuracy percentage.
Re-run after changing the description or tasks rather than reusing that result.

## Deterministic calculations and fixtures

```sh
python3 -m unittest discover -s tests -v
```

These checks verify data, script errors, exact sampling boundaries, input
preservation, package metadata, and presentation assets. They do not invoke an
agent. Prefer exact assertions for counts and formulas over a model judge.

## Vally: lint first, capability runs by explicit choice

Use a pinned Vally CLI. The reference repository pins **0.14.0** in its CI
toolchain and **0.16.0** in the maintained CSV skill's development package;
these are separate pins, not one universal version.

From this repository root, with `vally` on PATH:

```sh
SKILL=plugins/document-tools/skills/csv-analysis
SPEC="$SKILL/evals/csv-analysis/eval.yaml"
vally lint --eval-spec "$SPEC" --strict

# Optional: authenticated agent and judge calls; consumes model usage.
vally eval --eval-spec "$SPEC" --skill-dir "$SKILL" \
  --work-dir . --runs 3 --workers 1 --max-retries 0
```

The real capability cases use the checked-in synthetic CSV and a missing-file
scenario. They inspect measured results, invocation, and errors. Do not run
against private data on stage. Execution and judge credentials, permissions,
model availability, and any sandboxing remain host-specific.

The prompt judge is not a security boundary or a replacement for deterministic
tests. Review the trajectory as well as the score. Model runs are opt-in; neither
the Python tests nor slide publishing automatically starts them.

## Interpreting results

Keep four questions separate:

| Question | Evidence |
|---|---|
| Is the definition well-formed? | Static lint and package checks |
| Are routing requirements covered? | Waza mock trigger suite and spec verification |
| Does the real agent perform the task? | Vally trajectories, repeated trials, measured output |
| Did a change help? | Same cases/model/settings, before/after runs, no-skill baseline where supported |

The reference repo runs inexpensive deterministic checks on PRs and uses
scheduled/manual workflows for agent-driven capability evaluations. Its Vally
workflow runs five trials with at most two workers; that is a repository choice,
not a portability requirement.

Sources: [Waza eval specifications](https://microsoft.github.io/waza/guides/eval-yaml/),
[Waza trigger grader](https://github.com/microsoft/waza/blob/main/docs/graders/trigger.md),
[Waza CLI](https://github.com/microsoft/waza#commands),
[Vally CLI](https://microsoft.github.io/vally/reference/cli/eval),
and [Anthropic skill-creator](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills).
