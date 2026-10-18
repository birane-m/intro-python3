"""Arguments et erreurs des deux commandes numériques du TP4."""

import argparse
import sys

from classes import NbPremier


def main(method, argv=None):
    parser = argparse.ArgumentParser(description=f"TP4 : {method}.")
    parser.add_argument("N", type=int)
    args = parser.parse_args(argv)
    try:
        numbers = NbPremier(args.N)
        if method == "goldbach":
            numbers.test_goldbach()
        else:
            numbers.decomposition(args.N)
    except (TypeError, ValueError, RuntimeError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    return 0
