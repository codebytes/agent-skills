# Agent Skills, Plugins & Marketplace

A working example of the GitHub Copilot agent extensibility ecosystem — skills, plugins, and a marketplace — in a single repo.

## What's In This Repo

| Component | Location | Description |
|-----------|----------|-------------|
| **Marketplace** | `.github/plugin/marketplace.json` | Plugin registry — register with `copilot plugin marketplace add codebytes/agent-skills` |
| **Plugin** | `plugins/document-tools/` | Installable plugin with a data-analyst agent and CSV analysis skill |
| **Skills** | `.github/skills/`, `.agents/skills/`, `.gemini/skills/` | Cross-tool skill discovery for Copilot, Codex, and Gemini |
| **Slides** | `slides/Slides.md` | Marp presentation covering all three concepts |

## Quick Start

```bash
# Register this repo as a marketplace
copilot plugin marketplace add codebytes/agent-skills

# Browse available plugins
copilot plugin marketplace browse agent-skills

# Install the document-tools plugin
copilot plugin install document-tools@agent-skills
```

### VS Code

1. Set `chat.plugins.enabled` to `true`
2. Add `"codebytes/agent-skills"` to `chat.plugins.marketplaces`
3. Search `@agentPlugins` in Extensions view

## Cross-Tool Compatibility

This repo provides skill discovery paths for multiple AI coding tools:

| Tool | Skill Location | Plugin Manifest |
|------|---------------|-----------------|
| **Copilot CLI / VS Code** | `.github/skills/` | `.github/plugin.json` |
| **Claude Code** | `.claude/skills/` | `.claude-plugin/plugin.json` |
| **Codex CLI** | `.agents/skills/` | — |
| **Gemini CLI** | `.gemini/skills/` | — |

Skills use the [Agent Skills](https://agentskills.io) open standard — write once, discovered everywhere.

## Slides

Built with [Marp](https://marp.app/). Preview in VS Code with the [Marp extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode), or export:

```bash
npm install -g @marp-team/marp-cli
marp --theme-set slides/themes --pdf slides/Slides.md
```

## Resources

- [GitHub Docs: About CLI Plugins](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-cli-plugins)
- [awesome-copilot: Installing and Using Plugins](https://awesome-copilot.github.com/learning-hub/installing-and-using-plugins/)
- [Ken Muse: Creating Agent Plugins](https://www.kenmuse.com/blog/creating-agent-plugins-for-vs-code-and-copilot-cli/)
- [Agent Skills Standard](https://agentskills.io)
- [GitHub Changelog: Agent Skills](https://github.blog/changelog/2025-12-18-github-copilot-now-supports-agent-skills/)

## License

[MIT](LICENSE)