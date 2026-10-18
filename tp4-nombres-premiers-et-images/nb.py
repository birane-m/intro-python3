#!/usr/bin/env python3
"""Convertit une image couleur en niveaux de gris par moyenne des canaux."""

import argparse
import sys
from pathlib import Path

from src.classes import Image


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", type=Path)
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.input_file.resolve() == args.output_file.resolve():
            raise ValueError("La sortie doit être différente de l'image originale.")
        image = Image(args.input_file)
        image.to_gray()
        image.save(args.output_file)
    except ImportError:
        print("Erreur : installer les dépendances du TP4 (voir requirements.txt).", file=sys.stderr)
        return 1
    except (OSError, ValueError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
