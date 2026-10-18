import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tests.helpers import TP1, phone, run_cli


class PhoneTests(unittest.TestCase):
    def test_subject_valid_examples(self):
        cases = {"01 234 (567) 89": "01-23-45-67-89",
                 "+(33) 6 58 47 25 14": "06-58-47-25-14",
                 "(0033)2 456 (789) 25": "02-45-67-89-25"}
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(phone.format_phone_number(raw), (True, expected))

    def test_subject_invalid_examples(self):
        for raw in ["+033 1 56 74 89 65", "33 5 89 74 12 22", "06 45 12 78", "", "abc"]:
            with self.subTest(raw=raw):
                self.assertEqual(phone.format_phone_number(raw), (False, None))

    def test_formatting_is_idempotent(self):
        _, value = phone.format_phone_number("+33 6 58 47 25 14")
        self.assertEqual(phone.format_phone_number(value), (True, value))

    def process(self, source, output, summary):
        with contextlib.redirect_stdout(io.StringIO()):
            return phone.process_file(source, output, summary)

    def test_reference_data_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "nested/output.txt"
            summary = Path(tmp) / "summary.json"
            result = self.process(TP1 / "data/liste_numeros.txt", out, summary)
            self.assertEqual((result["entries"], result["valid"], result["invalid"]), (67, 63, 4))
            self.assertEqual(result["duplicate_group_sizes"], [2, 3])
            self.assertEqual(len(out.read_text(encoding="utf-8").splitlines()), 63)
            self.assertEqual(json.loads(summary.read_text()), result)

    def test_empty_file_creates_empty_output_and_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "empty.txt"
            source.touch()
            output = Path(tmp) / "new/result.txt"
            summary = Path(tmp) / "new/summary.json"
            result = self.process(source, output, summary)
            self.assertEqual(output.read_bytes(), b"")
            self.assertEqual(result["entries"], 0)
            self.assertEqual(result["duplicate_groups"], 0)

    def test_blank_lines_are_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "input.txt"
            source.write_text("\n  \nÉmilie : 01 23 45 67 89\n", encoding="utf-8")
            self.assertEqual(phone.read_entries(source), [("Émilie", "01 23 45 67 89")])

    def test_malformed_lines_have_line_numbers(self):
        for bad in ["no separator", ": 01 23 45 67 89", "Name : 01,second column"]:
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / "input.txt"
                source.write_text("\n" + bad + "\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "Ligne 2"):
                    phone.read_entries(source)

    def test_paths_must_be_distinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "file.txt"
            source.write_text("Name : 01 23 45 67 89\n")
            before = source.read_bytes()
            with self.assertRaises(ValueError):
                self.process(source, source, Path(tmp) / "summary.json")
            self.assertEqual(source.read_bytes(), before)

    def test_cli_runs_from_arbitrary_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "nested/result.txt"
            result = run_cli(TP1 / "src/format_phone_numbers.py", "--output", output, cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(output.with_suffix(".summary.json").read_text())["valid"], 63)

    def test_cli_missing_input_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_cli(TP1 / "src/format_phone_numbers.py", "--input", Path(tmp) / "missing")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Erreur", result.stderr)
            self.assertEqual(result.stdout, "")

    def test_malformed_input_does_not_overwrite_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / "input", Path(tmp) / "output"
            source.write_text("broken line")
            output.write_text("previous result")
            result = run_cli(TP1 / "src/format_phone_numbers.py", "--input", source, "--output", output)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(), "previous result")
