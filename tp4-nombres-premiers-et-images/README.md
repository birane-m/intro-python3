# TP4 - Nombres premiers

Projet Python permettant de calculer des nombres premiers, de tester la conjecture de Goldbach et de décomposer un entier en produit de facteurs premiers.

Ce README documente uniquement la première partie du TP4. La partie sur les images, NumPy et OpenCV n'est pas traitée ici.

## Problème

Le TP demande de construire une classe `NbPremier` capable de préparer les nombres premiers jusqu'à une limite `N`, puis de réutiliser ces informations pour répondre efficacement à plusieurs questions.

Il faut pouvoir:
1. savoir si un entier `k` est premier ;
2. afficher, pour chaque nombre pair entre `4` et `N`, une écriture `p=a+b` où `a` et `b` sont premiers ;
3. afficher la décomposition d'un entier `N` en facteurs premiers.

## Solution proposée

La classe `NbPremier`, définie dans `src/classes.py`, utilise le crible d'Ératosthène pour calculer les nombres premiers jusqu'à `N`.

Elle construit trois structures:
1. `est_prime`, une liste de booléens pour tester rapidement si un nombre est premier ;
2. `lprime`, la liste des nombres premiers trouvés ;
3. `facteurs`, une liste utilisée pour retrouver les facteurs premiers lors de la décomposition.

`est_prime` permet un test de primalité en accès direct, tandis que `lprime` facilite le parcours des nombres premiers pour Goldbach.

Exemple d'utilisation directe:

```python
from classes import NbPremier

nombres = NbPremier(20)

print(nombres.est_nombre_premier(19))
print(nombres.est_nombre_premier(20))
```

Sortie:

```text
True
False
```

## Exemples de tests

Depuis le dossier du TP4, tester la conjecture de Goldbach jusqu'à `10`:

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

Tester la décomposition d'un nombre composé:

```bash
python3 src/decomposition.py 68
```

Sortie obtenue:

```text
68=2*2*17
```

Tester la décomposition d'un nombre premier:

```bash
python3 src/decomposition.py 67
```

Sortie obtenue:

```text
67=67
```

Vérifier la syntaxe Python:

```bash
python3 -m py_compile src/classes.py src/goldbach.py src/decomposition.py
```

## Exécution

Cloner le dépôt:

```bash
git clone https://github.com/birane-m/intro-python3.git
```

Se placer dans le dossier du TP4:

```bash
cd intro-python3/tp4-nombres-premiers-et-images
```

Tester Goldbach jusqu'à `N`:

```bash
python3 src/goldbach.py N
```

Décomposer un entier `N`:

```bash
python3 src/decomposition.py N
```

Prérequis: Python 3, idéalement Python 3.10 ou plus récent. Aucune dépendance externe n'est nécessaire pour la partie nombres premiers.

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
