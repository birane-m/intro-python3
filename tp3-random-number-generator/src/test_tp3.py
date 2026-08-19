"""
Script test_tp3.py
------------------
Script de test complet pour valider toutes les classes du TP3, 
notamment les nouvelles classes de la section 1.6 :
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
    print(" 🧪 TEST DES CLASSES DE LA SECTION 1.6")
    print("=" * 60)

    # 1. Test de DeNfacesIllustrees
    print("\n1. Test de DeNfacesIllustrees ('rouge', 'bleu', 'vert') :")
    de_couleurs = DeNfacesIllustrees("rouge", "bleu", "vert", seed=42)
    tirages_couleurs = de_couleurs.tirer(6)
    print(f"   ► 6 tirages effectués : {tirages_couleurs}")
    for res in tirages_couleurs:
        assert res in ["rouge", "bleu", "vert"], f"Résultat invalide : {res}"
    print("   ✅ Test DeNfacesIllustrees RÉUSSI")

    # 2. Test de Piece
    print("\n2. Test de Piece (Pile ou Face) :")
    piece = Piece(seed=42)
    tirages_piece = piece.tirer(10)
    print(f"   ► 10 lancers de pièce : {tirages_piece}")
    for res in tirages_piece:
        assert res in ["pile", "face"], f"Résultat invalide : {res}"
    print("   ✅ Test Piece RÉUSSI")

    # 3. Test de SacNBillesSansRemise
    print("\n3. Test de SacNBillesSansRemise (3 billes) :")
    sac = SacNBillesSansRemise(3, seed=123)
    premier_cycle = sac.tirer(3)
    print(f"   ► 1er cycle de 3 tirages (sans remise) : {premier_cycle}")
    # Dans un cycle de 3 billes (1 à 3), chaque bille doit apparaître exactement une fois
    assert sorted(premier_cycle) == [1, 2, 3], f"Les billes ne sont pas toutes uniques dans le cycle : {premier_cycle}"

    deuxieme_cycle = sac.tirer(3)
    print(f"   ► 2ème cycle de 3 tirages (rechargement auto) : {deuxieme_cycle}")
    assert sorted(deuxieme_cycle) == [1, 2, 3], f"Le rechargement du sac a échoué : {deuxieme_cycle}"
    print("   ✅ Test SacNBillesSansRemise RÉUSSI")


def tester_classes_sections_1_1_a_1_5():
    print("\n" + "=" * 60)
    print(" 🧪 TEST DES CLASSES DES SECTIONS 1.1 À 1.5")
    print("=" * 60)

    # Test classe abstraite MyRandom
    print("\n1. Test d'interdiction d'instanciation de MyRandom :")
    try:
        instance = MyRandom()
        print("   ❌ ÉCHEC : MyRandom a pu être instancié !")
    except TypeError as e:
        print(f"   ✅ RÉUSSI : Impossible d'instancier MyRandom ({e})")

    # Test De6faces et DeNfaces
    print("\n2. Test De6faces & DeNfaces :")
    d6 = De6faces(seed=1)
    d9 = DeNfaces(9, seed=1)
    print(f"   ► De6faces (3 tirs) : {d6.tirer(3)}")
    print(f"   ► DeNfaces(9) (3 tirs) : {d9.tirer(3)}")

    # Test DeNfacestruque et exception de poids
    print("\n3. Test DeNfacestruque & Exception :")
    dt = DeNfacestruque(4, [1, 5, 1, 1], seed=10)
    print(f"   ► Dé à 4 faces truqué (favorise la face 2) : {dt.tirer(8)}")
    try:
        DeNfacestruque(4, [1, 2])
    except PoidsInvalidesError as e:
        print(f"   ✅ RÉUSSI : Exception levée pour poids invalides ({e})")

    # Test PaquetDe & Addition
    print("\n4. Test PaquetDe et surcharges d'opérateurs (+) :")
    de1 = De6faces()
    de2 = DeNfacestruque(4, [2, 3, 1, 3])
    de3 = DeNfaces(8)
    de4 = DeNfaces(12)

    paquet1 = PaquetDe(de1, de2, de3)
    paquet2 = paquet1 + de4
    paquet3 = de4 + paquet1

    print(f"   ► Paquet original (3 dés) : nb dés = {len(paquet1.list_de)}")
    print(f"   ► paquet1 + de4 : nb dés = {len(paquet2.list_de)}, dé4 en dernier = {isinstance(paquet2.list_de[-1], DeNfaces) and paquet2.list_de[-1].nb_faces == 12}")
    print(f"   ► de4 + paquet1 : nb dés = {len(paquet3.list_de)}, dé4 en premier = {isinstance(paquet3.list_de[0], DeNfaces) and paquet3.list_de[0].nb_faces == 12}")

    # Indépendance (deepcopy)
    assert paquet2.list_de[3] is not de4, "Échec : dépendance directe détectée au lieu d'une copie profonde !"
    print("   ✅ Test d'indépendance des objets (deepcopy) RÉUSSI")

    # Lancer global du paquet
    res_paquet = paquet1.tirer(4)
    print(f"   ► Lancer global du paquet (4 tirages pour 3 dés) : {res_paquet}")


if __name__ == "__main__":
    tester_classes_section_1_6()
    tester_classes_sections_1_1_a_1_5()
    print("\n" + "=" * 60)
    print(" 🎉 TOUS LES TESTS SE SONT ÉCOULÉS AVEC SUCCÈS !")
    print("=" * 60)
