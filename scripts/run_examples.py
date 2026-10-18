"""Exécute des exemples reproductibles et crée leur index dans outputs/."""

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(script, *args):
    result = subprocess.run([sys.executable, str(ROOT / script), *map(str, args)],
                            cwd=ROOT, check=True, capture_output=True, text=True, timeout=60)
    return result.stdout


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_examples(output):
    import cv2
    import numpy as np

    output = Path(output)
    # Le répertoire contient des noms fixes : relancer met à jour ces seuls exemples.
    for name in ["tp1", "tp2", "tp3", "tp4"]:
        (output / name).mkdir(parents=True, exist_ok=True)
    transcript = run("tp1-filtage-spam/src/format_phone_numbers.py",
                     "--output", output / "tp1/numeros.txt", "--summary", output / "tp1/summary.json")
    (output / "tp1/console.txt").write_text(transcript, encoding="utf-8")

    key = "zyxwvutsrqponmlkjihgfedcba"
    source = ROOT / "tp2-chiffrement-substitution/data/test_encoding.txt"
    encoded, decoded = output / "tp2/encoded.txt", output / "tp2/decoded.txt"
    run("tp2-chiffrement-substitution/encodage.py", source, key, encoded)
    run("tp2-chiffrement-substitution/decodage.py", encoded, key, decoded)
    if decoded.read_bytes() != source.read_bytes():
        raise RuntimeError("L'aller-retour de chiffrement a modifié le fichier source.")
    write_json(output / "tp2/summary.json", {"example": "roundtrip", "encryption_key": key,
                                            "roundtrip_identical": True})

    rolls = run("tp3-random-number-generator/src/paquetde.py", 10, 6, 8, 12, "--seed", 42)
    (output / "tp3/tirages.txt").write_text(rolls, encoding="utf-8")
    write_json(output / "tp3/summary.json", {"seed": 42, "faces": [6, 8, 12], "draw_count": 10,
                                            "draws": [[int(x) for x in line.split()] for line in rolls.splitlines()]})

    tp4 = load_module("example_images", ROOT / "tp4-nombres-premiers-et-images/src/classes.py")
    numbers = tp4.NbPremier(100)
    write_json(output / "tp4/nombres.json", {"limit": 100, "primes": numbers.lprime,
                                           "factors_68": numbers.decomposition_factors(68),
                                           "goldbach": numbers.goldbach_pairs()})
    original = tp4.Image(ROOT / "tp4-nombres-premiers-et-images/data/chien.jpg")
    gray = tp4.Image.from_array(original.im)
    gray.to_gray()
    gray.save(output / "tp4/gris.png")
    stripes = tp4.Image.from_array(gray.im)
    stripes.add_black_stripes(12)
    stripes.save(output / "tp4/bandes.png")
    contours = tp4.Image.from_array(gray.im)
    contours.compute_contours(1)
    contours.save(output / "tp4/contours.png")

    # Chaque panneau part de la même image ; bandes et contours ne sont pas cumulés.
    panels = []
    for title, array in [("Image originale", original.im), ("Moyenne des canaux", gray.im),
                         ("Bandes : une ligne / 12", stripes.im), ("Contours max-min : k=1", contours.im)]:
        if array.ndim == 2:
            array = cv2.cvtColor(array, cv2.COLOR_GRAY2BGR)
        width = 480
        height = round(array.shape[0] * width / array.shape[1])
        resized = cv2.resize(array, (width, height), interpolation=cv2.INTER_AREA)
        label = np.full((44, width, 3), 245, dtype=np.uint8)
        cv2.putText(label, title, (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (35, 35, 35), 1, cv2.LINE_AA)
        panels.append(np.vstack((label, resized)))
    comparison = np.vstack((np.hstack(panels[:2]), np.hstack(panels[2:])))
    tp4.Image.from_array(comparison).save(output / "tp4/comparaison.png")
    write_json(output / "tp4/summary.json", {"source": "tp4-nombres-premiers-et-images/data/chien.jpg",
                                            "shape": list(original.im.shape), "grayscale": "mean_channels",
                                            "stripe_step": 12, "contour_radius": 1, "contour_border": 0})

    index = """# Exemples d'exécution Python 3

Ces fichiers sont régénérés par `python3 scripts/run_examples.py`.
Relancer la commande remplace les exemples de mêmes noms.

| TP | Résultat | Bilan et paramètres |
| --- | --- | --- |
| TP1 | [Numéros filtrés](tp1/numeros.txt) · [Console](tp1/console.txt) | [Résumé JSON](tp1/summary.json) |
| TP2 | [Texte chiffré](tp2/encoded.txt) · [Texte déchiffré](tp2/decoded.txt) | [Vérification de l'aller-retour](tp2/summary.json) |
| TP3 | [Tirages du paquet](tp3/tirages.txt) | [Graine, faces et tirages](tp3/summary.json) |
| TP4 | [Nombres premiers et décompositions](tp4/nombres.json) | [Paramètres images](tp4/summary.json) |

## Traitements d'images du TP4

Chaque traitement est appliqué séparément à la même image source.
Les contours restent à leur intensité d'origine, sans amplification visuelle.

![Original, niveaux de gris, bandes et contours](tp4/comparaison.png)

Fichiers individuels : [gris](tp4/gris.png), [bandes](tp4/bandes.png), [contours](tp4/contours.png).
"""
    (output / "index.md").write_text(index, encoding="utf-8")
    return output / "index.md"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs")
    args = parser.parse_args(argv)
    output = args.output.resolve()
    # Les fichiers de sortie doivent rester séparés du code et des données fournis.
    protected = [ROOT / name for name in ["tests", "scripts", "docs", ".github", ".git", ".venv", "venv"]]
    protected += list(ROOT.glob("tp*-*"))
    if output == ROOT or any(output == p or p in output.parents for p in protected):
        parser.error("Choisir outputs/ ou un dossier extérieur aux sources et aux données.")
    try:
        index = build_examples(output)
    except ImportError:
        print("Erreur : installer les dépendances images avec python -m pip install -r requirements.txt.", file=sys.stderr)
        return 1
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    print(f"Exemples disponibles : {index}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
