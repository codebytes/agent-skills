# Document Tools Demo Plugin

This compact plugin is the live example used in the "Agent Skills, Plugins &
Marketplace" talk. It starts with **a one-file skill**, then shows a skill with
resources, a portable Agent Plugins 1.0 package, thin native-host adapters, and
a checkable input/output example. Guidance was checked on **September 21, 2026**.

> This is a presentation fixture. Maintained reusable skills live in
> [codebytes/skills](https://github.com/codebytes/skills).

Walk the checked-in fixture rather than reconstructing it from abbreviated slide
snippets. The main demo validates locally before distribution; publication,
installation, and model-backed evaluations are separate explicit actions.

## Structure

```
document-tools/
├── plugin.json                 # Agent Plugins 1.0: Copilot, VS Code, Codex
├── gemini-extension.json       # Gemini's native extension adapter
├── .claude-plugin/
│   └── plugin.json             # Claude Code native adapter
├── com.github.copilot/
│   ├── agents/
│   │   └── data-analyst.agent.md
│   └── hooks/
│       └── hooks.json
├── examples/
│   ├── sample.csv
│   └── sample-report.md
└── skills/
    ├── release-note/
    │   └── SKILL.md            # Entire minimal example; nothing else needed
    └── csv-analysis/
        ├── SKILL.md            # Resource-backed example
        ├── scripts/profile_csv.py
        ├── references/methodology.md
        ├── assets/report.md
        └── evals/csv-analysis/eval.yaml  # Vally capability cases
```

## Start Small, Then Add Resources

The complete `release-note` skill is only seven lines:

```markdown
---
name: release-note
description: Write a short release note from a change summary.
---

Write two sentences: what changed, then why it matters.
Use plain language and only the facts the user supplied.
```

After loading the package in your chosen host, ask:

```text
Use release-note: users can now export search results to CSV for spreadsheet analysis.
```

There is no script, skill-local test, eval, runtime manifest, or extra configuration
inside that skill folder. The enclosing plugin is just one way to distribute it.
The plain instructions operate on text already supplied in the request.

The separate `csv-analysis` skill is the next example: it needs deterministic
calculations, supporting methodology, and a report template. Its optional Waza/
Vally examples illustrate how to evaluate a growing workflow; they are not a
requirement to create or use the minimal skill.

## Catalogs

The repository root also contains three catalog entry points:

| Host | Catalog |
|------|---------|
| Copilot CLI / VS Code | `.github/plugin/marketplace.json` |
| Claude Code | `.claude-plugin/marketplace.json` |
| Codex | `.agents/plugins/marketplace.json` |

All point to `./plugins/document-tools` **from the repository root**, not from
their manifest's directory. The Copilot and Claude catalogs have matching
content; Codex uses its documented typed `local` source. All use the marketplace
name `codebytes-agent-skills`. Gemini uses its native extension flow, not these
catalogs.

**Catalog identity changed:** Claude reserves `agent-skills`, so the catalogs
use the publisher-qualified name `codebytes-agent-skills`. The repository URL
remains `codebytes/agent-skills`, and the plugin remains `document-tools`.
Existing `document-tools@agent-skills` installations are not automatically
migrated. After publishing, register the updated catalog and use the new
selector; inspect any old installation separately before removing it.

## What Each Host Loads

| Host | Entry point | Demo capabilities |
|------|-------------|-------------------|
| Copilot CLI | Root `plugin.json` | Both skills, namespaced agent, namespaced hook |
| VS Code with Copilot | Root `plugin.json` | Both skills and supported/enabled Copilot extensions |
| Claude Code | `.claude-plugin/plugin.json` | Both skills and the explicitly referenced shared agent |
| Codex CLI / desktop | Root `plugin.json` | Both skills; not the Copilot agent or hook |
| Gemini CLI | `gemini-extension.json` | Both skills; not the Copilot/Claude agent or hook |
| Rider Skills Manager | Local source `plugins/document-tools/skills/` | Selected skills only, for supported AI Assistant agents |
| CLI in Rider's terminal | The chosen CLI's entry point above | CLI capabilities; not proof of IDE-native package support |

The root manifest's exact `$schema` selects Agent Plugins 1.0. It has no
legacy component-path fields: skills are discovered under `skills/`, and
portable MCP configuration would belong in `mcp.json`. This demo has **no MCP
or LSP server** and needs no redundant `.codex-plugin/plugin.json`.

The Claude adapter lists the shared agent's **file path in an array**.
Its `Bash`, `Read`, `Edit`, `Write`, `Grep`, and `Glob` tool names are also
documented Copilot aliases. `Skill` is included to permit Claude's native skill
invocation; tool availability in other hosts is still host-specific. This is
deliberate compatibility, not a claim that all agent definitions or tool APIs
are portable. If no skill tool is available, the profile reads the canonical
file and explicitly distinguishes instruction reuse from native invocation.

The Copilot `SubagentStart` hook emits a local-data-handling reminder as JSON.
It includes the CLI's `additionalContext` field and VS Code's
`hookSpecificOutput` envelope. It does not grant permissions, write files,
contact a server, or prove that the CSV skill activated. It can run for other
subagents too. Claude, Codex, and Gemini are not configured to load this hook.

The **Codex IDE extension** is not the same surface as Codex CLI/desktop:
current OpenAI documentation says that extension does not support plugins.
OpenAI API skill and plugin loading is separate from the local workflows below.

## Rehearsal Setup

Run these commands from the **repository root**, with the relevant host CLI
installed. The skill's calculations require Python 3 and only standard-library
modules. Installation may require host trust/approval; inspect the source first.
No install command here submits the package to a public plugin directory.

Remote installs see the last published commit, not uncommitted local changes.
Use the local paths for rehearsing edits. Do not register both local and remote
catalogs under the same name and assume they are interchangeable.

### Verify Locally Before Publishing

After reviewing the code, run the deterministic profiler from the repository
root:

```bash
SKILL=plugins/document-tools/skills/csv-analysis
python3 "$SKILL/scripts/profile_csv.py" \
  plugins/document-tools/examples/sample.csv --delimiter ,
python3 -m unittest discover -s tests -v
```

The script uses only Python's standard library. It returns aggregate JSON, not
the input rows, and it does not write files or contact a server. Read the linked
methodology for missing markers, sample standard deviation, type inference,
and the exact 100 MiB sampling boundary. The report template loads separately
when formatting; ordinary links do not automatically inject target contents.

Next use the session-only preview below, inspect invocation, and compare the
actual result. Static checks and a correct profiler do not prove model routing.
Keep the expected report as an honestly labeled offline fallback.

### Copilot CLI

For a session-only local preview:

```bash
PLUGIN="$PWD/plugins/document-tools"
copilot --plugin-dir "$PLUGIN" plugin list
copilot --plugin-dir "$PLUGIN" skill list
copilot --plugin-dir "$PLUGIN"
```

The first two commands verify the mount without starting a model conversation.
The last starts the interactive preview. Each new process needs `--plugin-dir`;
a plain `copilot skill list` in another terminal does not inherit that mount.

Inside the preview, open `/skills` and inspect the **exact listed name**.
Same-name skills can be namespaced rather than appearing under the bare name.
On the verified Copilot CLI 1.0.87-0 setup, an installed Codebytes collection
causes these distinct entries:

- `document-tools:csv-analysis` - this local demo.
- `codebytes-skills:csv-analysis` - the separately installed collection.
- `release-note` - this demo's unique one-file skill.

In that setup use `/skills info document-tools:csv-analysis` and
`/skills info release-note`. In a clean setup, use whatever identifier `/skills`
shows instead. Check that each source path points into the intended
`plugins/document-tools/skills/` directory. `/agent` inspects the optional agent.

If discovery still differs, confirm `copilot --version`, that `copilot --help`
documents `--plugin-dir`, and that the terminal is in the edited checkout.
The plugin listing should show `document-tools` version `1.3.0` as enabled and
external; `skill list --json` provides source paths. No global install is needed.

For a marketplace installation:

```bash
copilot plugin marketplace add .
copilot plugin marketplace browse codebytes-agent-skills
copilot plugin install document-tools@codebytes-agent-skills
copilot plugin list
copilot skill list
```

After publishing, replace `.` with `codebytes/agent-skills` to register the
remote catalog. To update a Git-backed installation:

```bash
copilot plugin marketplace update codebytes-agent-skills
copilot plugin update document-tools@codebytes-agent-skills
```

Catalog refresh and installed-plugin update are distinct. Prefer this
marketplace workflow over relying on direct-install behavior across versions.

### VS Code

Register the local **plugin root** in settings, substituting its actual
absolute path:

```json
{
  "chat.plugins.enabled": true,
  "chat.pluginLocations": {
    "/absolute/path/agent-skills/plugins/document-tools": true
  }
}
```

For the published catalog:

```json
{
  "chat.plugins.marketplaces": ["codebytes/agent-skills"]
}
```

Browse **Extensions → `@agentPlugins`**, or **Chat: Open Customizations →
Plugins**, and review the marketplace trust prompt. Plugin support is not
blanket preview-only; individual capabilities such as hooks can still be
preview features or disabled by policy. Current VS Code also supports
workspace plugin recommendations and discovers Copilot CLI-installed plugins.

### Claude Code CLI

Validate and load the local plugin for one session:

```bash
claude plugin validate --strict ./plugins/document-tools
claude --plugin-dir ./plugins/document-tools
```

Explicitly invoke `/document-tools:csv-analysis` in the session. For a catalog
installation:

```bash
claude plugin marketplace add .
claude plugin install document-tools@codebytes-agent-skills
```

Use `codebytes/agent-skills` instead of `.` for a published catalog. The
marketplace adapter is `.claude-plugin/marketplace.json`; the Copilot-only
catalog path is not the Claude discovery contract.

The two-command flow is intentional: the combined
`/plugin install <plugin> --marketplace <source>` shortcut arrived in Claude
Code 2.1.275, newer than the 2.1.240 validator used for this fixture. Version
2.1.275 also introduced account skill/plugin sync into signed-in terminal
sessions. Inspect the active source rather than assuming a same-name component
came from this local plugin.

This section is specifically for the **`claude` CLI**, not claude.ai or Cowork.
It also applies when that CLI runs in Rider's integrated terminal from the same
project root. The JetBrains Claude Code bridge, when installed and compatible,
uses the existing CLI executable on the IDE's PATH; check `claude --version`
in that terminal rather than assuming it matches another shell.

### Codex CLI

```bash
codex plugin marketplace add .
codex plugin list --marketplace codebytes-agent-skills --available --json
codex plugin add document-tools@codebytes-agent-skills
codex
```

In the new session, inspect `/plugins` and `/skills`, then explicitly request
`$csv-analysis`. Codex reads the portable skill; it does not turn the shared
Markdown profile into a Codex custom agent.

For a published Git-backed catalog, register `codebytes/agent-skills` instead
of `.`. The CLI also supports `--ref` when adding Git marketplaces. Updates use:

```bash
codex plugin marketplace upgrade codebytes-agent-skills
codex plugin add document-tools@codebytes-agent-skills
```

`marketplace upgrade` refreshes Git snapshots. For local source changes,
reinstall with `codex plugin add`; do not assume the installed copy follows
every source edit. A package `version` is not a Git revision pin.

### Gemini CLI

Confirm current Gemini CLI account/API access before rehearsing. Google's
May 2026 announcement changed consumer access from June 18 while preserving
specified enterprise subscriptions and paid API-key access. Do not assume the
older free consumer sign-in flow, or confuse Gemini CLI with Antigravity CLI.

Validate, then link the native extension for local development:

```bash
gemini extensions validate ./plugins/document-tools
gemini extensions link ./plugins/document-tools
gemini extensions list
gemini skills list
```

Linking registers the extension in the user's Gemini configuration; it is not
a session-only flag. Source changes remain in the repository. Restart
Gemini and inspect available skills before the demo. Request
`csv-analysis` explicitly and follow the host's activation/trust prompts.

The extension uses default `skills/` discovery. The portable manifest and
Copilot namespace do not replace Gemini's native extension manifest. Do not
use Copilot's `owner/repo:subdirectory` syntax with Gemini. Native Agent Plugins
1.0 loading in Gemini CLI is not confirmed by the official host docs checked
here; Google's standards participation is not evidence of that implementation.

For **public skill-only installation**, use the documented subdirectory option
after publishing the repository changes:

```bash
gemini skills install https://github.com/codebytes/agent-skills.git \
  --path plugins/document-tools/skills/csv-analysis \
  --scope user
gemini skills list
```

Choose this **or** the local extension route for a rehearsal. Workspace and user
skills override extension-bundled skills of the same name; installing both can
hide which copy ran. Within a workspace/user scope, `.agents/skills/` takes
precedence over `.gemini/skills/`.

The nested extension adapter does not qualify this repository for direct
whole-repo extension installation or the Gemini gallery. Those distribution
routes require the extension manifest at the repository/release-archive root.
Do not invent an extension-install `--path` flag; the option above belongs to
**skills install**. Gemini-specific subagents and hooks could be added in their
native layouts, but are intentionally not part of this adapter.

### JetBrains Rider

First identify the entry point and its version. Rider's AI Assistant, the
separate GitHub Copilot plugin, and CLI sessions in its terminal do not
necessarily load the same configuration.

**AI Assistant Skills Manager** (documented in Rider 2026.2):

1. Open **Settings/Preferences → Tools → AI Assistant → Skills**.
2. Choose **Skills Settings → Manage Skill Directories**.
3. Add the absolute path to this repository's
   `plugins/document-tools/skills/` as a local source.
4. Select `csv-analysis` and install it for the intended scope. IDE scope
   avoids adding a generated copy to this source repository; generic Project
   scope uses `.agents/skills/`.
5. Select a supported agent, inspect the skill's enabled state/source, and use
   **Try in chat**. Then run the sample-data prompt and compare its measured
   results.

The current AI Assistant agent matrix documents Skills Manager support for
Claude Agent and Codex; do not assume every entry in the ACP Registry has the
same integration. A managed Claude Agent chat is not simply the installed
Claude Code CLI with every CLI plugin option forwarded.

**Optional CLI staging into a separate Rider project**, from this repository:

```bash
gh skill install ./plugins/document-tools csv-analysis --from-local \
  --dir /path/to/your-rider-project/.agents/skills
```

Replace the destination with the actual project path. GitHub CLI copies the
skill and adds provenance metadata; it does not install the enclosing plugin,
agent, or hook. Continue authoring only the canonical plugin-local skill,
not the generated installation copy. This staging step is not a Rider runtime
activation test. The bundled sample paths below assume Rider opened this talk
repository; in another project, supply the actual accessible path to the CSV.

**GitHub Copilot's JetBrains plugin:** open its chat **Customizations** UI to
inspect the discovered skill and the selected local/CLI harness. GitHub
announced agent skills GA for this integration on June 2, 2026. When using
Copilot CLI in Rider's terminal, use the Copilot CLI package instructions above
instead of inventing Rider-specific `plugin.json` settings.

**Claude Code CLI in Rider:** run the established CLI workflow from Rider's
terminal at the project root, for example
`claude --plugin-dir ./plugins/document-tools`, then invoke
`/document-tools:csv-analysis`. IDE bridge installation is separate and is not
performed by this repository's validation commands.

Do not paste `chat.pluginLocations` or `chat.plugins.marketplaces` into Rider:
they are VS Code settings. The ACP Registry, Skills Manager's skill sources,
JetBrains Marketplace, and the demo's plugin catalogs serve different purposes.
Follow the installed agent's invocation UI instead of assuming every CLI slash
command works in every IDE chat.

## Check the Result

Use this prompt in the chosen host, applying its explicit skill-invocation
syntax where available:

```text
Use the csv-analysis skill from document-tools to profile
plugins/document-tools/examples/sample.csv.
Return a Markdown report. Do not modify or upload the input.
```

For Copilot, substitute the exact skill identifier from `/skills`, for example
`document-tools:csv-analysis` when a same-name installed skill causes namespacing.

Compare measured facts with [sample-report.md](examples/sample-report.md):

- 10 data rows, 5 columns, and no duplicate rows.
- One missing salary and one missing start date: **48/50 cells = 96% complete**.
- Numeric statistics exclude missing values and use **sample** standard deviation.
- Sampling, encoding, and calculation failures must be reported, not hidden.
- Currency, comparative age claims, and tenure require additional metadata;
  the reference report does not infer them from column names or old dates.

Installation, enabled state, and invocation are separate checks. An agent may
not automatically choose the skill, and same-name local skills or policy can
change what loads. Keep the expected report as a live-demo fallback rather
than claiming an unobserved model run succeeded.

## Quality Layers

The resource-backed CSV example aligns with `codebytes/skills` without
duplicating its managed distribution repository. These quality tools are
optional, and the minimal `release-note` skill intentionally has none of this
scaffolding:

| Layer | Location | What it establishes |
|---|---|---|
| Deterministic checks | Root `tests/` | Counts, scripts, errors, input preservation, package coherence |
| Waza mock trigger suite | Root `evals/csv-analysis/` | Heuristic positive/negative routing coverage |
| Vally capability spec | Skill-local `evals/csv-analysis/` | Opt-in agent execution, invocation, and rubric evidence |

See [quality setup and commands](../../evals/README.md). A mock trigger pass is
not a real model selection result; Vally's prompt judge is not a sandbox or a
substitute for exact formula checks. The slide examples name which layer ran.
Review tool versions and obtain approval before starting agent/judge calls.

## Validation

From the repository root:

```bash
python3 -m unittest discover -s tests -v
claude plugin validate --strict ./plugins/document-tools
claude plugin validate --strict .claude-plugin/marketplace.json
gemini extensions validate ./plugins/document-tools
```

The Python checks need Python 3.9 or later; host validators require their
respective CLIs. These checks do not exercise model routing, every OS, or every
host's runtime permissions. In Rider, also record the IDE version, integration,
agent/harness, scope, and skill source, then verify actual invocation and output.
Do not install or enable the demo globally as an incidental test.

See the [repository compatibility baseline and official sources](../../README.md#compatibility-baseline)
for the current standards, host caveats, and dated announcements.
