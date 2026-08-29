# TP4 - Nombres premiers et images

Projet Python combinant deux sujets: le calcul de nombres premiers avec le crible d'Eratosthene, puis la manipulation d'images avec NumPy et OpenCV.

## Probleme

La premiere partie du TP demande de construire une classe capable de preparer les nombres premiers jusqu'a une limite `N`, puis de reutiliser ces informations pour tester la primalite, verifier la conjecture de Goldbach et decomposer un entier en facteurs premiers.

La seconde partie introduit les images comme tableaux NumPy. L'objectif est de lire une image avec OpenCV, de la convertir en noir et blanc, puis de proposer quelques traitements simples comme l'ajout de bandes noires ou le calcul de contours.

## Solution proposee

Le coeur du projet est regroupe dans `src/classes.py`.

Pour les nombres premiers, la classe `NbPremier` utilise le crible d'Eratosthene. Elle construit:
1. `est_prime`, une liste de booleens pour tester rapidement si un nombre est premier ;
2. `lprime`, la liste des nombres premiers trouves ;
3. `facteurs`, une liste utilisee pour retrouver les facteurs premiers lors de la decomposition.

Pour les images, la classe `Image` encapsule une image lue par OpenCV. Elle propose:
1. `to_gray()`, pour convertir une image couleur en noir et blanc ;
2. `add_black_stripes(n)`, pour ajouter des bandes horizontales noires tous les `n` pixels ;
3. `compute_contours(k)`, pour calculer une image de contours a partir du contraste local ;
4. `save(output_file)`, pour sauvegarder le resultat.

Le script `nb.py` correspond au rendu demande pour la conversion noir et blanc:

```bash
python3 nb.py entree.jpg sortie.jpg
```

Exemple d'utilisation directe des classes:

```python
from classes import NbPremier, Image

nombres = NbPremier(20)
print(nombres.est_nombre_premier(19))

image = Image("data/chien.jpg")
image.to_gray()
image.save("output/chien_nb.jpg")
```

## Exemples de tests

Tester la conjecture de Goldbach jusqu'a `10`:

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

Tester la decomposition d'un nombre compose:

```bash
python3 src/decomposition.py 68
```

Sortie obtenue:

```text
68=2*2*17
```

Tester la decomposition d'un nombre premier:

```bash
python3 src/decomposition.py 67
```

Sortie obtenue:

```text
67=67
```

Convertir une image en noir et blanc:

```bash
python3 nb.py data/chien.jpg /tmp/chien_nb.jpg
```

Verifier que l'image de sortie a bien ete creee:

```bash
python3 -c "import cv2; im = cv2.imread('/tmp/chien_nb.jpg', cv2.IMREAD_GRAYSCALE); assert im is not None; print(im.shape)"
```

Verifier la syntaxe Python:

```bash
python3 -m py_compile nb.py src/classes.py src/goldbach.py src/decomposition.py
```

## Execution

Cloner le depot:

```bash
git clone https://github.com/birane-m/intro-python3.git
```

Se placer dans le dossier du TP4:

```bash
cd intro-python3/tp4-nombres-premiers-et-images
```

Creer et activer un environnement virtuel:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sous Windows:

```bash
py -3 -m venv .venv
.venv\Scripts\activate
```

Installer les dependances de la partie images:

```bash
python3 -m pip install -r requirements.txt
```

Tester Goldbach jusqu'a `N`:

```bash
python3 src/goldbach.py N
```

Decomposer un entier `N`:

```bash
python3 src/decomposition.py N
```

Convertir une image couleur en noir et blanc:

```bash
python3 nb.py entree.jpg sortie.jpg
```

## Structure

```text
tp4-nombres-premiers-et-images/
├── data/
│   ├── chien.jpg
│   └── ps5.png
├── docs/
│   └── TP4.pdf
├── src/
│   ├── classes.py
│   ├── decomposition.py
│   ├── goldbach.py
│   └── PremierContactNumpy.py
├── nb.py
├── requirements.txt
└── README.md
```
