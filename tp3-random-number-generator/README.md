# TP3 - Random Number Generator

Projet Python orienté objet permettant de simuler plusieurs générateurs aléatoires: dés équilibrés, dés truqués, dés illustrés, pièce de monnaie, sac de billes sans remise et paquets de dés.

## Problème

Le TP demande de modéliser différents objets capables de produire des tirages aléatoires, tout en évitant la duplication de code.

Il faut gérer plusieurs cas:
1. un dé classique à `N` faces ;
2. un dé truqué avec des probabilités pondérées ;
3. un paquet regroupant plusieurs dés ;
4. des objets plus spécialisés, comme une pièce ou un sac de billes tirées sans remise.

## Solution proposée

La solution repose sur une hiérarchie de classes dans `src/classes.py`.

`MyRandom` définit l'interface commune avec la méthode abstraite `tirer()`.

`DeNfacestruque` gère les tirages pondérés grâce à `random.choices`. Les dés équilibrés héritent de cette classe en utilisant des poids identiques pour toutes les faces.

`PaquetDe` regroupe plusieurs dés et surcharge l'opérateur `+` pour permettre des combinaisons naturelles comme `de1 + de2` ou `paquet + de`.

`DeNfacesIllustrees`, `Piece` et `SacNBillesSansRemise` étendent le modèle pour gérer des faces nommées ou des tirages sans remise.

Exemple d'utilisation directe:

```python
from classes import De6faces, DeNfaces, PaquetDe

de = De6faces(seed=1)
print(de.tirer(5))

paquet = PaquetDe(De6faces(seed=1), DeNfaces(4, seed=2))
print(paquet.tirer(3))
```

Sortie:

```text
[1, 6, 5, 2, 3]
[(1, 4), (6, 4), (5, 1)]
```

## Exemples de tests

Depuis le dossier du TP3, lancer la suite de tests:

```bash
python3 src/test_tp3.py
```

Tester un dé classique:

```bash
python3 src/denface.py 6 5
```

Tester un dé truqué à 4 faces:

```bash
python3 src/denfacetruque.py 4 10 1 5 1 1
```

Tester un paquet de dés:

```bash
python3 src/paquetde.py 5 6 8 12
```

Vérifier la syntaxe Python:

```bash
python3 -m py_compile src/classes.py src/denface.py src/denfacetruque.py src/paquetde.py src/test_tp3.py
```

## Exécution

Cloner le dépôt:

```bash
git clone https://github.com/birane-m/intro-python3.git
```

Se placer dans le dossier du TP3:

```bash
cd intro-python3/tp3-random-number-generator
```

Lancer un dé classique:

```bash
python3 src/denface.py <nb_faces> <nb_tirages>
```

Lancer un dé truqué:

```bash
python3 src/denfacetruque.py <nb_faces> <nb_tirages> <poids_1> ... <poids_N>
```

Lancer un paquet de dés:

```bash
python3 src/paquetde.py <nb_tirages> <faces_de1> <faces_de2> ...
```

Prérequis: Python 3. Aucune dépendance externe n'est nécessaire pour les scripts du TP.

## Structure

```text
tp3-random-number-generator/
├── README.md
├── docs/
│   └── TP3.pdf
└── src/
    ├── classes.py
    ├── denface.py
    ├── denfacetruque.py
    ├── paquetde.py
    └── test_tp3.py
```
