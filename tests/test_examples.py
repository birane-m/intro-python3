import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import ROOT

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
