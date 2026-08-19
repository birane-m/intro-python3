"""
Script test_tp3.py
------------------
Script de test complet pour valider toutes les classes du TP3 :
- DeNfacesIllustrees
- Piece
- SacNBillesSansRemise
- PaquetDe et ses surcharges d'opérateurs
"""

import sys
from classes import (
    MyRandom,
    De6faces,
    DeNfaces,
    DeNfacestruque,
    De6facestruque,
    PaquetDe,
    DeNfacesIllustrees,
    Piece,
    SacNBillesSansRemise,
    PoidsInvalidesError
)


def tester_classes_section_1_6():
    print("=" * 60)
    print(" TEST DES CLASSES DE LA SECTION 1.6")
    print("=" * 60)

    # 1. Test de DeNfacesIllustrees
    print("\n1. Test de DeNfacesIllustrees ('rouge', 'bleu', 'vert') :")
    de_couleurs = DeNfacesIllustrees("rouge", "bleu", "vert", seed=42)
    tirages_couleurs = de_couleurs.tirer(6)
    print(f"   -> 6 tirages effectues : {tirages_couleurs}")
    for res in tirages_couleurs:
        assert res in ["rouge", "bleu", "vert"], f"Resultat invalide : {res}"
    print("   [OK] Test DeNfacesIllustrees REUSSI")

    # 2. Test de Piece
    print("\n2. Test de Piece (Pile ou Face) :")
    piece = Piece(seed=42)
    tirages_piece = piece.tirer(10)
    print(f"   -> 10 lancers de piece : {tirages_piece}")
    for res in tirages_piece:
        assert res in ["pile", "face"], f"Resultat invalide : {res}"
    print("   [OK] Test Piece REUSSI")

    # 3. Test de SacNBillesSansRemise
    print("\n3. Test de SacNBillesSansRemise (3 billes) :")
    sac = SacNBillesSansRemise(3, seed=123)
    premier_cycle = sac.tirer(3)
    print(f"   -> 1er cycle de 3 tirages (sans remise) : {premier_cycle}")
    assert sorted(premier_cycle) == [1, 2, 3], f"Les billes ne sont pas toutes uniques dans le cycle : {premier_cycle}"

    deuxieme_cycle = sac.tirer(3)
    print(f"   -> 2eme cycle de 3 tirages (rechargement auto) : {deuxieme_cycle}")
    assert sorted(deuxieme_cycle) == [1, 2, 3], f"Le rechargement du sac a echoue : {deuxieme_cycle}"
    print("   [OK] Test SacNBillesSansRemise REUSSI")


def tester_classes_sections_1_1_a_1_5():
    print("\n" + "=" * 60)
    print(" TEST DES CLASSES DES SECTIONS 1.1 A 1.5")
    print("=" * 60)

    # Test classe abstraite MyRandom
    print("\n1. Test d'interdiction d'instanciation de MyRandom :")
    try:
        instance = MyRandom()
        print("   [ECHEC] MyRandom a pu etre instancie !")
    except TypeError as e:
        print(f"   [OK] Impossible d'instancier MyRandom ({e})")

    # Test De6faces et DeNfaces
    print("\n2. Test De6faces & DeNfaces :")
    d6 = De6faces(seed=1)
    d9 = DeNfaces(9, seed=1)
    print(f"   -> De6faces (3 tirs) : {d6.tirer(3)}")
    print(f"   -> DeNfaces(9) (3 tirs) : {d9.tirer(3)}")

    # Test DeNfacestruque et exception de poids
    print("\n3. Test DeNfacestruque & Exception :")
    dt = DeNfacestruque(4, [1, 5, 1, 1], seed=10)
    print(f"   -> De a 4 faces truque (favorise la face 2) : {dt.tirer(8)}")
    try:
        DeNfacestruque(4, [1, 2])
    except PoidsInvalidesError as e:
        print(f"   [OK] Exception levee pour poids invalides ({e})")

    # Test PaquetDe & Addition
    print("\n4. Test PaquetDe et surcharges d'operateurs (+) :")
    de1 = De6faces()
    de2 = DeNfacestruque(4, [2, 3, 1, 3])
    de3 = DeNfaces(8)
    de4 = DeNfaces(12)

    paquet1 = PaquetDe(de1, de2, de3)
    paquet2 = paquet1 + de4
    paquet3 = de4 + paquet1

    print(f"   -> Paquet original (3 des) : nb des = {len(paquet1.list_de)}")
    print(f"   -> paquet1 + de4 : nb des = {len(paquet2.list_de)}, de4 en dernier = {isinstance(paquet2.list_de[-1], DeNfaces) and paquet2.list_de[-1].nb_faces == 12}")
    print(f"   -> de4 + paquet1 : nb des = {len(paquet3.list_de)}, de4 en premier = {isinstance(paquet3.list_de[0], DeNfaces) and paquet3.list_de[0].nb_faces == 12}")

    # Independance (deepcopy)
    assert paquet2.list_de[3] is not de4, "Echec : dependance directe detectee au lieu d'une copie profonde !"
    print("   [OK] Test d'independance des objets (deepcopy) REUSSI")

    # Lancer global du paquet
    res_paquet = paquet1.tirer(4)
    print(f"   -> Lancer global du paquet (4 tirages pour 3 des) : {res_paquet}")


if __name__ == "__main__":
    tester_classes_section_1_6()
    tester_classes_sections_1_1_a_1_5()
    print("\n" + "=" * 60)
    print(" TOUS LES TESTS SE SONT ECOULES AVEC SUCCES !")
    print("=" * 60)
