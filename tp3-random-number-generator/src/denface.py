import sys
from classes import De6faces, DeNfaces

def main():
    # sys.argv[0] est le nom du script ('denface.py')
    # Les arguments suivants sont ceux tapés dans le terminal
    if len(sys.argv) != 3:
        # Sécurité : si on n'a pas exactement 2 arguments après le nom du script
        sys.exit(1)

    # Conversion des arguments du terminal (qui sont des chaînes de caractères) en entiers
    nb_faces = int(sys.argv[1])
    nb_tirages = int(sys.argv[2])

    # Construction du dé demandé
    if nb_faces == 6:
        mon_de = De6faces()
    else:
        mon_de = DeNfaces(nb_faces)

    # Tirage et affichage strictement conforme à JARVIS (un résultat par ligne)
    resultats = mon_de.tirer(nb_tirages)
    for res in resultats:
        print(res)

    # Code de retour 0 exigé par l'énoncé
    sys.exit(0)

if __name__ == "__main__":
    main()