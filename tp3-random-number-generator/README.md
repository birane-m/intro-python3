# TP3 : Random Number Generator (RNG)

Ce projet implémente un système orienté objet en Python pour simuler des tirages aléatoires de dés (classiques, truqués, illustrés, pièces de monnaie, sacs de billes sans remise) et des paquets de dés.

## Architecture des classes (`src/classes.py`)

- **`MyRandom`** : Classe abstraite de base (`abc.ABC`) encapsulant l'objet `random.Random`. Elle interdit l'instanciation directe via des méthodes abstraites (`__init__` et `tirer`). Elle prend également en charge l'opérateur d'addition `+`.
- **`DeNfacestruque`** : Dé à $N$ faces truqué acceptant une liste de poids. Si aucun poids n'est fourni, les faces sont équiprobables. Lève `PoidsInvalidesError` si le nombre de poids est incorrect.
- **`De6facestruque`** : Dé truqué à 6 faces héritant de `DeNfacestruque`.
- **`DeNfaces`** : Dé équilibré à $N$ faces héritant de `DeNfacestruque` avec des poids équiprobables.
- **`De6faces`** : Dé équilibré à 6 faces héritant de `DeNfaces`.
- **`PaquetDe`** : Conteneur autonome de dés (`MyRandom`). 
  - Surcharges de l'opérateur `+` (`paquet + de`, `de + paquet`, `paquet1 + paquet2`) utilisant `copy.deepcopy` pour éviter toute dépendance de référence directe.
  - Méthode `tirer(nb_tirs)` renvoyant la liste des tirages transposée par lancer (`zip`).
- **`DeNfacesIllustrees`** : Dé non truqué associant des étiquettes ou objets à chaque face (ex: `"rouge"`, `"bleu"`, `"vert"`).
- **`Piece`** : Pièce de monnaie héritant de `DeNfacesIllustrees` (`"pile"` ou `"face"`).
- **`SacNBillesSansRemise`** : Sac de $N$ billes numérotées de 1 à $N$. Les billes sont tirées sans remise et le sac se recharge automatiquement lorsqu'il est vide.

---

## Programmes exécutables (`src/`)

### 1. Dé classique (`denface.py`)
Génère `nb_tirages` tirages pour un dé à `nb_face` faces.
```bash
python3 src/denface.py <nb_face> <nb_tirages>
```
*Exemple :*
```bash
python3 src/denface.py 9 3
```

### 2. Dé truqué (`denfacetruque.py`)
Génère `nb_tirages` tirages pour un dé truqué avec les poids spécifiés.
```bash
python3 src/denfacetruque.py <nb_face> <nb_tirages> <poids_1> <poids_2> ... <poids_N>
```
*Exemple :*
```bash
python3 src/denfacetruque.py 6 8 1 2 1 2 1 2
```

### 3. Paquet de dés (`paquetde.py`)
Génère `nb_tirages` tirages pour un paquet composé des dés spécifiés par leur nombre de faces.
```bash
python3 src/paquetde.py <nb_tirages> <nb_face_de1> <nb_face_de2> ... <nb_face_deN>
```
*Exemple :*
```bash
python3 src/paquetde.py 5 6 6 9
```

---

## Exécution des tests

Le projet inclut une suite de tests automatisés couvrant l'ensemble des fonctionnalités et classes (1.1 à 1.6).

Pour lancer les tests :
```bash
python3 src/test_tp3.py
```

---

## Format de rendu

Pour le rendu final du TP, compressez les fichiers Python du dossier `src/` (hors environnement virtuel) dans une archive nommée selon le format exigé :
```text
VotreNom_VotrePrenom_VotreNumeroEtudiant.zip
```
