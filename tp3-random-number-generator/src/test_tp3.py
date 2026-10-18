"""Point d'entrée historique : exécute les vrais tests automatisés du TP3."""

import subprocess
import sys
from pathlib import Path


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    raise SystemExit(subprocess.call([sys.executable, "-m", "unittest", "tests.test_tp3", "-v"], cwd=root))
