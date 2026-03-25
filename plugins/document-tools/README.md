# Document Tools Plugin

A GitHub Copilot plugin providing data analysis agents and skills for CSV, JSON, and tabular data.

## Structure

```
document-tools/
├── .github/
│   └── plugin.json              # Plugin manifest
├── agents/
│   └── data-analyst.agent.md    # Custom agent persona
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

## Installation

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
- Ask: "Analyze this CSV file and generate a report"
