"""
Script denfacetruque.py
-----------------------
Permet de générer des tirages aléatoires d'un dé truqué (De6facestruque ou DeNfacestruque).
Usage : python3 denfacetruque.py nb_face nb_tirages poids_face_1 poids_face_2 ... poids_derniere_face
"""

import sys
from classes import De6facestruque, DeNfacestruque


def main():
    # Vérification minimale d'arguments
    if len(sys.argv) < 3:
        sys.exit(1)

    try:
        nb_faces = int(sys.argv[1])
        nb_tirages = int(sys.argv[2])
        poids = [int(x) for x in sys.argv[3:]]
    except ValueError:
        sys.exit(1)

    # Instanciation de la classe de dé truqué
    if nb_faces == 6:
        mon_de = De6facestruque(poids=poids if poids else None)
    else:
        mon_de = DeNfacestruque(nb_faces, poids=poids if poids else None)

    # Tirage et affichage (une valeur par ligne)
    resultats = mon_de.tirer(nb_tirages)
    for res in resultats:
        print(res)

    sys.exit(0)


if __name__ == "__main__":
    main()