# TP4 - Nombres premiers

Ce projet correspond a la premiere partie du TP4, consacree aux nombres premiers.
La deuxieme partie sur les images, NumPy et OpenCV n'est pas traitee dans ce README.

## Objectif

Le but est de creer une classe `NbPremier` capable de preparer les informations utiles sur les nombres premiers jusqu'a une limite `N`, puis de les reutiliser pour:

- savoir rapidement si un nombre est premier;
- verifier la conjecture de Goldbach pour les nombres pairs entre `4` et `N`;
- decomposer un entier en produit de facteurs premiers.

La contrainte importante est de garder un code simple, court et efficace, dans l'esprit Python.

## Structure du projet

```text
.
├── README.md
├── docs/
│   └── TP4.pdf
├── src/
│   ├── classes.py
│   ├── goldbach.py
│   └── decomposition.py
└── data/
    ├── chien.jpg
    └── ps5.png
```

Les fichiers importants pour la partie nombres premiers sont:

- `src/classes.py`: contient la classe `NbPremier` et l'exception `ParameterTooHighValue`;
- `src/goldbach.py`: lance le test de Goldbach depuis le terminal;
- `src/decomposition.py`: affiche la decomposition en facteurs premiers d'un nombre.

## Solution choisie

La classe `NbPremier` calcule les nombres premiers jusqu'a `N` avec le crible d'Eratosthene.
Elle construit trois structures:

- `est_prime`: liste de booleens ou `est_prime[k]` indique si `k` est premier;
- `lprime`: liste contenant tous les nombres premiers trouves;
- `facteurs`: liste gardant une trace d'un facteur premier pour chaque nombre, utile pour la decomposition.

Extrait de l'initialisation:

```python
def __init__(self, n):
    self.est_prime, self.lprime, self.facteurs = self.eratosthene(n)
```

`est_prime` permet de tester un nombre en temps constant, tandis que `lprime` est pratique pour parcourir uniquement les nombres premiers.

## Fonctionnalites

### Tester si un nombre est premier

La methode `est_nombre_premier(k)` retourne `True` si `k` est premier, sinon `False`.
Si `k` depasse la limite `N` donnee au constructeur, une exception `ParameterTooHighValue` est levee.

```python
from classes import NbPremier

nombres = NbPremier(100)
print(nombres.est_nombre_premier(97))
```

### Tester la conjecture de Goldbach

La methode `test_goldbach()` affiche, pour chaque nombre pair `p` entre `4` et `N`, une decomposition sous la forme:

```text
p=a+b
```

ou `a` et `b` sont deux nombres premiers.

Exemple:

```bash
python3 src/goldbach.py 10
```

Sortie:

```text
4=2+2
6=3+3
8=3+5
10=3+7
```

### Decomposer en facteurs premiers

La methode `decomposition(k)` affiche la decomposition de `k` en produit de nombres premiers.
Elle utilise la liste `facteurs` construite pendant le crible pour retrouver les facteurs successifs.

Exemple:

```bash
python3 src/decomposition.py 68
```

Sortie:

```text
68=2*2*17
```

## Installation et prerequis

Prerequis:

- Python 3.10 ou plus recent;
- aucune bibliotheque externe pour la partie nombres premiers.

Creation optionnelle d'un environnement virtuel:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Il n'y a rien a installer avec `pip` pour executer cette partie du projet.

## Execution etape par etape

Depuis la racine du projet:

```bash
cd tp4-nombres-premiers-et-images
```

Tester Goldbach jusqu'a `N`:

```bash
python3 src/goldbach.py N
```

Exemple:

```bash
python3 src/goldbach.py 10
```

Decomposer un nombre `N`:

```bash
python3 src/decomposition.py N
```

Exemples:

```bash
python3 src/decomposition.py 68
python3 src/decomposition.py 67
```

Si l'on se place directement dans le dossier `src`, les commandes deviennent:

```bash
cd src
python3 goldbach.py 10
python3 decomposition.py 68
```

## Tests realises

Les tests suivants permettent de verifier les sorties produites par le code pour la partie nombres premiers.

### Goldbach

Commande:

```bash
python3 src/goldbach.py 10
```

Sortie obtenue:

```text
4=2+2
6=3+3
8=3+5
10=3+7
```

### Decomposition d'un nombre compose

Commande:

```bash
python3 src/decomposition.py 68
```

Sortie obtenue:

```text
68=2*2*17
```

### Decomposition d'un nombre premier

Commande:

```bash
python3 src/decomposition.py 67
```

Sortie obtenue:

```text
67=67
```

## Remarques

- Les scripts attendent exactement un argument en ligne de commande: la valeur de `N`.
- Les affichages ne contiennent pas d'espaces afin de respecter le format demande par l'enonce.
- La partie images du TP est volontairement separee de cette documentation.
