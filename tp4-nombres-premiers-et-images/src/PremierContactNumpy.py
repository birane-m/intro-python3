"""Exploration reproductible de tableaux NumPy et d'une image OpenCV."""

import argparse
import sys
from pathlib import Path

from classes import Image


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", nargs="?", type=Path,
                        default=Path(__file__).resolve().parents[1] / "data/chien.jpg")
    args = parser.parse_args(argv)
    try:
        import numpy as np
        rng = np.random.default_rng(0)
        first = rng.integers(0, 10, (3, 1))
        second = rng.integers(0, 10, (1, 4))
        image = Image(args.image)
    except ImportError:
        print("Erreur : installer les dépendances du TP4.", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    print("Broadcasting :", first.shape, "*", second.shape)
    print(first * second)
    print("Image :", image.im.shape, "dtype :", image.im.dtype)
    print("Premier pixel (B, G, R) :", image.im[0, 0].tolist())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
