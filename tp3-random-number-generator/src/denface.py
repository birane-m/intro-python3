"""
Script denface.py
-----------------
Permet de générer des tirages aléatoires d'un dé classique (De6faces ou DeNfaces).
Usage : python3 denface.py nb_face nb_tirages
"""

import sys
from classes import De6faces, DeNfaces


def main():
    # Vérification du nombre d'arguments
    if len(sys.argv) != 3:
        sys.exit(1)

    try:
        nb_faces = int(sys.argv[1])
        nb_tirages = int(sys.argv[2])
    except ValueError:
        sys.exit(1)

    # Instanciation de la bonne classe de dé
    if nb_faces == 6:
        mon_de = De6faces()
    else:
        mon_de = DeNfaces(nb_faces)

    # Tirage et affichage (une valeur par ligne)
    resultats = mon_de.tirer(nb_tirages)
    for res in resultats:
        print(res)

    sys.exit(0)


if __name__ == "__main__":
    main()