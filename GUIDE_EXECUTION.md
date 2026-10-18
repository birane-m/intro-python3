# Guide d’exécution

Les commandes ci-dessous sont à lancer depuis la racine du dépôt, après l’installation décrite dans le [README](README.md). `python` désigne l’interpréteur de l’environnement virtuel activé.

## Commandes communes

| Action | Commande |
| --- | --- |
| Installer toutes les dépendances | `python -m pip install -r requirements.txt` |
| Tester le code sans les images | `python -m unittest discover -s tests -p 'test_tp*.py' -v` |
| Tester l’ensemble, images comprises | `make test` |
| Tester l’ensemble sans Make | `python -c "import numpy, cv2"`, puis `python -m unittest discover -s tests -v` |
| Produire les exemples et leur index | `python scripts/run_examples.py` |
| Préparer l’archive de sources | `python scripts/package_project.py` |

La suite utilise `unittest`, inclus dans Python. Elle n’appelle aucun service distant et n’ouvre aucune fenêtre graphique.

## TP1 — Filtrer les numéros

```bash
python tp1-filtage-spam/src/format_phone_numbers.py
```

Les fichiers par défaut sont `tp1-filtage-spam/data/liste_numeros.txt`, `tp1-filtage-spam/output/output.txt` et `tp1-filtage-spam/output/output.summary.json`.

Pour choisir les chemins :

```bash
python tp1-filtage-spam/src/format_phone_numbers.py \
  --input tp1-filtage-spam/data/liste_numeros.txt \
  --output outputs/tp1/numeros.txt \
  --summary outputs/tp1/summary.json
```

Les lignes vides sont ignorées. Une ligne qui ne suit pas le format `nom : numéro` provoque une erreur avant l’écriture des résultats. Les numéros invalides sont filtrés et leurs noms affichés. Le bilan JSON contient les effectifs et les tailles des groupes partageant un numéro.

## TP2 — Chiffrer et déchiffrer

La clé contient exactement une fois chaque lettre minuscule de `a` à `z`.

```bash
python tp2-chiffrement-substitution/encodage.py \
  tp2-chiffrement-substitution/data/test_encoding.txt \
  zyxwvutsrqponmlkjihgfedcba outputs/tp2/encoded.txt

python tp2-chiffrement-substitution/decodage.py \
  outputs/tp2/encoded.txt \
  zyxwvutsrqponmlkjihgfedcba outputs/tp2/decoded.txt
```

Pour rechercher une clé sans la connaître :

```bash
python tp2-chiffrement-substitution/cassercode.py \
  tp2-chiffrement-substitution/data/mystery_text.txt \
  tp2-chiffrement-substitution/data/english_quadgrams.txt \
  outputs/tp2/candidat.txt \
  --seed 42 --max-iterations 5000 --summary outputs/tp2/recherche.json
```

`--seed`, `--max-iterations` et `--summary` sont facultatifs. Sans limite globale, l’arrêt suit le sujet : 1000 permutations consécutives sans amélioration. Un budget d’itérations écoulé n’est pas un échec technique ; le fichier contient le meilleur candidat trouvé.

Le bilan enregistre la graine demandée, le nombre d’itérations, les scores initial et final, la cause d’arrêt et la **clé de déchiffrement**. Cette clé n’est pas directement la clé de chiffrement originale : elle représente la substitution inverse. Un score plus élevé n’assure pas un texte correctement déchiffré.

## TP3 — Effectuer des tirages

```bash
python tp3-random-number-generator/src/denface.py 6 5 --seed 1
python tp3-random-number-generator/src/denfacetruque.py 4 10 1 5 1 1 --seed 1
python tp3-random-number-generator/src/paquetde.py 5 6 8 12 --seed 1
```

Le nombre de faces est strictement positif, le nombre de tirages est positif ou nul. Les poids sont finis, non négatifs et leur somme est strictement positive ; ils peuvent être décimaux. Sans poids explicites, le dé est équilibré.

Une valeur est affichée par ligne pour un dé. Pour un paquet, une ligne représente un lancer de tous ses dés, séparés par des espaces. Pour conserver les tirages :

```bash
mkdir -p outputs/tp3
python tp3-random-number-generator/src/paquetde.py 5 6 8 12 --seed 1 > outputs/tp3/tirages.txt
```

Une même graine reproduit une expérience dans un même environnement. Pour les paquets en ligne de commande, un générateur maître produit une graine distincte pour chaque dé.

## TP4 — Calculer avec les nombres premiers

```bash
python tp4-nombres-premiers-et-images/src/goldbach.py 10
python tp4-nombres-premiers-et-images/src/decomposition.py 68
```

La limite du crible est un entier positif ou nul. La décomposition est définie ici pour les entiers au moins égaux à 2. Une requête de primalité négative renvoie `False`. Une valeur supérieure à la limite du crible déclenche `ParameterTooHighValue`.

## TP4 — Manipuler des images

```bash
python tp4-nombres-premiers-et-images/nb.py \
  tp4-nombres-premiers-et-images/data/chien.jpg outputs/tp4/gris.png

python tp4-nombres-premiers-et-images/src/PremierContactNumpy.py
```

`nb.py` crée les répertoires de sortie. Utiliser PNG pour conserver exactement les pixels produits ; JPEG peut modifier ces valeurs lors de la compression. Le script d’exploration affiche des tableaux et les propriétés d’une image sans ouvrir de fenêtre.

Les bandes et les contours sont accessibles par la classe `Image`, ou dans la démonstration commune :

```bash
python scripts/run_examples.py
```

La moyenne des canaux est calculée avant la conversion en `uint8` pour éviter les débordements. Les contours utilisent `maximum - minimum` sur un voisinage carré de rayon `k`, avec une bordure nulle. Le calcul à boucles reste pédagogique et peut être lent sur une grande image ou un grand rayon.

## Retrouver les résultats

La démonstration écrit les résultats et paramètres dans des sous-dossiers fixes :

| Dossier | Contenu |
| --- | --- |
| `outputs/tp1/` | Numéros filtrés, console et bilan JSON |
| `outputs/tp2/` | Texte chiffré, texte déchiffré et contrôle de l’aller-retour |
| `outputs/tp3/` | Tirages texte, graine, faces et tirages JSON |
| `outputs/tp4/` | Nombres premiers, facteurs, couples de Goldbach, images et paramètres |

**Ouvrir `outputs/index.md`.** Une nouvelle exécution met à jour les fichiers de mêmes noms. Pour conserver une expérience, donner un autre dossier :

```bash
python scripts/run_examples.py --output outputs/essai_02
```

Les fichiers de résultats et les environnements virtuels sont exclus de Git. `validation/` décrit une exécution de validation précise, pas une garantie sur toute modification ultérieure.

## Ressources techniques

- [Documentation officielle de `unittest`](https://docs.python.org/3/library/unittest.html)
- [Tester un projet Python avec GitHub Actions](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
