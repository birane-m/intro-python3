# TP4 — Nombres premiers et images

Deux parties indépendantes : préparer les nombres premiers avec un crible d’Ératosthène, puis manipuler des images comme des tableaux NumPy.

[Énoncé](docs/TP4.pdf) · [Installation commune](../README.md#installation)

## Nombres premiers

`NbPremier(n)` prépare les valeurs de 0 à `n`, bornes incluses. Le crible utilise le slicing et ne barre les multiples qu’avec les facteurs au plus égaux à la racine carrée de `n`.

| Méthode | Résultat |
| --- | --- |
| `est_nombre_premier(k)` | Booléen ; `False` si `k < 2`, exception si `k > n` |
| `decomposition_factors(k)` | Liste triée des facteurs premiers, pour `2 <= k <= n` |
| `decomposition(k)` | Affiche le format strict du sujet, par exemple `68=2*2*17` |
| `goldbach_pairs()` | Dictionnaire d’un couple de premiers pour chaque pair de 4 à `n` |
| `test_goldbach()` | Affiche les égalités au format du sujet |

Depuis le dossier du TP4 :

```bash
python src/goldbach.py 10
python src/decomposition.py 68
```

La première commande affiche :

```text
4=2+2
6=3+3
8=3+5
10=3+7
```

Tester Goldbach jusqu’à une borne finie ne prouve pas la conjecture. La mémoire du crible croît avec la borne ; ce code n’a pas vocation à traiter des entiers arbitrairement grands.

## Images

Installer les dépendances dans un environnement virtuel activé :

```bash
python -m pip install -r requirements.txt
```

Le fichier de dépendances à la racine du dépôt renvoie vers celui-ci ; les deux procédures installent les mêmes bibliothèques.

```bash
python nb.py data/chien.jpg output/chien_gris.png
python src/PremierContactNumpy.py
```

`PremierContactNumpy.py` illustre le broadcasting et affiche les dimensions, le type des pixels et les canaux d’une image, sans ouvrir de fenêtre graphique.

La classe `Image` propose :

| Méthode | Comportement |
| --- | --- |
| `to_gray()` | Moyenne des trois canaux puis conversion en `uint8` ; une image déjà grise reste identique |
| `add_black_stripes(n)` | Une ligne noire tous les `n` pixels, à partir de la première |
| `compute_contours(k)` | Différence max-min dans le carré de rayon `k`, bordure à zéro |
| `save(path)` | Crée les dossiers parents et sauvegarde l’image |
| `Image.from_array(array)` | Construit une image depuis une copie d’un tableau `uint8` |
| `show_im()` | Ouvre une fenêtre ; réservé à un environnement graphique |

Il s’agit de **niveaux de gris**, pas d’une binarisation noir/blanc. La moyenne suit le sujet ; elle n’utilise pas les pondérations perceptuelles d’une conversion standard. Les contours attendent une image grise et un rayon entier positif ou nul. Un voisinage trop grand laisse une image entièrement nulle.

Depuis ce dossier :

```python
from src.classes import Image

image = Image("data/chien.jpg")
image.to_gray()
image.compute_contours(1)
image.save("output/contours.png")
```

PNG préserve exactement les pixels ; JPEG applique une compression avec pertes. Le calcul des contours reste à boucles explicites et peut être lent pour de grandes images.

## Démonstration et tests

Depuis la racine du dépôt :

```bash
python scripts/run_examples.py
python -m unittest tests.test_tp4 tests.test_images -v
```

`outputs/index.md` donne accès à la comparaison de l’original, des niveaux de gris, des bandes et des contours. Chaque traitement part séparément de la même image source.

Les tests numériques confrontent le crible à une division d’essai indépendante, reconstruisent les entiers à partir de leurs facteurs et contrôlent les couples de Goldbach. Les tests d’images vérifient les pixels, les bordures, les erreurs et la lecture/écriture de PNG, sans fenêtre graphique.
