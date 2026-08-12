import sys
from classes import De6facestruque, DeNfacestruque

def main():
    if len(sys.argv) < 3:
        sys.exit(1)

    nb_faces = int(sys.argv[1])
    nb_tirages = int(sys.argv[2])
    
    # On récupère tous les arguments à partir de l'index 3 comme étant les poids
    # On utilise une compréhension de liste pour tout convertir en entier d'un coup
    poids = [int(x) for x in sys.argv[3:]]

    # Construction du dé truqué demandé
    if nb_faces == 6:
        mon_de = De6facestruque(poids=poids)
    else:
        mon_de = DeNfacestruque(nb_faces, poids=poids)

    # Tirage et affichage
    resultats = mon_de.tirer(nb_tirages)
    for res in resultats:
        print(res)

    sys.exit(0)

if __name__ == "__main__":
    main()