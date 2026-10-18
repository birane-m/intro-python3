import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from tests.helpers import ROOT, load_module

packaging = load_module("project_packaging", ROOT / "scripts/package_project.py")


class PackagingTests(unittest.TestCase):
    def test_archive_has_no_enclosing_folder_and_excludes_local_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            files = ["README.md", ".gitignore", ".github/workflows/tests.yml", "tests/test_one.py",
                     "tp1-filtage-spam/src/phone.py", "tp1-filtage-spam/output/old.txt",
                     ".git/HEAD", ".venv/private.py", "tp3-random-number-generator/data/setup.py",
                     "tp2-chiffrement-substitution/token.txt", "utilities/old.txt"]
            for name in files:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("example\n")
            destination = Path(tmp) / "project.zip"
            packaging.create_archive(destination, root)
            with zipfile.ZipFile(destination) as archive:
                self.assertEqual(set(archive.namelist()), {"README.md", ".gitignore", ".github/workflows/tests.yml",
                                                          "tests/test_one.py", "tp1-filtage-spam/src/phone.py"})
                self.assertIsNone(archive.testzip())

    def test_packaging_does_not_overwrite_source_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            readme = root / "README.md"
            readme.write_text("preserved")
            with self.assertRaises(ValueError):
                packaging.create_archive(readme, root)
            self.assertEqual(readme.read_text(), "preserved")


@unittest.skipUnless(importlib.util.find_spec("numpy") and importlib.util.find_spec("cv2"), "Dépendances images requises.")
class ExampleTests(unittest.TestCase):
    def test_examples_generate_index_parameters_and_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "examples"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/run_examples.py"), "--output", str(output)],
                                    cwd=tmp, text=True, capture_output=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / "index.md").is_file())
            for name in ["tp1", "tp2", "tp3", "tp4"]:
                self.assertTrue((output / name / "summary.json").is_file())
            self.assertEqual(json.loads((output / "tp1/summary.json").read_text())["valid"], 63)
            self.assertTrue(json.loads((output / "tp2/summary.json").read_text())["roundtrip_identical"])
            self.assertEqual(json.loads((output / "tp3/summary.json").read_text())["draw_count"], 10)
            self.assertTrue((output / "tp4/comparaison.png").is_file())
            self.assertTrue((output / "tp4/nombres.json").is_file())

    def test_examples_reject_source_directory_as_destination(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/run_examples.py"), "--output", str(ROOT / "tests")],
                                text=True, capture_output=True, timeout=10)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Choisir outputs/", result.stderr)
