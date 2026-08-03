#!/usr/bin/env python3
"""
Programme de cassage de code chiffré par substitution sans connaître le mot de passe.
Usage: python3 cassercode.py <fichier_entree.txt> <fichier_quadgram.txt> <fichier_sortie.txt>
"""

import sys
import os

# Insertion du dossier src dans le chemin de recherche des modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from classes import CodeBreaker
except ImportError:
    from src.classes import CodeBreaker


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 cassercode.py <fichier_entree.txt> <fichier_quadgram.txt> <fichier_sortie.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    quadgram_file = sys.argv[2]
    output_file = sys.argv[3]

    try:
        with open(input_file, 'r', encoding='utf-8') as f_in:
            crypted_content = f_in.read()
    except IOError:
        print(f"Cannot open file {input_file}")
        sys.exit(1)

    breaker = CodeBreaker(quadgram_file)
    found_pwd, decrypted_content = breaker.code_breaker(crypted_content)

    try:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write(decrypted_content)
    except IOError:
        print(f"Cannot open file {output_file}")
        sys.exit(1)


if __name__ == '__main__':
    main()
