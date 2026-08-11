# TP2 : Chiffrement par Substitution Monoalphabétique & Cassage de Code

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Ce projet est une réalisation pratique orientée objet en Python développée dans le cadre du cursus d'ingénieur en informatique à l'**Institut Galilée (Université Sorbonne Paris Nord / Paris 13)** pour le cours *Introduction à Python*.

Il met en œuvre un système complet de **chiffrement par substitution monoalphabétique**, de **déchiffrement avec clé**, ainsi qu'un **module d'attaque automatique (CodeBreaker)** capable de casser un cryptogramme sans connaître le mot de passe initial grâce à l'analyse fréquentielle par quadgrammes et à un algorithme de descente de gradient.

---

## 📌 Sommaire
1. [Contexte & Principes](#-contexte--principes)
2. [Structure du Projet](#-structure-du-projet)
3. [Fonctionnalités & Architecture](#-fonctionnalités--architecture)
   - [Classe Encodeur](#1-classe-encodeur)
   - [Classe Decodeur](#2-classe-decodeur)
   - [Classe CodeBreaker](#3-classe-codebreaker)
   - [Gestion des Exceptions](#4-gestion-des-exceptions-sur-les-mots-de-passe)
4. [Installation & Prérequis](#-installation--prérequis)
5. [Guide d'Utilisation](#-guide-dutilisation)
   - [1. Chiffrer un texte (`encodage.py`)](#1-chiffrer-un-texte-encodagepy)
   - [2. Déchiffrer un texte avec mot de passe (`decodage.py`)](#2-déchiffrer-un-texte-avec-mot-de-passe-decodagepy)
   - [3. Casser un texte chiffré sans mot de passe (`cassercode.py`)](#3-casser-un-texte-chiffré-sans-mot-de-passe-cassercodepy)
6. [Détails Algorithmiques du CodeBreaker](#-détails-algorithmiques-du-codebreaker)
7. [Auteur](#-auteur)

---

## 📖 Contexte & Principes

### Le Chiffrement par Substitution
Le chiffrement par substitution monoalphabétique consiste à remplacer chaque lettre de l'alphabet original par une lettre correspondante d'un alphabet désordonné de 26 lettres (le **mot de passe**).
* Les lettres minuscules sont remplacées par les minuscules correspondantes du mot de passe.
* Les lettres majuscules sont remplacées par les majuscules correspondantes du mot de passe.
* La ponctuation, les chiffres, les espaces et les retours à la ligne restent inchangés.

### Le Cassage par Analyse de Quadgrammes
Pour casser un code sans connaître la clé (parmi $26! \approx 4 \times 10^{26}$ clés possibles), le système évalue la vraisemblance linguistique des déchiffrements candidats au moyen d'un dictionnaire de **quadgrammes** (groupes de 4 lettres consécutives).

---

## 📁 Structure du Projet

```text
tp2-chiffrement-substitution/
├── docs/
│   └── TP2.pdf                    # Énoncé officiel du TP
├── data/
│   ├── english_quadgrams.txt      # Base de données des quadgrammes anglais et leurs fréquences
│   ├── mystery_text.txt           # Exemple de texte chiffré à attaquer
│   └── test_encoding.txt          # Fichier texte de test pour encodage/décodage
├── output/
│   └── output_mystery.txt         # Fichier déchiffré produit par cassercode.py
├── src/
│   ├── __init__.py
│   └── classes.py                 # Implémentation des classes Encodeur, Decodeur, CodeBreaker et Exceptions
├── encodage.py                    # Script CLI pour l'encodage d'un fichier
├── decodage.py                    # Script CLI pour le décodage d'un fichier avec clé
├── cassercode.py                  # Script CLI d'attaque et de cassage automatique
├── .gitignore
└── README.md                      # Documentation du projet
```

---

## 🛠 Fonctionnalités & Architecture

Les composants logiques du projet sont regroupés au sein du module [`src/classes.py`](file:///home/birane/Documents/PYTHON/Python3/intro-python3/tp2-chiffrement-substitution/src/classes.py) :

### 1. Classe `Encodeur`
* **`__init__(pwd=None)`** : Initialise l'encodeur avec un mot de passe de 26 lettres minuscules uniques. Si aucun mot de passe n'est fourni, un alphabet aléatoire est généré (`random.shuffle`).
* **`encode_string(input_string)`** : Chiffre la chaîne fournie en préservant la casse et la ponctuation.
* **`encode_file(input_file, output_file)`** : Chiffre le contenu d'un fichier source et l'écrit dans un fichier cible.

### 2. Classe `Decodeur`
* **`__init__(password)`** : Génère l'alphabet inverse correspondant au mot de passe de chiffrement à l'aide de `zip` et `sorted`, puis instancie un `Encodeur` interne configuré avec ce mot de passe inverse.
* **`decode_string(input_string)`** : Déchiffre la chaîne transmise.
* **`decode_file(input_file, output_file)`** : Déchiffre le fichier transmis et sauvegarde le résultat.

### 3. Classe `CodeBreaker`
* **`__init__(quadgram_file)`** : Charge le dictionnaire de quadgrammes et leurs occurrences associées.
* **`string_cleaner(input_string)`** : Nettoie le texte en ne conservant que les lettres `a-z` en minuscules.
* **`pwd_generator(mdp, i=None, j=None)`** : Échange deux lettres aux indices `i` et `j` (sélectionnés aléatoirement si non fournis).
* **`score_calculator(input_string)`** : Calcule le score de vraisemblance logarithmique $\sum \ln(\text{fréquence})$ sur l'ensemble des quadgrammes du texte.
* **`code_breaker(crypted_string)`** : Exécute la boucle d'optimisation (descente de gradient) et renvoie le mot de passe découvert ainsi que le texte déchiffré.

### 4. Gestion des Exceptions sur les Mots de Passe
Pour garantir la robustesse des entrées, une hiérarchie d'exceptions personnalisées a été mise en place (Section 6 du TP) :
* **`PasswordError`** : Classe de base héritant d'`Exception` permettant de capturer n'importe quelle anomalie de clé avec une seule instruction `except`.
* **`InvalidPasswordLengthError`** : Levée si la longueur du mot de passe diffère de 26 lettres.
* **`InvalidPasswordCharError`** : Levée si le mot de passe comporte des caractères autres que des lettres minuscules `a-z`.
* **`DuplicateLetterError`** : Levée si une lettre apparaît plusieurs fois dans le mot de passe.

---

## 💻 Installation & Prérequis

* **Python 3.8+** (aucune dépendance tierce requise, uniquement la bibliothèque standard Python : `sys`, `os`, `string`, `random`, `math`).

Clonez le dépôt :
```bash
git clone https://github.com/birane-m/intro-python3.git
cd intro-python3/tp2-chiffrement-substitution
```

---

## 🚀 Guide d'Utilisation

### 1. Chiffrer un texte (`encodage.py`)
Pour chiffrer un fichier texte avec un mot de passe de 26 lettres :
```bash
python3 encodage.py data/test_encoding.txt wqaxszcdevfrbgtnhyjukilomp output/encoded.txt
```

### 2. Déchiffrer un texte avec mot de passe (`decodage.py`)
Pour déchiffrer le fichier produit à l'aide de la clé d'origine :
```bash
python3 decodage.py output/encoded.txt wqaxszcdevfrbgtnhyjukilomp output/decoded.txt
```

### 3. Casser un texte chiffré sans mot de passe (`cassercode.py`)
Pour attaquer un texte chiffré (dont on ne possède pas la clé) à l'aide du fichier de quadgrammes :
```bash
python3 cassercode.py data/mystery_text.txt data/english_quadgrams.txt output/output_mystery.txt
```

---

## 🔬 Détails Algorithmiques du CodeBreaker

L'algorithme du `CodeBreaker` fonctionne selon une recherche locale par **descente de gradient** (Hill Climbing) conforme aux exigences de l'énoncé :

1. **Initialisation** : L'alphabet démarre dans son ordre naturel (`abcdefghijklmnopqrstuvwxyz`) et un unique objet `Encodeur` est instancié.
2. **Définition du score de référence** : Le texte nettoyé est déchiffré avec la clé courante et évalué via la fonction de score logarithmique :
   $$\text{Score} = \sum_{i=0}^{N-4} \ln(\text{fréquence}(\text{quadgramme}_i))$$
3. **Optimisation par Permutation** :
   * Deux positions $i$ et $j$ sont choisies aléatoirement pour intervertir deux lettres dans l'alphabet de l'encodeur.
   * Le nouveau score du texte déchiffré est calculé.
   * **Si le score s'améliore** : La permutation est validée et le compteur de stagnation (`stagnant_count`) est réinitialisé à $0$.
   * **Sinon** : La permutation est annulée (les 2 lettres sont remises à leur place initiale) et le compteur de stagnation est incrémenté de $+1$.
4. **Critère d'arrêt** : Dès que le compteur atteint **1 000 permutations consécutives sans amélioration**, la recherche s'arrête et le texte d'origine est déchiffré complètement.

---

## 👤 Auteur

* **birane-m** — *Université Sorbonne Paris Nord / Institut Galilée*
