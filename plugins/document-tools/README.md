# Document Tools Demo Plugin

This compact plugin is the live example used in the "Agent Skills, Plugins &
Marketplace" talk. It demonstrates one agent, one canonical skill, one hook,
two host manifests, and a small input/output example.

> This is a presentation fixture. Maintained reusable skills live in
> [codebytes/skills](https://github.com/codebytes/skills).

## Structure

```
document-tools/
├── .claude-plugin/
│   └── plugin.json              # Claude Code plugin manifest
├── .github/
│   └── plugin.json              # GitHub Copilot plugin manifest
├── agents/
│   └── data-analyst.agent.md    # Custom agent persona
├── examples/
│   ├── sample.csv
│   └── sample-report.md
├── skills/
│   └── csv-analysis/
│       └── SKILL.md             # CSV analysis skill
└── hooks.json                   # Lifecycle hooks
```

## What's Included

| Component | Description |
|-----------|-------------|
| **data-analyst** agent | Expert data analyst for CSV, JSON, and tabular data |
| **csv-analysis** skill | Automated CSV profiling, statistics, and quality checks |
| **hooks** | Notification hook on subagent activation |

## Live Demo

### From This Marketplace

```bash
copilot plugin install document-tools@agent-skills
```

### Direct from Repository

```bash
copilot plugin install codebytes/agent-skills:plugins/document-tools
```

### Local Development

Point VS Code at the plugin directory:

```json
{
  "chat.plugins.paths": ["./plugins/document-tools"]
}
```

## Usage

Once installed:

- The **data-analyst** agent appears in your agent selection
- The **csv-analysis** skill auto-loads when you work with CSV files
- Ask: "Analyze `plugins/document-tools/examples/sample.csv` and generate a
  report"
- Compare the result with
  `plugins/document-tools/examples/sample-report.md`
