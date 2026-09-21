import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/document-tools/skills/csv-analysis/scripts/profile_csv.py"
SPEC = importlib.util.spec_from_file_location("profile_csv", SCRIPT)
PROFILER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROFILER)


class CsvProfilerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.input = Path(self.directory.name) / "input.csv"

    def write(self, text, encoding="utf-8"):
        self.input.write_text(text, encoding=encoding)
        return self.input

    def test_fixture_statistics_and_read_only_behavior(self):
        path = ROOT / "plugins/document-tools/examples/sample.csv"
        original = path.read_bytes()
        result = PROFILER.profile(path)
        self.assertEqual(path.read_bytes(), original)
        self.assertFalse(result["sampled"])
        self.assertEqual(result["total_rows"], 10)
        self.assertEqual(result["column_count"], 5)
        self.assertEqual(result["missing_cells"], 2)
        self.assertEqual(result["completeness_percent"], 96)
        self.assertEqual(result["duplicate_rows"], 0)
        columns = {column["name"]: column for column in result["columns"]}
        self.assertEqual(columns["salary"]["statistics"]["count"], 9)
        self.assertAlmostEqual(columns["salary"]["statistics"]["mean"], 93111.111111, places=5)
        self.assertAlmostEqual(columns["salary"]["statistics"]["sample_stddev"], 24851.782858, places=5)
        self.assertEqual(columns["start_date"]["type"], "date")
        self.assertNotIn("Alice", json.dumps(result))

    def test_missing_values_and_small_samples_are_explicit(self):
        result = PROFILER.profile(self.write("a,b\nNA,2\nN/A,\nnull, \n"))
        self.assertEqual(result["missing_cells"], 5)
        self.assertEqual(result["columns"][0]["type"], "unknown")
        stats = result["columns"][1]["statistics"]
        self.assertEqual(stats["mean"], 2)
        self.assertIsNone(stats["sample_stddev"])
        self.assertIsNone(stats["outliers_3sd"])

    def test_raw_duplicates_and_non_null_unique_counts(self):
        result = PROFILER.profile(self.write("a,b\nx,1\nx,1\n x,1\n"))
        self.assertEqual(result["duplicate_rows"], 1)
        self.assertEqual(result["columns"][0]["unique"], 2)

    def test_delimiters_and_bom(self):
        for delimiter in (",", "\t", ";", "|"):
            with self.subTest(delimiter=delimiter):
                result = PROFILER.profile(
                    self.write(f"a{delimiter}b\n1{delimiter}2\n", "utf-8-sig"),
                    delimiter=delimiter,
                )
                self.assertEqual(result["column_count"], 2)
                self.assertEqual(result["columns"][0]["name"], "a")

    def test_encoding_is_not_silently_changed(self):
        self.write("name\nAndr\u00e9\n", "cp1252")
        with self.assertRaises(UnicodeError):
            PROFILER.profile(self.input)
        self.assertEqual(PROFILER.profile(self.input, encoding="cp1252")["total_rows"], 1)

    def test_sampling_does_not_claim_whole_file_counts(self):
        self.write("a\n1\n2\n3\n")
        result = PROFILER.profile(self.input, max_rows=2)
        self.assertTrue(result["sampled"])
        self.assertIsNone(result["total_rows"])
        self.assertEqual(result["rows_analyzed"], 2)
        self.assertEqual(result["columns"][0]["statistics"]["max"], 2)
        self.assertFalse(PROFILER.profile(self.input, max_rows=3)["sampled"])
        with patch.object(PROFILER, "LARGE_FILE_BYTES", 1), patch.object(PROFILER, "SAMPLE_ROWS", 2):
            self.assertTrue(PROFILER.profile(self.input)["sampled"])

    def test_header_only_is_not_claimed_complete(self):
        result = PROFILER.profile(self.write("a,b\n"))
        self.assertEqual(result["total_rows"], 0)
        self.assertIsNone(result["completeness_percent"])

    def test_sampling_threshold_is_exactly_100_mib(self):
        self.write("a\n1\n2\n3\n")
        for size, sampled in ((100 * 1024 * 1024, False), (100 * 1024 * 1024 + 1, True)):
            with self.subTest(size=size):
                with patch.object(Path, "stat", return_value=SimpleNamespace(st_size=size)):
                    with patch.object(PROFILER, "SAMPLE_ROWS", 2):
                        self.assertEqual(PROFILER.profile(self.input)["sampled"], sampled)

    def test_types_do_not_drop_mixed_values(self):
        result = PROFILER.profile(self.write(
            "mixed,boolean,date\n1,true,2026-09-20\nunknown,FALSE,2026-09-21\n"
        ))
        self.assertEqual([c["type"] for c in result["columns"]], ["string", "boolean", "date"])
        self.assertNotIn("statistics", result["columns"][0])

    def test_invalid_inputs_fail_without_partial_output(self):
        for content in ("", "a,a\n1,2\n", "a,\n1,2\n", "a,b\n1\n", 'a\n"unterminated\n', "a\n\n", "a\nNaN\n"):
            with self.subTest(content=content):
                self.write(content)
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    status = PROFILER.main([str(self.input)])
                self.assertEqual(status, 2)
                self.assertEqual(out.getvalue(), "")
                self.assertIn("error:", err.getvalue())

    def test_cli_emits_standard_json(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            status = PROFILER.main([str(self.write("a\n1\n2\n"))])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(out.getvalue())["rows_analyzed"], 2)

    def test_row_error_identifies_record(self):
        with self.assertRaisesRegex(ValueError, "data record 2 .*has 1 cells; expected 2"):
            PROFILER.profile(self.write("a,b\n1,2\n3\n"))


if __name__ == "__main__":
    unittest.main()
