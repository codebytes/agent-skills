# Agent Skills, Plugins & Marketplace

This repository is the source for Chris Ayers' talk "Agent Skills, Plugins &
Marketplace."

## Slides

The slides for the talk can be found at:\
[https://chris-ayers.com/agent-skills/](https://chris-ayers.com/agent-skills/)

The main story first defines an agent skill and when a task is worth turning into
one. The context-window explanation comes before instruction, skill, and agent
loading. It compares GitHub Copilot and Claude Code, including shared `AGENTS.md`
guidance, then introduces a one-file `release-note` skill before the resource-backed
CSV example. Waza/Vally quality checks are an optional next step, not prerequisites
for the minimal skill. One package proceeds through verification and distribution.
The main story closes with **Questions?**, followed by the presenter's contact
slide before the reference appendix.
The authoring section makes the skill naming contract visible, including the
1–64 character limit, lowercase Unicode alphanumerics/hyphens, edge and repeated
hyphen restrictions, and matching the parent directory.
The reference appendix preserves host-specific paths, adapters, IDE procedures,
version pinning, and primary sources without interrupting the main narrative.
The plugin section explicitly shows one plugin configuring multiple MCP servers;
an appendix example uses placeholder endpoints, not live demo services. MCP
server processes do not automatically provide separate model context windows.

## What's Here

- `slides/Slides.md` - the Marp presentation source
- `slides/themes/custom-default.css` - the talk's custom Marp theme
- `slides/img/` - presentation images, editable `.drawio.svg` diagrams, and their JSON specifications
- `plugins/document-tools/` - the compact, cross-host presentation fixture
- `plugins/document-tools/skills/release-note/SKILL.md` - the entire minimal skill, with no supporting scaffold
- `plugins/document-tools/skills/csv-analysis/` - the example with a script, reference, and template
- `plugins/document-tools/plugin.json` - the Agent Plugins 1.0 manifest
- `plugins/document-tools/com.github.copilot/` - Copilot-specific agent and hook
- `.github/plugin/marketplace.json` - the minimal marketplace shown in the talk
- `.claude-plugin/marketplace.json` - the equivalent Claude catalog
- `.agents/plugins/marketplace.json` - Codex's native catalog for the same package
- `tests/test_demo.py` - dependency-free fixture and documentation checks
- `tests/test_profile_csv.py` - deterministic profiler, error-handling, and sampling checks
- `evals/csv-analysis/` - Waza deterministic trigger coverage
- `plugins/document-tools/skills/csv-analysis/evals/` - opt-in Vally capability cases

The demo keeps one canonical source for each of its two skills:

| Example | Contents | Purpose |
|---|---|---|
| `release-note` | Just `SKILL.md` | Show the minimum useful skill; no scripts, tests, evals, or extra configuration |
| `csv-analysis` | Instructions, a Python profiler, a linked methodology reference, and a report template | Show when supporting resources become useful |

These are teaching fixtures, not the maintained distribution source. The optional
quality examples apply to `csv-analysis`; they are deliberately absent from the
minimal skill folder.

## Alignment with Codebytes Skills

The resource-backed CSV fixture follows the maintained [codebytes/skills](https://github.com/codebytes/skills)
repository's explicit `USE FOR` / `DO NOT USE FOR` descriptions, workflow/safety/
exit-criteria sections, and separate quality layers:

- Waza mock/heuristic trigger suites at root `evals/<name>/`.
- Agent-driven Vally capability specs inside the skill at `evals/<name>/`.
- Deterministic tests for scripts, fixtures, and distribution invariants.

The reference worktree was reviewed read-only at commit
`94406df5cd7c1865cbf2b132e20afdfde052b6c2` on September 21, 2026, including its
local quality-documentation changes. This talk is not a second managed copy of
that collection: it has a nested plugin fixture rather than a root `skills/`
distribution. Its explicit-encoding, immutable-input profiler is a deliberate
teaching adaptation, not a claim about the maintained CSV skill's implementation.
The collection's generated manifests, thumbnails, and sync lifecycle remain in
their own repository.

The minimal `release-note` example intentionally omits that production-oriented
scaffolding: the portable format requires only its `SKILL.md`.

See [quality checks and tool boundaries](evals/README.md). Passing mock routing
checks does not prove actual model selection, and a prompt-judge score does not
replace exact arithmetic checks or enforce a security boundary.

## Compatibility Baseline

**Official guidance checked on September 21, 2026.** Configuration and
availability depend on the client, version, execution environment, and policy,
not just the model provider.

The hands-on workflows explicitly cover **Claude Code CLI**, Copilot CLI,
Codex CLI, and Gemini CLI. Claude/Cowork, web, API, and IDE integrations are
separate surfaces, not substitutes for validating those command-line tools.

Two standards have different responsibilities:

| Standard | Defines | Does not define |
|----------|---------|-----------------|
| [Agent Skills](https://agentskills.io/specification) | `SKILL.md`, metadata, instructions, supporting resources | A universal discovery path, tool API, or activation policy |
| [Agent Plugins 1.0](https://agent-plugins.org/specification) | Root `plugin.json`, `skills/`, `mcp.json`, extension namespaces | Marketplace schemas, install commands, permissions, or portable custom agents/hooks |

The fixture deliberately uses different host entry points:

| Host | Package entry point used here | Important boundary |
|------|-------------------------------|--------------------|
| Copilot CLI / VS Code with Copilot | Root `plugin.json` and `com.github.copilot/` | Native capabilities still depend on the client and policy. |
| Claude Code | `.claude-plugin/plugin.json` | Native adapter retained; standard-loader adoption is unverified. |
| Codex CLI / desktop | Root `plugin.json` | Reuses the skill, not the Copilot agent/hook; has its own catalog. |
| Gemini CLI | `gemini-extension.json`, or direct skill installation | Native Agent Plugins 1.0 loading is unverified; the nested extension is a local-path demo. |
| JetBrains Rider | Skills Manager/local skill source, or the selected CLI | AI Assistant, the GitHub Copilot plugin, and a CLI in Rider's terminal are different entry points. |

For a new portable plugin, the demo follows the current guidance:

1. Declare the exact Agent Plugins 1.0 `$schema` in a **root** `plugin.json`.
   Do not add legacy `agents`, `skills`, `hooks`, or `mcpServers` path fields.
2. Keep skills in immediate children of `skills/`. This demo has `release-note`
   and `csv-analysis`; each directory matches its `SKILL.md` frontmatter name.
3. Put Copilot-specific components under `com.github.copilot/`. Other clients
   do not automatically load those capabilities.
4. Add only the native adapters the target host needs. The Claude manifest
   uses an array of explicit agent file paths, not an agent-directory string.
5. Review executable components before installation. A package's path
   containment rules are **not a subprocess sandbox**.

Adding `$schema` to an old manifest without moving its components is not a
complete migration. Existing native/legacy plugins remain supported by their
hosts; adopting the portable format does not make every feature portable.

### Shared Instructions Are Not Agent Profiles

`AGENTS.md` is project guidance, not a `*.agent.md` custom-agent definition.
[Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)
and [Copilot in VS Code](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
support it alongside their other instruction sources.

[Claude Code 2.1.277+](https://code.claude.com/docs/en/memory#agents-md) supports
native `AGENTS.md` loading in supported sessions. Its default uses `AGENTS.md`
only when no project/ancestor `CLAUDE.md` or `CLAUDE.local.md` is present. The
Project instructions setting can select both; an explicit `@AGENTS.md` import
from `CLAUDE.md` is another route and remains useful where native support is
unavailable. Do not assume identical discovery or merging across hosts.

Applicable instructions become model context without a skill invocation. The
host need not reread every file for every call; retained content and prompt
caching are different from selection. Scope rules keep unrelated guidance out.

The catalogs now use **`codebytes-agent-skills`**, because Claude reserves
`agent-skills` as a marketplace name. The repository remains
`codebytes/agent-skills`. See the demo's
[catalog identity migration note](plugins/document-tools/README.md#catalogs)
before replacing an existing installation.

### Relevant Announcements

| Date | Official source | Effect on this talk |
|------|-----------------|---------------------|
| 2026-02-10 | [OpenAI API changelog: Responses API Skills](https://developers.openai.com/api/docs/changelog) | Uploaded/versioned API skills are a separate delivery mechanism from local Codex marketplaces. |
| 2026-02-24 | [Anthropic: Cowork plugins across the enterprise](https://claude.com/blog/cowork-plugins-across-enterprise) | Cowork organization marketplaces and provisioning are not the same surface as Claude Code's terminal install flow. |
| 2026-03-03 | [Anthropic: improving skill-creator](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills) | Evaluate triggering separately from output quality; a valid package alone proves neither. |
| 2026-03-25 | [OpenAI: Codex plugins](https://developers.openai.com/codex/changelog/#codex-2026-03-25) | Codex has plugins and marketplaces, not only standalone skill installers. |
| 2026-04-16 | [GitHub: manage agent skills with `gh skill`](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/) | A skill installer can target different hosts; it is not a plugin marketplace format. |
| 2026-05-19 | [Google: Gemini CLI consumer transition](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/) | Consumer access changed June 18; do not promise the old free consumer sign-in flow. |
| 2026-06-02 | [GitHub: Copilot CLI and agentic improvements in JetBrains IDEs](https://github.blog/changelog/2026-06-02-introducing-copilot-cli-and-agentic-capabilities-enhancements-in-jetbrains-ides/) | Agent skills are GA in the Copilot plugin; select the actual local/CLI harness instead of assuming VS Code parity. |
| 2026-07-22 | [JetBrains: Rider 2026.2](https://blog.jetbrains.com/dotnet/2026/07/22/rider-2026-2-release/) | Rider exposes Skills Manager and integrated agents; skill registries and agent registries are not plugin marketplaces. |
| 2026-08-06 | [Google: Agent Plugins](https://developers.googleblog.com/agent-plugins-package-your-skills-tools-and-more/) | Google participation is confirmed; the named shipping products are Agents CLI and Data Agent Kit, not proof of a Gemini CLI loader. |
| 2026-08-12 | [GitHub: Agent Plugins 1.0 is GA](https://github.blog/changelog/2026-08-12-agent-plugins-1-0-in-vs-code-copilot-cli-and-the-copilot-app/) | Use the portable package format published August 6, with namespaced client extensions. |
| 2026-08-12 | [VS Code 1.133](https://code.visualstudio.com/updates/v1_133) | Portable plugin support is available; individual capabilities have their own release status. |
| 2026-09-03 | [Codex CLI 0.153.0](https://github.com/openai/codex/releases/tag/rust-v0.153.0) | Remote-marketplace listing, installation, and removal are part of the CLI. |
| 2026-09-09 | [Codex CLI 0.154.0](https://github.com/openai/codex/releases/tag/rust-v0.154.0) | Live refresh improved; still rehearse updates and invocation on the actual presentation client. |
| 2026-09-10 | [OpenAI API changelog: Agents API public beta](https://developers.openai.com/api/docs/changelog) | Managed Codex environments load plugin capabilities through API-specific configuration. |
| 2026-09-15 | [Gemini CLI stable v0.60.0](https://github.com/google-gemini/gemini-cli/releases/tag/v0.60.0) | Extension environment-change consent and loader hardening reinforce the need to rehearse trust behavior. |
| 2026-09-16 | [VS Code 1.138](https://code.visualstudio.com/updates/v1_138) | New Dev Container and Codex-harness capabilities are surface-specific, not proof that all plugins work everywhere. |
| 2026-09-17 | [Claude Code 2.1.275](https://github.com/anthropics/claude-code/releases/tag/v2.1.275) | Account skill/plugin sync and a combined marketplace-install shortcut are new; keep the established two-step demo compatible with older clients. |
| 2026-09-18 | [Claude Code 2.1.277](https://github.com/anthropics/claude-code/releases/tag/v2.1.277) | Recent fixes affect plugin reinstallation, marketplace policy, and installed commit tracking. |
| 2026-09-18 | [Codex CLI 0.155.1](https://github.com/openai/codex/releases/tag/rust-v0.155.1) | Released implementation baseline used to confirm portable-manifest support. |

Package support, workspace configuration, and approval behavior must be checked
for the named client rather than inferred from the model provider.

### Claude Code CLI: Native Adapter and Reserved Catalog Names

Claude's documented entry points remain
`.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.
Native Agent Plugins 1.0 adoption was not confirmed by the official Claude
guidance checked here, so the adapter remains intentional.

The explicit `agents` path points to a Markdown **file**, not a directory.
Its `.agent.md` suffix satisfies the published `.md` path rule, and the local
Claude validator accepts it. Tool names and runtime behavior are still
host-specific. The shared profile includes Claude's `Skill` tool; without it,
its explicit allowlist would prevent native skill invocation. Reading the
canonical file instead is instruction reuse, not proof that the skill activated.

The [Claude marketplace schema](https://code.claude.com/docs/en/plugin-marketplaces#marketplace-schema)
reserves `agent-skills`. All three demo catalogs therefore use the consistent
publisher-qualified name `codebytes-agent-skills`; the repository slug is
unchanged. Schema acceptance in an older CLI is not sufficient evidence that a
catalog name follows current distribution guidance.

Keep portable `name` and `description` metadata even though Claude Code's own
skill loader is more permissive. Claude Code-specific frontmatter and runtime
features are not automatically valid in claude.ai uploads or the Skills API.
Plugin installation is also not a sandbox, and `allowed-tools` is not a
read-only restriction.

### OpenAI Is Not One Installation Surface

Current [OpenAI plugin guidance](https://developers.openai.com/plugins/build/plugins)
recommends the same portable root manifest used by this demo. The
`.codex-plugin/plugin.json` compatibility format remains supported, but adding
one here would be redundant. The Copilot agent and hook are not advertised as
Codex capabilities.

The [current plugin availability documentation](https://learn.chatgpt.com/docs/plugins)
says the **Codex IDE extension does not support plugins**; this supersedes the
broader wording in the March launch announcement. CLI, desktop, ChatGPT
platform/workspace capabilities, and the newer VS Code agent-host harness
must not be treated as identical surfaces.

Local catalogs, workspace GitHub imports, and the OpenAI public plugin
directory have different admission and publication flows. Adding this
repository's catalog does not publish it to the public directory. Likewise,
[Responses API Skills](https://developers.openai.com/api/docs/guides/tools-skills)
and [Agents API plugins](https://developers.openai.com/api/docs/guides/agents-api/tools/plugins)
use their own uploaded resources and environment configuration, not these
local install commands. `agents/openai.yaml`, when used, is per-skill metadata
and policy, not a portable custom-agent definition.

### Gemini: Native Extensions, Explicit Distribution

The [Gemini extension reference](https://geminicli.com/docs/extensions/reference.md)
documents `gemini-extension.json` and default `skills/` discovery. The
two-field adapter in this fixture uses that native mechanism, not an invented
Gemini namespace in the portable manifest.

Google's Agent Plugins participation does **not** establish native Gemini CLI
package loading. The official documentation checked here does not confirm that
loader; this is an **unverified capability**, not a claim that it is impossible.
Agents CLI, Antigravity CLI, and Gemini CLI are distinct products.

The [official extension gallery](https://geminicli.com/extensions/) is a
discovery surface, not a verified consumer of Copilot/Claude marketplace JSON.
[Gallery publication](https://geminicli.com/docs/extensions/releasing.md)
expects `gemini-extension.json` at the repository or release-archive root.
Our nested adapter supports local linking; it does not make the whole talk
repository directly installable as a Gemini extension. For remote use, the
demo instructions use the documented `gemini skills install --path` route.

The May 19 transition announcement preserved specified enterprise subscriptions
and paid API-key access while moving consumer usage to Antigravity CLI from
June 18. Confirm the presenter's current eligibility before a live Gemini demo.
Installation consent, skill-activation consent, workspace trust, and tool
permissions are separate checks; do not bypass them in the example.

### JetBrains Rider: Choose the Entry Point First

[Rider 2026.2](https://blog.jetbrains.com/dotnet/2026/07/22/rider-2026-2-release/)
documents **Settings/Preferences → Tools → AI Assistant → Skills**.
The [Skills Manager](https://www.jetbrains.com/help/ai-assistant/agent-skills.html)
can register a local source directory, including this demo's
`plugins/document-tools/skills/`, then install a selected skill at IDE or
project scope. Generic project installs use `.agents/skills/`.

That is not the same integration as either of these:

- **Claude Code CLI or Copilot CLI in Rider's terminal:** use the corresponding
  CLI workflow from the project root. Anthropic's optional JetBrains bridge
  launches an existing `claude` command; it does not bundle the CLI.
- **GitHub Copilot's JetBrains plugin:** has its own chat/customizations UI and
  multiple agent harnesses. GitHub documents skill support, but the active
  harness and version still determine packaged-plugin behavior.

The [AI Assistant agent matrix](https://www.jetbrains.com/help/ai-assistant/agents.html)
currently documents Skills Manager support for **Claude Agent and Codex**.
Do not extend that statement to every ACP agent. Junie has its own
[skill documentation](https://junie.jetbrains.com/docs/agent-skills.html), and
the separate Copilot plugin has its own capabilities. Likewise, the OpenAI
Codex IDE extension and JetBrains' managed Codex agent are not interchangeable.

The **ACP Registry** discovers agent integrations; **skill repositories**
distribute skills; **JetBrains Marketplace** distributes IDE plugins.
None of those names establishes universal Agent Plugins 1.0 marketplace
compatibility. VS Code settings such as `chat.pluginLocations` do not configure
Rider.

Use the [Rider rehearsal instructions](plugins/document-tools/README.md#jetbrains-rider)
to check the selected agent, scope, skill source, and actual invocation in the
installed IDE. File validation and installer staging do not prove that Rider's
UI loaded a skill or that an agent ran it.

## Rehearse the Demo

Follow the [demo setup and host-specific instructions](plugins/document-tools/README.md).
Rehearse the exact client and version used on stage, and explicitly request
`csv-analysis` rather than relying only on automatic routing.

The supplied CSV has **10 rows, 5 columns, 2 missing cells, and 96% completeness**.
Check those facts and the calculation conventions against the
[expected report](plugins/document-tools/examples/sample-report.md).
Keep that report available as the fallback for network or live-model failures.
The demo does not require publishing a new commit during the presentation.
Review the source, run the local profiler, preview with
`copilot --plugin-dir ./plugins/document-tools`, and verify the result **before**
publishing. After installation, verify discovery, invocation, output, and input
integrity again. Local preview and remote installation exercise different paths.
Preflight discovery with `copilot --plugin-dir "$PWD/plugins/document-tools" skill list`.
The flag applies to that process, not to future bare listing commands. Inside the
preview, use `/skills` and its exact identifier: when the maintained collection
is also installed, the demo can be listed as `document-tools:csv-analysis`, not
bare `csv-analysis`. See the [Copilot rehearsal instructions](plugins/document-tools/README.md#copilot-cli).

### Local Checks

With Python 3.9 or later:

```bash
python3 -m unittest discover -s tests -v
```

These checks cover fixture consistency, profiler behavior, and examples, not an
end-to-end model run. Use the host's own validator and a manual activation/output
check as well.
For example, with Claude Code installed:

```bash
claude plugin validate --strict plugins/document-tools
```

See [evals/README.md](evals/README.md) for pinned Waza setup, deterministic trigger
checks, Vally lint, and optional authenticated capability evaluations. Do not
run billed or agent-driven evaluations as an incidental static check.

### Render and Edit the Presentation

The `custom-default` theme uses the existing blue, white, and navy identity with
a dark cover and section dividers, open comparison columns, readable dark code
panels, consistent tables, and visible source footers. Slide-local classes
select the cover, bio, agenda, concept, diagram, workflow, and closing layouts;
styling does not require a new font dependency. Keep factual content and
speaker notes separate from these presentation directives.

Use Marp CLI **v4**, explicitly loading the custom theme and trusted local assets:

```sh
npx @marp-team/marp-cli@4 slides/Slides.md \
  --theme-set slides/themes --html --allow-local-files -o /tmp/agent-skills.html
npx @marp-team/marp-cli@4 slides/Slides.md \
  --theme-set slides/themes --html --allow-local-files --pdf -o /tmp/agent-skills.pdf
```

Inspect every rendered slide at presentation size, including code, reference
footers, and diagram labels. A successful render or a word-count check alone
does not prove there is no clipping.

All current diagrams are static, editable `.drawio.svg` files with an embedded
draw.io model and a matching `*.spec.json` source. They do not require runtime
Mermaid or a CDN to draw the image. Open the SVG in Draw.io Integration or
diagrams.net. When editing JSON, regenerate both the rendered image and embedded
model with the maintained
[drawio-diagrams helper](https://github.com/codebytes/skills/tree/main/skills/drawio-diagrams).
For example, with `DRAWIO_SKILL` pointing to that skill directory:

```sh
node "$DRAWIO_SKILL/scripts/make-drawio-svg.mjs" build \
  slides/img/context-window-budget.spec.json \
  -o slides/img/context-window-budget.drawio.svg
node "$DRAWIO_SKILL/scripts/validate-drawio.mjs" \
  slides/img/context-window-budget.drawio.svg
```

Keep JSON and SVG synchronized; do not edit only the visible SVG text.
The older detailed `create-to-consume-flow.drawio.png` is retained as a historical
reference, not used as a projected diagram.

### Publishing

Publishing requires a separately approved push/merge. The Pages workflow builds
HTML and PDF from `main`; a local render or feature-branch edit does not update
the public presentation. After an approved merge, check the workflow result,
open the published deck and PDF, and confirm the context, quality-tool slides,
and `.drawio.svg` assets match the reviewed revision. Remote plugin installs
likewise see only the published revision and require repository access.

## Reusable Skills

The maintained, cross-agent skills marketplace now lives in
[codebytes/skills](https://github.com/codebytes/skills). Browse the published
catalog at [https://chris-ayers.com/skills/](https://chris-ayers.com/skills/).

## Talk Topics

- Understanding **Agent Skills** and the `SKILL.md` format
- Distinguishing always-on policy, conditional instructions, and on-demand skill resources
- Managing context with progressive disclosure, targeted tool output, and bounded delegation
- Separating Waza routing checks, deterministic correctness, and Vally capability evidence
- Building **Agent Plugins 1.0** packages with host-specific extensions
- Publishing through a host's **marketplace** or native distribution mechanism
- Separating portable skills from discovery, tools, permissions, and adapters
- Verifying activation and output, not just successful installation

## Resources

- [VS Code Instruction Types](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
- [Claude Context Management](https://code.claude.com/docs/en/how-claude-code-works)
- [Prompt Caching and Billing](https://code.claude.com/docs/en/prompt-caching)
- [Agent Skills Execution and Progressive Disclosure](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Waza](https://github.com/microsoft/waza) and [evaluation specifications](https://microsoft.github.io/waza/guides/eval-yaml/)
- [Vally CLI](https://microsoft.github.io/vally/reference/cli/eval)
- [Anthropic Skill-Creator Evals](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)
- [Codebytes Quality Workflow](https://github.com/codebytes/skills#skill-quality)
- [Agent Plugins Specification](https://agent-plugins.org/specification)
- [GitHub Docs: About Plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
- [Copilot CLI Plugin Reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
- [VS Code Agent Plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins)
- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [Claude Plugin Reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude Marketplace Reference](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude Skills](https://code.claude.com/docs/en/skills)
- [Claude Subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code JetBrains Integration](https://code.claude.com/docs/en/jetbrains)
- [OpenAI Plugin Authoring](https://developers.openai.com/plugins/build/plugins)
- [OpenAI Plugin Availability](https://learn.chatgpt.com/docs/plugins)
- [OpenAI Skill Authoring](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI Plugin Submission](https://developers.openai.com/plugins/deploy/submission)
- [Gemini CLI Skills](https://geminicli.com/docs/cli/skills.md)
- [Gemini CLI Extension Reference](https://geminicli.com/docs/extensions/reference.md)
- [Gemini CLI Extension Publishing](https://geminicli.com/docs/extensions/releasing.md)
- [Gemini CLI Subagents](https://geminicli.com/docs/core/subagents.md)
- [Rider 2026.2 Agent Skills](https://blog.jetbrains.com/dotnet/2026/07/22/rider-2026-2-release/)
- [JetBrains Skills Manager](https://www.jetbrains.com/help/ai-assistant/agent-skills.html)
- [JetBrains AI Assistant Agent Matrix](https://www.jetbrains.com/help/ai-assistant/agents.html)
- [GitHub Copilot Entry Points in JetBrains IDEs](https://docs.github.com/en/copilot/concepts/agents/copilot-in-jetbrains)
- [awesome-copilot: Installing and Using Plugins](https://awesome-copilot.github.com/learning-hub/installing-and-using-plugins/)
- [Ken Muse: Creating Agent Plugins](https://www.kenmuse.com/blog/creating-agent-plugins-for-vs-code-and-copilot-cli/) - historical walkthrough; use current host docs for configuration
- [Agent Skills Standard](https://agentskills.io)
- [GitHub Changelog: Agent Skills](https://github.blog/changelog/2025-12-18-github-copilot-now-supports-agent-skills/)
- [copilot-plugins Registry](https://github.com/github/copilot-plugins)
- [awesome-copilot Marketplace](https://github.com/github/awesome-copilot)

## Connect with Chris Ayers

Feel free to connect with Chris Ayers on social media and visit his blog for more information on Copilot extensibility and other topics:

- BlueSky: [@chris-ayers.com](https://bsky.app/profile/chris-ayers.com)
- LinkedIn: [chris-l-ayers](https://linkedin.com/in/chris-l-ayers/)
- Blog: [https://chris-ayers.com/](https://chris-ayers.com/)
- GitHub: [Codebytes](https://github.com/codebytes)
- Mastodon: [@Chrisayers@hachyderm.io](https://hachyderm.io/@Chrisayers)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.