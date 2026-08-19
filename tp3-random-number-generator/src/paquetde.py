"""
Script paquetde.py
------------------
Permet de générer des ensembles de tirages aléatoires à l'aide d'un paquet de dés non truqués.
Usage : python3 paquetde.py nb_tirages nb_face_de1 nb_face_de2 ... nb_face_dernier_de
"""

import sys
from classes import De6faces, DeNfaces, PaquetDe


def main():
    # Vérification minimale des arguments (au moins script + nb_tirages + 1 dé)
    if len(sys.argv) < 3:
        sys.exit(1)

    try:
        nb_tirages = int(sys.argv[1])
        faces_des = [int(x) for x in sys.argv[2:]]
    except ValueError:
        sys.exit(1)

    # Construction des dés selon le nombre de faces spécifié
    liste_des = []
    for face in faces_des:
        if face == 6:
            liste_des.append(De6faces())
        else:
            liste_des.append(DeNfaces(face))

    # Création du paquet de dés
    paquet = PaquetDe(*liste_des)

    # Lancer global
    resultats = paquet.tirer(nb_tirages)

    # Affichage des résultats (un lancer par ligne, valeurs séparées par un espace)
    for tirage in resultats:
        print(" ".join(map(str, tirage)))

    sys.exit(0)


if __name__ == "__main__":
    main()