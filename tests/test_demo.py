import csv
import json
import re
import shlex
import statistics
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "document-tools"
SKILL = PLUGIN / "skills" / "csv-analysis" / "SKILL.md"
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

    def test_there_is_one_canonical_skill(self):
        self.assertEqual(list((ROOT / "plugins").rglob("SKILL.md")), [SKILL])
        source = SKILL.read_text(encoding="utf-8")
        frontmatter = source.split("---", 2)[1]
        self.assertIn("\nname: csv-analysis\n", frontmatter)
        description = re.search(r"^description: (.+)$", frontmatter, re.MULTILINE)
        self.assertIsNotNone(description)
        self.assertGreater(len(description.group(1)), 0)
        self.assertLessEqual(len(description.group(1)), 1024)
        self.assertNotIn("allowed-tools:", frontmatter)
        self.assertIn("statistics.stdev", source)

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


if __name__ == "__main__":
    unittest.main()
