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

Pour executer ce projet sur son ordinateur, il faut avoir:

- Git, pour recuperer le projet;
- Python 3, idealement Python 3.10 ou plus recent;
- un terminal.

Verifier que Git est installe:

```bash
git --version
```

Verifier que Python 3 est installe:

```bash
python3 --version
```

Si la commande `python3` n'existe pas, il faut installer Python 3 avant de continuer.
Sur Windows, la commande peut aussi etre:

```bash
py -3 --version
```

Exemples d'installation si Git ou Python 3 ne sont pas encore disponibles:

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install git python3 python3-venv
```

```bash
# macOS avec Homebrew
brew install git python
```

Sur Windows, installer Git depuis le site officiel de Git et Python depuis le site officiel de Python.
Pendant l'installation de Python, cocher l'option permettant d'ajouter Python au `PATH`.

La partie nombres premiers n'utilise aucune bibliotheque externe: il n'y a donc pas de fichier `requirements.txt` a installer pour cette partie.

Creation optionnelle d'un environnement virtuel, apres avoir clone le projet:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sous Windows, l'activation peut se faire avec:

```bash
.venv\Scripts\activate
```

## Execution etape par etape

1. Cloner le depot.

Avec SSH:

```bash
git clone git@github.com:birane-m/intro-python3.git
```

Ou avec HTTPS:

```bash
git clone https://github.com/birane-m/intro-python3.git
```

2. Entrer dans le dossier du TP.

```bash
cd intro-python3/tp4-nombres-premiers-et-images
```

3. Verifier que Python 3 fonctionne.

```bash
python3 --version
```

4. Creer et activer un environnement virtuel, si souhaite.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Cette etape est optionnelle pour la partie nombres premiers, car le code n'a pas besoin de dependance externe.
Sur Windows, remplacer `python3` par `py -3` si necessaire.

5. Tester Goldbach jusqu'a `N`.

```bash
python3 src/goldbach.py N
```

Exemple avec `N = 10`:

```bash
python3 src/goldbach.py 10
```

6. Decomposer un nombre `N`.

```bash
python3 src/decomposition.py N
```

Exemples avec `N = 68` puis `N = 67`:

```bash
python3 src/decomposition.py 68
python3 src/decomposition.py 67
```

7. Variante: executer les scripts depuis le dossier `src`.

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
