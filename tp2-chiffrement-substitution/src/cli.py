"""Entrées en ligne de commande du TP2 ; les erreurs vont sur stderr."""

import argparse
import json
import sys
from pathlib import Path

from .classes import CodeBreaker, Decodeur, Encodeur


def main(method, argv=None):
    parser = argparse.ArgumentParser(description=f"TP2 : {method} par substitution.")
    parser.add_argument("input_file", type=Path)
    parser.add_argument("quadgrams" if method == "cassercode" else "password")
    parser.add_argument("output_file", type=Path)
    if method == "cassercode":
        parser.add_argument("--seed", type=int)
        parser.add_argument("--max-iterations", type=int)
        parser.add_argument("--summary", type=Path, help="Bilan JSON optionnel de la recherche.")
    args = parser.parse_args(argv)
    try:
        if args.input_file.resolve() == args.output_file.resolve():
            raise ValueError("Le fichier de sortie doit être différent du fichier d'entrée.")
        if method == "cassercode":
            protected = {args.input_file.resolve(), Path(args.quadgrams).resolve()}
            if args.output_file.resolve() in protected:
                raise ValueError("La sortie ne doit pas écraser les données d'entrée.")
            if args.summary and args.summary.resolve() in protected | {args.output_file.resolve()}:
                raise ValueError("Le bilan doit être un fichier distinct des entrées et de la sortie.")
            content = args.input_file.read_bytes().decode("utf-8")
            breaker = CodeBreaker(args.quadgrams, seed=args.seed)
            key, decoded = breaker.code_breaker(content, max_iterations=args.max_iterations)
            args.output_file.parent.mkdir(parents=True, exist_ok=True)
            args.output_file.write_bytes(decoded.encode("utf-8"))
            if args.summary:
                summary = {"input": str(args.input_file), "output": str(args.output_file),
                           "decryption_key": key, **breaker.last_search}
                args.summary.parent.mkdir(parents=True, exist_ok=True)
                args.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        elif method == "encodage":
            Encodeur(args.password).encode_file(args.input_file, args.output_file)
        else:
            Decodeur(args.password).decode_file(args.input_file, args.output_file)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    return 0
