#!/usr/bin/env python3
"""
Programme de conversion d'une image couleur en noir et blanc.

Usage:
    python3 nb.py entree.jpg sortie.jpg
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from classes import Image


def main():
    """
    Lit une image, la convertit en noir et blanc, puis sauvegarde le resultat.
    """
    if len(sys.argv) != 3:
        print("Usage: python3 nb.py entree.jpg sortie.jpg")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    output_dir = os.path.dirname(output_file)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    image = Image(input_file)
    image.to_gray()
    image.save(output_file)


if __name__ == "__main__":
    main()
