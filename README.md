# Introduction à Python 3

[![Tests Python](https://github.com/birane-m/intro-python3/actions/workflows/tests.yml/badge.svg)](https://github.com/birane-m/intro-python3/actions/workflows/tests.yml)

Solutions de quatre travaux pratiques du cours d’introduction à Python de l’Institut Galilée, Université Sorbonne Paris Nord.

Les exercices couvrent le traitement de fichiers, la programmation orientée objet, les algorithmes et la manipulation d’images. Chaque TP dispose de son énoncé, d’exemples d’exécution et de tests automatisés.

## Travaux pratiques

| TP | Sujet | Notions principales |
| --- | --- | --- |
| [TP1 — Numéros de téléphone](tp1-filtage-spam/README.md) | Normalisation et détection de doublons | Chaînes, compréhensions, CSV, `zip`, `Counter` |
| [TP2 — Chiffrement par substitution](tp2-chiffrement-substitution/README.md) | Chiffrement, déchiffrement et recherche de clé | Classes, exceptions, dictionnaires, recherche locale |
| [TP3 — Générateurs aléatoires](tp3-random-number-generator/README.md) | Dés, pièces, sacs de billes et paquets | Héritage, abstraction, composition, copies profondes |
| [TP4 — Nombres premiers et images](tp4-nombres-premiers-et-images/README.md) | Crible, factorisation et traitements d’images | Slicing, tableaux NumPy, OpenCV |

## Installation

**Python 3.10 ou supérieur.** NumPy et OpenCV sont nécessaires pour les images du TP4 et la démonstration complète. Les autres exercices utilisent la bibliothèque standard.

```bash
git clone https://github.com/birane-m/intro-python3.git
cd intro-python3
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Sous Windows, utiliser `py -3 -m venv .venv`, puis `.venv\Scripts\Activate.ps1` dans PowerShell. Les commandes `python` suivantes sont identiques.

Le fichier de dépendances à la racine renvoie vers celui du TP4, qui peut aussi être installé séparément.

## Tests

Depuis la racine du dépôt, avec l’environnement activé :

```bash
python -c "import numpy, cv2"
python -m unittest discover -s tests -v
```

La suite couvre les exemples des sujets, les entrées invalides, les formats des commandes, les copies des générateurs et les calculs sur les pixels. Elle n’ouvre aucune fenêtre et n’appelle aucun service distant. GitHub Actions exécute les tests sur Python 3.10, 3.12 et 3.13.

Pour tester uniquement les exercices sans dépendances externes :

```bash
python -m unittest discover -s tests -p 'test_tp*.py' -v
```

## Exemples et résultats

```bash
python scripts/run_examples.py
```

Ouvrir **`outputs/index.md`** pour parcourir les résultats :

| Dossier | Contenu |
| --- | --- |
| `outputs/tp1/` | Numéros filtrés et bilan du traitement |
| `outputs/tp2/` | Texte chiffré, texte déchiffré et contrôle de l’aller-retour |
| `outputs/tp3/` | Tirages, composition du paquet et graine aléatoire |
| `outputs/tp4/` | Nombres premiers, décompositions et comparaison des images |

Relancer la démonstration remplace les exemples de mêmes noms. Pour conserver une autre exécution :

```bash
python scripts/run_examples.py --output outputs/essai_02
```

Les résultats sont exclus du suivi Git. Les commandes individuelles et leurs options sont présentées dans le README de chaque TP ; `--help` affiche les arguments disponibles. Les chemins de fichiers passés en argument sont relatifs au dossier courant.

## Raccourcis Make

Sur Linux ou macOS :

| Commande | Action |
| --- | --- |
| `make install` | Créer `.venv` et installer les dépendances |
| `make test` | Vérifier les dépendances et lancer tous les tests |
| `make test-core` | Tester les exercices sans dépendances externes |
| `make demo` | Générer les exemples dans `outputs/` |

## Organisation

- `tp1-…/` à `tp4-…/` : sources, énoncés PDF, données et documentation de chaque TP ;
- `tests/` : tests des exercices, des commandes et de la démonstration ;
- `scripts/run_examples.py` : génération des exemples et de leur index ;
- `.github/workflows/tests.yml` : automatisation des tests.

Les énoncés et données de référence sont issus des supports de cours. Les algorithmes suivent les consignes des TP ; leurs limites sont précisées dans les README correspondants.

Auteur des solutions : **Papa Birane Mbengue**.
