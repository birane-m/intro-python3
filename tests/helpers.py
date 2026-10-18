"""Charge chaque TP isolément malgré leurs noms historiques de dossiers."""

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TP1 = ROOT / "tp1-filtage-spam"
TP2 = ROOT / "tp2-chiffrement-substitution"
TP3 = ROOT / "tp3-random-number-generator"
TP4 = ROOT / "tp4-nombres-premiers-et-images"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


phone = load_module("tp1_phone", TP1 / "src/format_phone_numbers.py")
cipher = load_module("tp2_cipher", TP2 / "src/classes.py")
dice = load_module("tp3_dice", TP3 / "src/classes.py")
prime = load_module("tp4_prime", TP4 / "src/classes.py")


def run_cli(script, *args, cwd=None):
    return subprocess.run([sys.executable, "-B", str(script), *map(str, args)],
                          cwd=cwd or ROOT, text=True, capture_output=True, timeout=30)
