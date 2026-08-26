# TP2 - Chiffrement par substitution

Projet Python orienté objet permettant de chiffrer, déchiffrer et attaquer un texte chiffré par substitution monoalphabétique.

## Problème

Le chiffrement par substitution monoalphabétique remplace chaque lettre de l'alphabet par une autre lettre définie par une clé de 26 caractères.

Le TP pose trois objectifs:
1. chiffrer un fichier texte avec une clé donnée ;
2. déchiffrer un fichier avec cette même clé ;
3. tenter de retrouver automatiquement un texte lisible sans connaître la clé, à partir de statistiques de langue.

## Solution proposée

Le projet est organisé autour de trois classes dans `src/classes.py`.

`Encodeur` applique la substitution lettre par lettre. Les minuscules et les majuscules sont transformées, tandis que les espaces, chiffres et signes de ponctuation sont conservés.

`Decodeur` reconstruit l'alphabet inverse de la clé de chiffrement, puis réutilise la logique de l'encodeur pour restaurer le texte original.

`CodeBreaker` charge un fichier de fréquences de quadgrammes anglais, évalue la vraisemblance linguistique des textes candidats et améliore progressivement une clé par permutations de lettres.

Le projet définit aussi des exceptions personnalisées pour refuser les clés invalides: longueur incorrecte, caractères interdits ou lettres dupliquées.

Exemple d'utilisation directe:

```python
from classes import Encodeur, Decodeur

pwd = "bcdefghijklmnopqrstuvwxyza"
texte = "abc XYZ!"

chiffre = Encodeur(pwd).encode_string(texte)
clair = Decodeur(pwd).decode_string(chiffre)

print(chiffre)
print(clair)
```

Sortie:

```text
bcd YZA!
abc XYZ!
```

## Exemples de tests

Depuis le dossier du TP2, chiffrer un fichier:

```bash
python3 encodage.py data/test_encoding.txt bcdefghijklmnopqrstuvwxyza /tmp/tp2_encoded.txt
```

Déchiffrer le fichier obtenu:

```bash
python3 decodage.py /tmp/tp2_encoded.txt bcdefghijklmnopqrstuvwxyza /tmp/tp2_decoded.txt
```

Vérifier que le déchiffrement retrouve le texte initial:

```bash
diff --strip-trailing-cr data/test_encoding.txt /tmp/tp2_decoded.txt
```

Tester le cassage automatique avec les quadgrammes:

```bash
python3 cassercode.py data/mystery_text.txt data/english_quadgrams.txt output/output_mystery.txt
```

Vérifier la syntaxe Python:

```bash
python3 -m py_compile encodage.py decodage.py cassercode.py src/classes.py
```

## Exécution

Cloner le dépôt:

```bash
git clone https://github.com/birane-m/intro-python3.git
```

Se placer dans le dossier du TP2:

```bash
cd intro-python3/tp2-chiffrement-substitution
```

Chiffrer un fichier:

```bash
python3 encodage.py <fichier_entree> <cle_26_lettres> <fichier_sortie>
```

Déchiffrer un fichier:

```bash
python3 decodage.py <fichier_entree> <cle_26_lettres> <fichier_sortie>
```

Casser un fichier chiffré:

```bash
python3 cassercode.py <fichier_chiffre> <fichier_quadgrammes> <fichier_sortie>
```

Prérequis: Python 3. Aucune dépendance externe n'est nécessaire.

## Structure

```text
tp2-chiffrement-substitution/
├── data/
│   ├── english_quadgrams.txt
│   ├── mystery_text.txt
│   └── test_encoding.txt
├── docs/
│   └── TP2.pdf
├── output/
├── src/
│   └── classes.py
├── encodage.py
├── decodage.py
├── cassercode.py
└── README.md
```
