# Introduction à Python 3

Quatre travaux pratiques réalisés dans le cadre du cours d’introduction à Python à l’Institut Galilée, Université Sorbonne Paris Nord.

Ce dépôt présente des exercices de traitement de données, de programmation orientée objet, d’algorithmique et de manipulation d’images. Chaque TP conserve son énoncé et ses commandes de rendu, avec des validations d’entrée et des tests automatisés.

## Les travaux pratiques

| TP | Sujet | Notions mises en pratique |
| --- | --- | --- |
| [TP1 — Filtrage de numéros](tp1-filtage-spam/README.md) | Normaliser des numéros français et repérer les doublons | Chaînes, compréhensions, CSV, `zip`, `Counter` |
| [TP2 — Chiffrement par substitution](tp2-chiffrement-substitution/README.md) | Chiffrer, déchiffrer et rechercher une clé | Classes, exceptions, dictionnaires, recherche locale |
| [TP3 — Générateurs aléatoires](tp3-random-number-generator/README.md) | Dés, pièces, sacs de billes et paquets de dés | Héritage, classes abstraites, composition, copies profondes |
| [TP4 — Nombres premiers et images](tp4-nombres-premiers-et-images/README.md) | Crible, décomposition et traitements de pixels | Slicing, NumPy, tableaux, OpenCV |

Le nom historique `tp1-filtage-spam` est conservé pour préserver les chemins existants ; le TP traite bien de numéros de téléphone.

## Installation

**Python 3.10 ou supérieur** est requis. Les TP1 à TP3 et les calculs de nombres premiers du TP4 utilisent uniquement la bibliothèque standard. NumPy et OpenCV sont nécessaires pour les images et la démonstration complète.

```bash
git clone https://github.com/birane-m/intro-python3.git
cd intro-python3
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Sous Windows, créer l’environnement avec `py -3 -m venv .venv`, puis l’activer dans PowerShell avec `.venv\Scripts\Activate.ps1`. Utiliser ensuite les mêmes commandes `python`.

Le fichier `requirements.txt` de la racine renvoie vers celui du TP4 : les dépendances sont définies à un seul endroit.

## Vérifier et essayer

Depuis la racine du dépôt, avec l’environnement activé :

```bash
python -m unittest discover -s tests -v
python scripts/run_examples.py
```

La deuxième commande produit un dossier `outputs/` : ouvrir **`outputs/index.md`** pour accéder aux résultats, aux paramètres et à la comparaison des images.

Pour tester les parties sans dépendances externes :

```bash
python3 -m unittest discover -s tests -p 'test_tp*.py' -v
```

Les tests d’images sont ignorés par la découverte complète si NumPy ou OpenCV manque. `make test` vérifie leur présence avant de lancer la suite entière. Le workflow GitHub Actions installe ces dépendances et lance les tests sur Python 3.10, 3.12 et 3.13.

Sur Linux ou macOS, des raccourcis sont disponibles :

```bash
make install
make test
make demo
```

## Exécuter un TP

Exemples depuis la racine, avec l’environnement activé :

```bash
python tp1-filtage-spam/src/format_phone_numbers.py
python tp3-random-number-generator/src/denface.py 6 5 --seed 1
python tp4-nombres-premiers-et-images/src/decomposition.py 68
python tp4-nombres-premiers-et-images/nb.py \
  tp4-nombres-premiers-et-images/data/chien.jpg outputs/chien_gris.png
```

Les arguments de fichiers explicites sont relatifs au dossier courant. Les données par défaut du TP1 et du script d’exploration NumPy sont repérées à partir de leur emplacement dans le projet.

Les commandes conservent les sorties attendues par les sujets : tirages seuls sur la sortie standard pour le TP3, égalités seules pour les commandes numériques du TP4. Les diagnostics passent sur la sortie d’erreur et les échecs renvoient un code non nul.

## Organisation

- `tp1-…/` à `tp4-…/` : code, données et énoncé de chaque TP ;
- `tests/` : tests unitaires, cas limites et tests des commandes ;
- `scripts/` : génération des exemples et préparation de l’archive ;
- `outputs/` : résultats générés, exclus de Git ;
- `validation/` : compte rendu de la validation livrée ;
- `.github/workflows/tests.yml` : vérification automatique à chaque push et pull request.

Les dossiers `output/` propres aux TP restent utilisables pour les commandes individuelles. La démonstration commune centralise ses fichiers dans `outputs/tp1/` à `outputs/tp4/`.

## Périmètre et limites

Les algorithmes restent ceux des TP. Le chiffrement par substitution est un exercice historique. La recherche de clé peut rester bloquée sur un optimum local. La vérification de Goldbach porte sur un intervalle fini et ne constitue pas une preuve de la conjecture. La conversion en gris suit la moyenne des trois canaux demandée par le sujet.

Les ressources `data/` et les énoncés `docs/` proviennent des supports de cours fournis avec les TP. L’extension facultative du TP3 utilisant une source quantique distante n’est pas implémentée ; les tirages fonctionnent hors ligne avec `random.Random`.

## Documentation

- [Guide d’exécution et sorties](GUIDE_EXECUTION.md)
- [Corrections et choix de conception](MODIFICATIONS.md)
- [Intégrer l’archive dans un dépôt existant](INTEGRATION.md)
- [Bilan des vérifications](validation/README.md)

Auteur des solutions : **Papa Birane Mbengue**.
