"""Commandes du TP3 : résultats seuls sur stdout, diagnostics sur stderr."""

import argparse
import sys
from random import Random

from classes import DeNfaces, DeNfacestruque, PaquetDe


def main(method, argv=None):
    parser = argparse.ArgumentParser(description=f"TP3 : {method}.")
    if method == "paquetde":
        parser.add_argument("nb_tirages", type=int)
        parser.add_argument("faces", type=int, nargs="+")
    else:
        parser.add_argument("nb_faces", type=int)
        parser.add_argument("nb_tirages", type=int)
        if method == "denfacetruque":
            parser.add_argument("poids", type=float, nargs="*")
    parser.add_argument("--seed", type=int, help="Graine optionnelle pour reproduire les tirages.")
    args = parser.parse_args(argv)
    try:
        if method == "paquetde":
            seeds = Random(args.seed)
            dice = [DeNfaces(faces, seed=seeds.getrandbits(128)) for faces in args.faces]
            generator = PaquetDe(*dice)
        elif method == "denfacetruque":
            generator = DeNfacestruque(args.nb_faces, args.poids or None, seed=args.seed)
        else:
            generator = DeNfaces(args.nb_faces, seed=args.seed)
        for result in generator.tirer(args.nb_tirages):
            print(" ".join(map(str, result)) if method == "paquetde" else result)
    except (TypeError, ValueError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    return 0
