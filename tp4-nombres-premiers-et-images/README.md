# TP4 - Nombres premiers

Classe Python permettant de calculer les nombres premiers jusqu'a une limite `N`, de tester la conjecture de Goldbach et d'afficher la decomposition d'un nombre en facteurs premiers.

Ce README documente uniquement la premiere partie du TP4. La partie sur les images, NumPy et OpenCV n'est pas traitee ici.

## Fonctionnement

La classe `NbPremier`, definie dans `src/classes.py`, construit les informations utiles avec le crible d'Eratosthene.

Le programme prepare:
1. `est_prime`, une liste de booleens pour savoir rapidement si un nombre est premier ;
2. `lprime`, la liste des nombres premiers trouves jusqu'a `N` ;
3. `facteurs`, une liste permettant de retrouver les facteurs premiers d'un nombre.

Les scripts fournis permettent ensuite:
1. d'afficher les decompositions de Goldbach pour tous les nombres pairs entre `4` et `N` ;
2. d'afficher la decomposition de `N` en produit de facteurs premiers.

## Prerequis

- Git, pour cloner le depot ;
- Python 3, idealement Python 3.10 ou plus recent ;
- aucune dependance externe pour la partie nombres premiers.

Verifier les installations:

```bash
git --version
python3 --version
```

Sur Windows, la commande Python peut etre:

```bash
py -3 --version
```

Si Python 3 ou Git ne sont pas installes, il faut les installer avant de continuer.

## Installation

Cloner le depot:

```bash
git clone https://github.com/birane-m/intro-python3.git
```

Se placer dans le dossier du TP4:

```bash
cd intro-python3/tp4-nombres-premiers-et-images
```

Creation optionnelle d'un environnement virtuel:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sous Windows:

```bash
py -3 -m venv .venv
.venv\Scripts\activate
```

Il n'y a pas de `requirements.txt` a installer pour cette partie du projet.

## Utilisation

Tester la conjecture de Goldbach jusqu'a `N`:

```bash
python3 src/goldbach.py N
```

Exemple:

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

Afficher la decomposition en facteurs premiers de `N`:

```bash
python3 src/decomposition.py N
```

Exemples:

```bash
python3 src/decomposition.py 68
python3 src/decomposition.py 67
```

Sorties obtenues:

```text
68=2*2*17
67=67
```

## Tests

Les commandes suivantes ont ete utilisees pour verifier la partie nombres premiers:

```bash
python3 src/goldbach.py 10
python3 src/decomposition.py 68
python3 src/decomposition.py 67
python3 -m py_compile src/classes.py src/goldbach.py src/decomposition.py
```

## Structure

```text
tp4-nombres-premiers-et-images/
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
