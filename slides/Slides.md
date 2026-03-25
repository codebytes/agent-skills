---
marp: true
theme: custom-default
paginate: true
footer: '@chris-ayers'
math: mathjax
---

<!-- Mermaid.js for diagrams -->
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true });
</script>

<!-- _paginate: skip -->
<!-- _footer: "" -->
<!-- _class: lead invert -->

# Agent Skills, Plugins & Marketplace

Extending GitHub Copilot with Reusable AI Capabilities

<!-- This talk covers the new extensibility model for GitHub Copilot: agent skills for teaching Copilot specialized tasks, plugins for packaging and distributing those capabilities, and marketplaces for discovering and sharing them across teams. -->

---

<!-- _class: lead -->

# Agenda

1. **Agent Skills** — Teaching Copilot specialized tasks
2. **Plugins** — Packaging reusable capabilities
3. **Marketplaces** — Discovering & sharing plugins
4. **Demo** — Building a plugin from scratch
5. **Best Practices** — Tips for teams

<!-- Walk through each concept, then do a live demo building a plugin and publishing it to a marketplace. -->

---

<!-- _class: lead invert -->

# Agent Skills

---

## What Are Agent Skills?

Skills are **folders** containing instructions, scripts, and resources that Copilot **automatically loads** when relevant to your prompt.

- Defined with a `SKILL.md` file
- Discovered automatically from `.github/skills/`
- Work across **Copilot CLI**, **VS Code**, and **Coding Agent**
- Can include scripts, templates, and reference files

<!-- Agent skills were announced December 2025. They work across all three Copilot surfaces. The key insight is that skills are demand-loaded — Copilot only loads them when it determines they're relevant to the current task. -->

---

## Skill Directory Structure

```
.github/skills/
└── csv-analysis/
    ├── SKILL.md          # Instructions & tool config
    ├── scripts/
    │   └── analyze.py    # Supporting scripts
    └── templates/
        └── report.md     # Output templates
```

- `SKILL.md` is the entry point — **required**
- Supporting files are referenced from the instructions
- Skills can specify which **tools** and **model** to use

<!-- The SKILL.md file is the heart of a skill. It contains the instructions Copilot follows, plus metadata about which tools to use. Supporting files like scripts and templates give the skill concrete capabilities beyond just prompting. -->

---

## Anatomy of a SKILL.md

```markdown
---
name: csv-analysis
description: Analyze CSV files and generate reports
tools:
  - powershell
  - create
  - view
---

## Instructions

When asked to analyze a CSV file:
1. Read the file with the view tool
2. Run `scripts/analyze.py` to compute statistics
3. Generate a report using `templates/report.md`

## Output Format

Always include: row count, column types, 
summary statistics, and any anomalies found.
```

<!-- The frontmatter declares the skill name, description, and which tools it needs. The body contains the actual instructions Copilot will follow. You can be very specific about the workflow and output format. -->

---

## How Skills Are Discovered

<div class="mermaid">
flowchart LR
    A[User Prompt] --> B{Copilot Evaluates<br/>Relevance}
    B -->|Relevant| C[Load SKILL.md]
    B -->|Not Relevant| D[Skip Skill]
    C --> E[Execute with<br/>Specified Tools]
    E --> F[Return Results]
</div>

Skills load **on demand** — only when Copilot determines they match the task.

<!-- This is important for performance. You can have dozens of skills defined, but Copilot only loads the ones relevant to the current prompt. This keeps context windows clean and focused. -->

---

## Skill Discovery Locations

<!-- _class: small -->

| Location | Tool | Scope |
|----------|------|-------|
| `.github/skills/` | Copilot CLI, VS Code | Repository |
| `.claude/skills/` | Claude Code, Copilot | Repository |
| `.agents/skills/` | Codex CLI | Repository |
| `.gemini/skills/` | Gemini CLI | Repository |
| `~/.copilot/skills/` | Copilot CLI | User-level |
| `~/.claude/skills/` | Claude Code | User-level |
| `~/.agents/skills/` | Codex CLI | User-level |
| `~/.gemini/skills/` | Gemini CLI | User-level |
| Installed plugins | All | Global |

