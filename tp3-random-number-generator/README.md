# TP3 — Générateurs aléatoires

Modéliser des dés équilibrés et pondérés, des faces illustrées, une pièce, un sac de billes sans remise et des paquets de dés.

[Énoncé](docs/TP3.pdf) · [Installation commune](../README.md#installation)

## Conception

`MyRandom` impose un constructeur et une méthode `tirer()` abstraits. Chaque générateur possède son propre `random.Random`. `DeNfacestruque` réalise les tirages pondérés ; les dés équilibrés réutilisent ce comportement avec des poids égaux.

`PaquetDe` contient des générateurs plutôt que d’hériter de `MyRandom`. Les tirages sont regroupés par lancer avec `zip`. `DeNfacesIllustrees`, `Piece` et `SacNBillesSansRemise` complètent le modèle.

## Commandes

Depuis le dossier du TP3 :

```bash
python src/denface.py 6 5
python src/denfacetruque.py 4 10 1 5 1 1
python src/paquetde.py 5 6 8 12
```

L’option facultative `--seed` permet de reproduire une expérience :

```bash
python src/paquetde.py 5 6 8 12 --seed 42
```

Les commandes affichent uniquement les résultats, comme demandé dans l’énoncé : une valeur par ligne pour un dé, un lancer par ligne pour un paquet. Les erreurs vont sur `stderr` et renvoient un code non nul.

## Contrats des classes

| Paramètre | Règle |
| --- | --- |
| Nombre de faces ou de billes | Entier strictement positif |
| Nombre de tirages | Entier positif ou nul ; zéro donne une liste vide |
| Poids | Un poids fini et non négatif par face, avec une somme strictement positive |
| Faces illustrées | Au moins un élément |
| Contenu d’un paquet | Instances de `MyRandom` uniquement |

Les poids décimaux et les faces de poids nul sont autorisés. Sans poids explicites, le dé est équilibré. Un sac se recharge uniquement après épuisement de son contenu ; chaque cycle complet contient toutes ses billes une seule fois.

## Utilisation et copies

Depuis le dossier du TP3 :

```python
from src.classes import De6faces, DeNfaces, PaquetDe

de = De6faces(seed=1)
print(de.tirer(5))

paquet = PaquetDe(De6faces(seed=1), DeNfaces(4, seed=2))
print(paquet.tirer(3))
```

Le constructeur `PaquetDe(de1, de2)` conserve les objets transmis. Toutes les additions (`dé + dé`, `paquet + dé`, `dé + paquet`, `paquet + paquet`) créent de nouveaux objets et des copies profondes des dés. Tirer dans le paquet résultant n’avance donc pas les générateurs des opérandes.

Une copie profonde copie aussi l’état aléatoire. Deux dés copiés depuis le même état peuvent donner les mêmes suites : indépendance des objets en mémoire et indépendance statistique sont deux notions différentes. Pour des dés créés séparément, éviter de leur imposer tous la même graine. La commande des paquets dérive des graines distinctes d’une graine maître. Une même graine permet de reproduire les tirages dans un même environnement Python.

## Tests

Depuis la racine du dépôt :

```bash
python -m unittest tests.test_tp3 -v
```

Les tests couvrent les validations, les graines, les cycles du sac, la composition, les copies et les formats des commandes.

## Périmètre

Les générateurs utilisent `random.Random` et fonctionnent hors ligne. L’extension facultative de l’énoncé utilisant une source quantique distante n’est pas implémentée.
