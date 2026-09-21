import csv
import json
import re
import shlex
import statistics
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "document-tools"
SKILL = PLUGIN / "skills" / "csv-analysis" / "SKILL.md"
SIMPLE_SKILL = PLUGIN / "skills" / "release-note" / "SKILL.md"
AGENT = PLUGIN / "com.github.copilot" / "agents" / "data-analyst.agent.md"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class DemoConfigurationTests(unittest.TestCase):
    def test_portable_manifest_has_only_standard_fields(self):
        manifest = read_json(PLUGIN / "plugin.json")
        self.assertEqual(
            manifest["$schema"],
            "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        )
        self.assertEqual(manifest["name"], "document-tools")
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertLessEqual(len(manifest["name"]), 64)
        self.assertRegex(
            manifest["name"], r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$"
        )
        self.assertLessEqual(
            set(manifest),
            {
                "$schema", "name", "version", "description", "author", "homepage",
                "repository", "license", "keywords", "extensions",
            },
        )

    def test_skill_examples_have_one_canonical_entry_each(self):
        self.assertEqual(set((ROOT / "plugins").rglob("SKILL.md")), {SKILL, SIMPLE_SKILL})
        self.assertEqual(list(SIMPLE_SKILL.parent.iterdir()), [SIMPLE_SKILL])
        minimal = SIMPLE_SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(minimal.splitlines()), 8)
        self.assertIn("name: release-note", minimal)
        deck = (ROOT / "slides/Slides.md").read_text(encoding="utf-8")
        self.assertIn(f"```markdown\n{minimal}```", deck)
        source = SKILL.read_text(encoding="utf-8")
        frontmatter = source.split("---", 2)[1]
        self.assertIn("\nname: csv-analysis\n", frontmatter)
        description = re.search(
            r"^description: >-\n((?:[ \t]+[^\n]+(?:\n|$))+)",
            frontmatter,
            re.MULTILINE,
        )
        self.assertIsNotNone(description)
        description_text = " ".join(line.strip() for line in description.group(1).splitlines())
        self.assertGreater(len(description_text), 0)
        self.assertLessEqual(len(description_text), 1024)
        self.assertEqual(re.findall(r"^([a-z-]+):", frontmatter, re.MULTILINE), ["name", "description"])
        self.assertNotIn("allowed-tools:", frontmatter)
        self.assertIn("statistics.stdev", source)
        self.assertIn("USE FOR:", frontmatter)
        self.assertIn("DO NOT USE FOR:", frontmatter)
        for section in ("Workflow", "Safety", "Exit Criteria"):
            self.assertIn(f"## {section}", source)
        for reference in re.findall(r"\[[^\]]+\]\(([^)]+)\)", source):
            if not reference.startswith(("https://", "http://")):
                self.assertTrue((SKILL.parent / reference).is_file(), reference)

    def test_quality_layers_are_distinct(self):
        suite = (ROOT / "evals/csv-analysis/eval.yaml").read_text()
        self.assertIn("executor: mock", suite)
        self.assertIn("model: mock-model", suite)
        tasks = list((ROOT / "evals/csv-analysis/tasks").glob("*.yaml"))
        self.assertEqual(len(tasks), 4)
        contents = [task.read_text() for task in tasks]
        for content in contents:
            self.assertIn("type: trigger", content)
            self.assertIn("skill_path: plugins/document-tools/skills/csv-analysis/SKILL.md", content)
        self.assertTrue(any("mode: positive" in content for content in contents))
        self.assertTrue(any("mode: negative" in content for content in contents))
        capability = (SKILL.parent / "evals/csv-analysis/eval.yaml").read_text()
        self.assertIn("type: capability", capability)
        self.assertIn("executor: copilot-sdk", capability)
        self.assertIn("measured-csv-report", capability)
        self.assertIn("missing-input-is-a-blocker", capability)

    def test_diagrams_have_synchronized_editable_models(self):
        for path in (ROOT / "slides/img").glob("*.spec.json"):
            with self.subTest(diagram=path.name):
                spec = read_json(path)
                svg = ET.parse(path.with_name(path.name.replace(".spec.json", ".drawio.svg"))).getroot()
                self.assertEqual(svg.attrib["role"], "img")
                model = ET.fromstring(svg.attrib["content"])
                cells = {cell.attrib["id"]: cell for cell in model.iter("mxCell")}
                self.assertEqual(
                    {key for key, cell in cells.items() if cell.attrib.get("vertex") == "1"},
                    {node["id"] for node in spec["nodes"]},
                )
                for node in spec["nodes"]:
                    self.assertEqual(cells[node["id"]].attrib["value"], node["label"])
                    geometry = cells[node["id"]].find("mxGeometry")
                    for dimension in ("x", "y", "width", "height"):
                        self.assertEqual(float(geometry.attrib[dimension]), node[dimension])

    def test_claude_adapter_reuses_the_package_and_agent(self):
        portable = read_json(PLUGIN / "plugin.json")
        claude = read_json(PLUGIN / ".claude-plugin" / "plugin.json")
        for field in ("name", "version", "description", "license"):
            self.assertEqual(claude[field], portable[field])
        self.assertEqual(
            claude["agents"], ["./com.github.copilot/agents/data-analyst.agent.md"]
        )
        for path in claude["agents"]:
            resolved = (PLUGIN / path).resolve()
            self.assertTrue(resolved.is_relative_to(PLUGIN.resolve()))
            self.assertTrue(resolved.is_file())
        self.assertNotIn("skills", claude)
        self.assertNotIn("hooks", claude)
        self.assertEqual(
            (AGENT.parent / "../../skills/csv-analysis/SKILL.md").resolve(), SKILL
        )
        self.assertIn("\n  - Skill\n", AGENT.read_text(encoding="utf-8"))

    def test_copilot_catalog_matches_the_package(self):
        package = read_json(PLUGIN / "plugin.json")
        catalog = read_json(ROOT / ".github" / "plugin" / "marketplace.json")
        self.assertEqual(catalog["name"], "codebytes-agent-skills")
        self.assertEqual(catalog["metadata"]["version"], package["version"])
        self.assertEqual(len(catalog["plugins"]), 1)
        entry = catalog["plugins"][0]
        for field in ("name", "version", "description"):
            self.assertEqual(entry[field], package[field])
        self.assertEqual((ROOT / entry["source"]).resolve(), PLUGIN)

    def test_hook_is_a_host_specific_context_reminder(self):
        hook_file = PLUGIN / "com.github.copilot" / "hooks" / "hooks.json"
        config = read_json(hook_file)
        self.assertEqual(config["version"], 1)
        self.assertEqual(set(config["hooks"]), {"SubagentStart"})
        hook, = config["hooks"]["SubagentStart"]
        self.assertEqual(hook["type"], "command")
        executable, argument = shlex.split(hook["command"])
        self.assertEqual(executable, "echo")
        output = json.loads(argument)
        self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "SubagentStart")
        self.assertEqual(
            output["additionalContext"],
            output["hookSpecificOutput"]["additionalContext"],
        )
        self.assertNotIn("permissionDecision", output)
        self.assertNotIn("permissionDecision", output["hookSpecificOutput"])
        self.assertFalse((PLUGIN / "hooks.json").exists())

    def test_claude_catalog_matches_the_copilot_catalog(self):
        self.assertEqual(
            read_json(ROOT / ".claude-plugin" / "marketplace.json"),
            read_json(ROOT / ".github" / "plugin" / "marketplace.json"),
        )

    def test_codex_catalog_reuses_the_portable_package(self):
        catalog = read_json(ROOT / ".agents" / "plugins" / "marketplace.json")
        self.assertEqual(catalog["name"], "codebytes-agent-skills")
        entry, = catalog["plugins"]
        self.assertEqual(entry["name"], read_json(PLUGIN / "plugin.json")["name"])
        self.assertEqual(entry["source"]["source"], "local")
        self.assertEqual((ROOT / entry["source"]["path"]).resolve(), PLUGIN)
        self.assertEqual(entry["policy"]["installation"], "AVAILABLE")
        self.assertEqual(entry["policy"]["authentication"], "ON_INSTALL")
        self.assertFalse((PLUGIN / ".codex-plugin" / "plugin.json").exists())

    def test_gemini_adapter_uses_default_skill_discovery(self):
        extension = read_json(PLUGIN / "gemini-extension.json")
        package = read_json(PLUGIN / "plugin.json")
        self.assertEqual(set(extension), {"name", "version"})
        self.assertEqual(extension["name"], package["name"])
        self.assertEqual(extension["version"], package["version"])
        self.assertTrue(SKILL.is_file())

    def test_sample_report_matches_the_data(self):
        with (PLUGIN / "examples" / "sample.csv").open(newline="", encoding="utf-8") as source:
            rows = list(csv.DictReader(source))
        self.assertEqual(len(rows), 10)
        self.assertEqual(len(rows[0]), 5)
        self.assertEqual(len({tuple(row.values()) for row in rows}), len(rows))
        populated = sum(bool(value) for row in rows for value in row.values())
        self.assertEqual(populated, 48)
        report = (PLUGIN / "examples" / "sample-report.md").read_text(encoding="utf-8")
        self.assertIn("96% completeness", report)
        self.assertIn("Sample Std Dev", report)
        for column in ("age", "salary"):
            values = [float(row[column]) for row in rows if row[column]]
            for value in (
                statistics.mean(values),
                statistics.median(values),
                statistics.stdev(values),
            ):
                self.assertIn(f"{value:,.2f}", report)

    def test_documented_json_is_parseable_and_versions_match(self):
        package = read_json(PLUGIN / "plugin.json")
        for path in (ROOT / "README.md", PLUGIN / "README.md", ROOT / "slides" / "Slides.md"):
            source = path.read_text(encoding="utf-8")
            for index, block in enumerate(re.findall(r"```json\n(.*?)\n```", source, re.DOTALL)):
                with self.subTest(path=path.relative_to(ROOT), block=index):
                    example = json.loads(block)
                    self.assertIsInstance(example, dict)
                    entries = [example]
                    if "plugins" in example:
                        self.assertIsInstance(example["plugins"], list)
                        entries.extend(example["plugins"])
                    for entry in entries:
                        self.assertIsInstance(entry, dict)
                        if entry.get("name") == package["name"] and "version" in entry:
                            self.assertEqual(entry["version"], package["version"])

    def test_per_plugin_mcp_example_does_not_configure_demo_servers(self):
        source = (ROOT / "slides/Slides.md").read_text(encoding="utf-8")
        examples = [
            json.loads(block)
            for block in re.findall(r"```json\n(.*?)\n```", source, re.DOTALL)
        ]
        mcp_examples = [
            example for example in examples
            if example.get("$schema") == "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
        ]
        self.assertEqual(len(mcp_examples), 1)
        self.assertEqual(set(mcp_examples[0]), {"$schema", "mcpServers"})
        servers = mcp_examples[0]["mcpServers"]
        self.assertEqual(set(servers), {"docs", "issues"})
        for name, server in servers.items():
            self.assertEqual(server, {
                "type": "streamable-http",
                "url": f"https://{name}.example.com/mcp",
            })
        self.assertFalse((PLUGIN / "mcp.json").exists())
        self.assertIn("Server processes are not separate model context windows.", source)

    def test_slide_assets_and_frontmatter(self):
        deck = ROOT / "slides" / "Slides.md"
        source = deck.read_text(encoding="utf-8")
        frontmatter = source.split("---", 2)[1]
        for directive in ("marp: true", "theme: custom-default", "paginate: true", "math: mathjax"):
            self.assertIn(directive, frontmatter)
        for reference in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", source):
            if not reference.startswith(("https://", "http://")):
                with self.subTest(asset=reference):
                    self.assertTrue((deck.parent / reference).is_file())
        self.assertNotIn("```mermaid", source)
        self.assertIn("## Waza: Check the Routing Contract", source)
        self.assertIn("## Vally: Test the Agent's Actual Work", source)
        preview = source.split("## Preview This Fixture Locally", 1)[1].split("\n---\n", 1)[0]
        self.assertIn('copilot --plugin-dir "$PLUGIN" skill list', preview)
        self.assertIn("/skills info document-tools:csv-analysis", preview)
        self.assertIn("collision example", preview)
        loading_order = (
            "## Chris Ayers",
            "## Stop Re-explaining the Same Task",
            "## What Is an Agent Skill?",
            "## When Is a Task Worth a Skill?",
            "## Choose the Smallest Useful Mechanism",
            "## What a Model Call Can See",
            "## Instructions Are Included, Not Invoked",
            "## How Skills Are Loaded",
            "## Load the Next Layer Only When Needed",
            "## How Agent Profiles Are Loaded",
            "## A Profile Is Not an Extra Window",
            "## Subagents Isolate Intermediate Work",
            "## First Example: One File Is Enough",
            "## Our Destination:",
            "## Real Instruction Files",
            "## One Real Skill",
        )
        positions = [source.index(title) for title in loading_order]
        self.assertEqual(positions, sorted(positions))
        instructions = source.split("## Instructions Are Included, Not Invoked", 1)[1].split("\n---\n", 1)[0]
        for term in ("GitHub Copilot", "Claude Code", "AGENTS.md", "CLAUDE.md", "2.1.277+; conditional"):
            self.assertIn(term, instructions)
        self.assertLess(source.index("## Our Destination:"), source.index("## One Real Skill"))
        self.assertLess(source.index("## Describe When the Skill Should Win"), source.index("## Name the Skill, Match the Folder"))
        self.assertLess(source.index("## Name the Skill, Match the Folder"), source.index("## Keep the Main Workflow Short"))
        self.assertLess(source.index("## What's Inside a Plugin?"), source.index("## One Plugin, Multiple MCP Servers"))
        self.assertLess(source.index("## One Plugin, Multiple MCP Servers"), source.index("## The Host Decides"))
        self.assertLess(source.index("## Review Before You Load"), source.index("copilot --plugin-dir"))
        self.assertLess(source.index("## Verify the Result"), source.index("## Declare the Catalog"))
        self.assertLess(source.index("# Reference Appendix"), source.index("## Discovery Paths"))
        self.assertLess(source.index("# <!-- fit --> Questions?"), source.index("## Connect with Chris Ayers"))
        self.assertLess(source.index("## Connect with Chris Ayers"), source.index("# Reference Appendix"))


if __name__ == "__main__":
    unittest.main()