<!-- All five tools — Copilot CLI, VS Code, Claude Code, Codex CLI, and Gemini CLI — support the same SKILL.md format. The difference is WHERE they look for skills. Skills are the most portable piece of the ecosystem. Write once, discovered everywhere. -->

---

<!-- _class: lead invert -->

# Cross-Tool Compatibility

---

## The Open Agent Skills Standard

The SKILL.md format is an **open standard** ([agentskills.io](https://agentskills.io)) shared across leading AI agent tools:

- ✅ **GitHub Copilot CLI** — Full plugin + marketplace support
- ✅ **VS Code** (Copilot agent mode) — Plugin support (preview)
- ✅ **Claude Code** — Full plugin + marketplace support
- ✅ **OpenAI Codex CLI** — Skills support, community registries
- ✅ **Gemini CLI** — Skills + extensions support

All use the same `SKILL.md` file with `name`, `description`, and instructions.

<!-- The agent skills standard at agentskills.io defines a portable format that works across tools. This is huge — you write a skill once, and it works in Copilot, Claude, Codex, Gemini, Cursor, and more. -->

---

## Plugin Manifest Differences

<!-- _class: small -->

| Tool | Manifest Location | Marketplace |
|------|-------------------|-------------|
| **Copilot CLI** | `.github/plugin.json` | `.github/plugin/marketplace.json` |
| **VS Code** | `.github/plugin.json` | Same as Copilot CLI |
| **Claude Code** | `.claude-plugin/plugin.json` | Supported (same concept) |
| **Codex CLI** | No plugin.json | `$skill-installer`, community repos |
| **Gemini CLI** | Extensions system | `gemini extensions`, registries |

**Solution:** Include **multiple** manifests in your plugin:

```
my-plugin/
├── .github/plugin.json          # Copilot CLI + VS Code
├── .claude-plugin/plugin.json   # Claude Code
├── agents/
├── skills/
└── hooks.json
```

<!-- The plugin manifest format is nearly identical between Copilot and Claude Code — the only difference is the directory name. Include both and your plugin works everywhere. Codex uses a different approach with .agents/skills/ and $skill-installer. -->

---

## Making a Plugin Work Everywhere

```
my-plugin/
├── .github/
│   └── plugin.json              # Copilot CLI + VS Code
├── .claude-plugin/
│   └── plugin.json              # Claude Code
├── agents/
│   └── data-analyst.agent.md    # All tools
├── skills/
│   └── csv-analysis/
│       └── SKILL.md             # Universal format
└── hooks.json                   # Copilot + Claude
```

**For Codex + Gemini:** Provide skills at the repo root:
```
.agents/skills/    # Codex CLI discovery
.gemini/skills/    # Gemini CLI discovery
```

<!-- This repo demonstrates this exact pattern. We include .github/plugin.json, .claude-plugin/plugin.json, and provide .agents/skills/ and .gemini/skills/ at the repo root for Codex and Gemini users. -->

---

<!-- _class: lead invert -->

# Plugins

---

## What Are Plugins?

Plugins are **installable packages** that bundle Copilot customizations into a single distributable unit.

Think of it as **package management for your Copilot configurations**.

<!-- Before plugins, sharing Copilot customizations meant submodules, manual file copying, or trying to keep configurations in sync across repos. Plugins solve this with a proper packaging and distribution model. -->

---

## What Plugins Contain

| Component | File Pattern | Purpose |
|-----------|-------------|---------|
| **Custom Agents** | `agents/*.agent.md` | Specialized AI assistants |
| **Skills** | `skills/*/SKILL.md` | Discrete callable capabilities |
| **Hooks** | `hooks.json` | Lifecycle event handlers |
| **MCP Servers** | `.mcp.json` | External tool integrations |
| **LSP Servers** | `lsp.json` | Language server integrations |

A plugin can include **any combination** of these.

<!-- A plugin is flexible — it can be as simple as a single agent, or as complex as a full development toolkit with multiple agents, skills, hooks, and server configurations all working together. -->

---

## Plugin Directory Structure

```
my-plugin/
├── .github/
│   └── plugin.json           # Plugin manifest (required)
├── agents/
│   ├── api-architect.agent.md
│   └── test-writer.agent.md
├── skills/
│   └── database-migrations/
│       ├── SKILL.md
│       └── scripts/migrate.sh
├── hooks.json
└── .mcp.json
```

<!-- The plugin.json manifest in .github/ is the only required file. Everything else is optional. The manifest declares what the plugin contains and points to the component locations. -->

---

## The Plugin Manifest

```json
{
  "name": "my-dev-toolkit",
  "description": "Full-stack development toolkit",
  "version": "1.0.0",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "license": "MIT",
  "keywords": ["fullstack", "api", "testing"],
  "agents": [
    "./agents/api-architect.agent.md",
    "./agents/test-writer.agent.md"
  ],
  "skills": [
    "./skills/database-migrations/"
  ]
}
```

<!-- plugin.json lives in .github/ within the plugin directory. The name should only contain letters, numbers, and dashes. File paths are relative to the plugin root, not the .github directory. -->

---

## Plugins vs Manual Configuration

<!-- _class: columns -->

## Manual Config

- Scoped to **single repository**
- Sharing via **copy/paste**
- Versioned through **git history**
- Discovery by **searching repos**

## Plugins

- Works across **any project**
- Install with **one command**
- **Marketplace versioning**
- **Browsable** marketplace registry

<!-- The key advantage is reusability and consistency. Define once, install everywhere. No more drift between team members running different versions of the same configuration. -->

---

<!-- _class: lead invert -->

# Marketplaces

---

## What Is a Marketplace?

A **marketplace** is a Git repository that serves as a **registry** for available plugins.

- Contains a `marketplace.json` manifest
- Lists plugins with metadata and source locations
- Acts as a lightweight **app store** for plugins

<!-- Think of it like npm registry, but for Copilot plugins. A marketplace is just a Git repo with a specific JSON file that describes what plugins are available and where to find them. -->

---

## Default Marketplaces

Two marketplaces are registered **by default** — no setup needed:

| Marketplace | Description |
|-------------|-------------|
| **[copilot-plugins](https://github.com/github/copilot-plugins)** | Official GitHub Copilot plugins |
| **[awesome-copilot](https://github.com/github/awesome-copilot)** | Community-contributed plugins |

Additional community resources:
- [anthropic/skills](https://github.com/anthropics/skills) — Reference skills (Anthropic)
- [DevsForge Marketplace](https://github.com/claudeforge/marketplace) — Community plugins

<!-- Both VS Code and Copilot CLI ship with these two marketplaces pre-configured. You can start browsing and installing plugins immediately without any setup. -->

---

## Creating a Marketplace

```json
// .github/plugin/marketplace.json
{
  "name": "my-team-plugins",
  "owner": {
    "name": "My Team",
    "email": "team@example.com"
  },
  "metadata": {
    "description": "Internal team plugin registry",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "dev-toolkit",
      "description": "Full-stack development tools",
      "version": "1.0.0",
      "source": "./plugins/dev-toolkit"
    }
  ]
}
```

<!-- The marketplace.json file goes in .github/plugin/ at the root of a Git repository. Each plugin entry points to a directory containing the plugin manifest. Push to GitHub and you have a working marketplace. -->

---

## Marketplace Architecture

<div class="mermaid">
flowchart TD
    M[Marketplace Repository] --> MJ[marketplace.json]
    MJ --> P1[Plugin: dev-toolkit]
    MJ --> P2[Plugin: security-scanner]
    MJ --> P3[Plugin: docs-generator]
    P1 --> PJ1[.github/plugin.json]
    P1 --> A1[agents/]
    P1 --> S1[skills/]
    P2 --> PJ2[.github/plugin.json]
    P2 --> MCP2[.mcp.json]
    P3 --> PJ3[.github/plugin.json]
    P3 --> S3[skills/]
    P3 --> H3[hooks.json]
</div>

<!-- A single marketplace repository can host multiple plugins, each with their own combination of components. Plugins can also reference external repositories for versioned sources. -->

---

## Versioning with External Sources

Plugins can reference **external repositories** with specific versions:

```json
{
  "plugins": [
    {
      "name": "external-tool",
      "description": "Tool from another repo",
      "version": "2.0.0",
      "source": {
        "source": "url",
        "url": "https://github.com/org/tool-plugin",
        "ref": "v2.0"
      }
    }
  ]
}
```

<!-- This allows your marketplace to curate plugins from multiple repositories, each pinned to a specific tag or branch. Great for enterprise teams that want to control which versions are available. -->

---

<!-- _class: lead invert -->

# Installing & Managing Plugins

---

## Copilot CLI Commands

```bash
# Browse marketplaces
copilot plugin marketplace list
copilot plugin marketplace browse awesome-copilot

# Install plugins
copilot plugin install dev-toolkit@awesome-copilot
copilot plugin install user/repo
copilot plugin install user/repo:plugins/subfolder

# Manage plugins
copilot plugin list
copilot plugin update my-plugin
copilot plugin uninstall my-plugin

# Add custom marketplace
copilot plugin marketplace add my-org/internal-plugins
```

<!-- Copilot CLI provides the most detailed error messages when something goes wrong. Ken Muse recommends starting with CLI before VS Code for troubleshooting. -->

---

## VS Code Integration

1. Enable: Set `chat.plugins.enabled` to `true`
2. Add marketplaces in settings:

```json
{
  "chat.plugins.marketplaces": [
    "my-org/my-plugins"
  ]
}
```

3. Browse: Extensions view → search `@agentPlugins`
4. Or: Command Palette → **Chat: Plugins**

<!-- VS Code must have plugins enabled as a preview feature. Marketplace configurations must be set at the user level — workspace settings won't work. The @agentPlugins search filter in Extensions view shows all available plugins from your registered marketplaces. -->

---

## How Plugins Work at Runtime

<div class="mermaid">
flowchart LR
    I[Install Plugin] --> R[Plugin Registry]
    R --> AG[Agents Available]
    R --> SK[Skills Auto-load]
    R --> HK[Hooks Execute]
    R --> MC[MCP Servers Connect]
    AG --> S[Copilot Session]
    SK --> S
    HK --> S
    MC --> S
</div>

After installation, plugin components **integrate automatically**:
- Agents appear in agent selection
- Skills load when relevant
- Hooks fire at lifecycle events
- MCP servers extend available tools

<!-- No additional configuration needed after install. Everything just works. This is the key UX improvement over manual configuration. -->

---

## Where Plugins Are Stored

| Source | Location |
|--------|----------|
| Marketplace plugins | `~/.copilot/installed-plugins/MARKETPLACE/PLUGIN/` |
| Direct installs | `~/.copilot/installed-plugins/_direct/PLUGIN/` |
| VS Code (macOS) | `~/Library/Application Support/Code/agentPlugins/` |
| VS Code (Windows) | `%APPDATA%/Code/agentPlugins/` |

<!-- Knowing where plugins are stored helps with debugging. If a plugin isn't loading, check these paths to verify it was installed correctly. -->

---

<!-- _class: lead invert -->

# Demo: Building a Plugin

---

## Step 1: Create the Plugin Structure

```bash
mkdir -p my-plugin/.github
mkdir -p my-plugin/agents
mkdir -p my-plugin/skills/csv-analysis
```

```
my-plugin/
├── .github/
│   └── plugin.json
├── agents/
│   └── data-analyst.agent.md
└── skills/
    └── csv-analysis/
        ├── SKILL.md
        └── scripts/
            └── analyze.py
```

<!-- Start with the directory structure. The .github/plugin.json manifest is required. Then add whatever agents, skills, hooks, or MCP configurations you need. -->

---

<!-- _class: small -->

## Step 2: Write the Plugin Manifest

```json
// my-plugin/.github/plugin.json
{
  "name": "data-analysis-toolkit",
  "description": "Data analysis agents and skills for CSV, JSON, and SQL",
  "version": "1.0.0",
  "author": { "name": "Your Team" },
  "license": "MIT",
  "keywords": ["data", "analysis", "csv"],
  "agents": ["../agents/data-analyst.agent.md"],
  "skills": ["../skills/csv-analysis/"]
}
```

> **Note:** File paths are relative to the plugin root, not the `.github/` directory.

<!-- The name field is critical — only use letters, numbers, and dashes. Other characters will cause silent failures. The paths point up from .github to the plugin root, then into the component directories. -->

---

## Step 3: Create an Agent

```markdown
<!-- agents/data-analyst.agent.md -->
---
name: data-analyst
description: Expert data analyst for CSV, JSON, and SQL data
tools:
  - powershell
  - view
  - create
---

You are an expert data analyst. When given data files:

1. Identify the format (CSV, JSON, SQL dump)
2. Profile the data (row counts, column types, nulls)
3. Generate summary statistics
4. Flag anomalies or quality issues
5. Produce a clean, formatted report
```

<!-- The agent markdown file defines a persona with specific tools. When users invoke this agent, Copilot adopts this persona and follows these instructions. -->

---

## Step 4: Create a Skill

```markdown
<!-- skills/csv-analysis/SKILL.md -->
---
name: csv-analysis
description: Analyze CSV files and generate statistical reports
tools:
  - powershell
  - view
  - create
---

## Instructions

When asked to analyze a CSV file:
1. Read the file and identify columns
2. Compute summary statistics per column
3. Detect missing values and outliers
4. Generate a markdown report with tables

## Output

Include: row count, column types, min/max/mean,
null counts, and any detected anomalies.
```

<!-- Skills are more focused than agents — they define a specific capability rather than a persona. Copilot loads skills on-demand when it detects they're relevant to the current task. -->

---

## Step 5: Publish as a Marketplace

```json
// .github/plugin/marketplace.json
{
  "name": "agent-skills",
  "owner": { "name": "Chris Ayers" },
  "metadata": {
    "description": "Agent skills and plugins for Copilot",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "document-tools",
      "description": "Data analysis toolkit",
      "version": "1.0.0",
      "source": "./plugins/document-tools"
    }
  ]
}
```

Push to GitHub → teammates can install immediately!

<!-- That's it. Push the repo to GitHub, and anyone can add your marketplace and install your plugins. The source field points to the plugin directory relative to the repo root. -->

---

## Step 6: Install & Use

```bash
# Add the marketplace
copilot plugin marketplace add codebytes/agent-skills

# Browse available plugins
copilot plugin marketplace browse agent-skills

# Install the plugin
copilot plugin install document-tools@agent-skills

# Verify installation
copilot plugin list
```

Now the agent and skills are available in **every project**!

<!-- Once installed, the data-analyst agent appears in agent selection and the csv-analysis skill auto-loads whenever a user works with CSV files. No per-project configuration needed. -->

---

<!-- _class: lead invert -->

# Security & Permissions

---

## Plugin Security Model

- **Folder trust** — Repo-level hooks only load after user confirms trust
- **Tool permissions** — Standard approval prompts for plugin tools
- **`skipPermission`** — Plugin authors can mark safe operations
- **MCP allowlists** — Restrict servers via `MCP_ALLOWLIST` feature flag
- **Review before install** — Always inspect unfamiliar plugins

<div class="mermaid">
flowchart LR
    T[Plugin Tool Call] --> P{Permission<br/>Required?}
    P -->|skipPermission: true| E[Execute]
    P -->|Standard| A[User Approval]
    A -->|Approved| E
    A -->|Denied| D[Blocked]
</div>

<!-- Security is built into the plugin system. Users always have control over what runs. The skipPermission flag should only be used for read-only or known-safe operations. -->

---

<!-- _class: lead invert -->

# Best Practices

---

## Tips for Teams

- **Start with marketplace plugins** before building your own
- **Keep plugins focused** — one domain per plugin
- **Use plugins for team standards** — ensure consistency
- **Test with Copilot CLI first** — better error messages than VS Code
- **Version with tags** — pin external sources to `ref` values
- **Review what you install** — plugins run code on your machine
- **Update regularly** — `copilot plugin update` for latest fixes

<!-- The most common mistake is making plugins too broad. A "Rails development" plugin is better than an "everything" plugin. Focused plugins are easier to maintain and compose. -->

---

<!-- _class: small -->

## Known Limitations (Preview)

| Issue | Detail |
|-------|--------|
| **VS Code settings** | Marketplaces must be user-level, not workspace |
| **Dev containers** | Plugin install may not work in containers |
| **Silent failures** | Manifest errors cause feeds to not appear |
| **Aggressive caching** | VS Code caches feed details; may need reload |
| **Branch installs** | CLI doesn't yet support branch-based install |

> **Tip:** Use VS Code Insiders for the latest fixes. Use Copilot CLI for debugging plugin issues.

<!-- These are preview-era limitations that will improve. The most frustrating is silent failures — if your marketplace.json has a typo, the feed simply won't appear with no error message. Always validate with Copilot CLI first. -->

---

<!-- _class: columns -->

## The Ecosystem

## Create

- Write `SKILL.md` files
- Build `.agent.md` personas
- Configure `hooks.json`
- Set up `.mcp.json`

## Distribute

- Bundle in `plugin.json`
- Publish to marketplace
- Version with Git tags
- Share across teams

<!-- The ecosystem is designed for a create-distribute-consume workflow. Teams create skills and agents, package them as plugins, publish to marketplaces, and consumers install with one command. -->

---

## Resources

- 📖 [GitHub Docs: About CLI Plugins](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-cli-plugins)
- 🛒 [awesome-copilot Marketplace](https://github.com/github/awesome-copilot)
- 🔌 [copilot-plugins Registry](https://github.com/github/copilot-plugins)
- 📝 [Ken Muse: Creating Agent Plugins](https://www.kenmuse.com/blog/creating-agent-plugins-for-vs-code-and-copilot-cli/)
- 📢 [GitHub Changelog: Agent Skills](https://github.blog/changelog/2025-12-18-github-copilot-now-supports-agent-skills/)
- 🔍 [DeepWiki: Plugin System](https://deepwiki.com/github/copilot-cli/5.5-plugin-system-and-skills)

<!-- All the references used for this presentation. The Ken Muse blog post is especially good for a step-by-step walkthrough of creating a plugin from an existing skills repository. -->

---

<!-- _paginate: skip -->
<!-- _footer: "" -->
<!-- _class: lead invert -->

# <!--fit--> Thank You!

Questions?

<i class="fa-brands fa-github"></i> [codebytes](https://github.com/codebytes)
<i class="fa-brands fa-linkedin"></i> [chris-ayers](https://linkedin.com/in/chris-ayers)
<i class="fa-brands fa-mastodon"></i> [@Chrisayers@hachyderm.io](https://hachyderm.io/@Chrisayers)
<i class="fa-brands fa-bluesky"></i> [@chris-ayers.com](https://bsky.app/profile/chris-ayers.com)
