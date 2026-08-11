#!/usr/bin/env python3
"""
Programme de décodage par substitution monoalphabétique.
Usage: python3 decodage.py <fichier_entree.txt> <mot_de_passe> <fichier_sortie.txt>
"""

import sys
import os

# Insertion du dossier src dans le chemin de recherche des modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from classes import Decodeur, PasswordError
except ImportError:
    from src.classes import Decodeur, PasswordError


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 decodage.py <fichier_entree.txt> <mot_de_passe> <fichier_sortie.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    password = sys.argv[2]
    output_file = sys.argv[3]

    try:
        decodeur = Decodeur(password)
        decodeur.decode_file(input_file, output_file)
    except PasswordError as e:
        print(f"Erreur : {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

