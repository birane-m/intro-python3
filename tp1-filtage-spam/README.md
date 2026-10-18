# TP1 — Filtrage de numéros de téléphone

Normaliser une liste de numéros français, éliminer les numéros invalides et repérer les personnes partageant un même numéro.

[Énoncé](docs/TP1_Enonce.pdf) · [Installation commune](../README.md#installation) · [Guide d’exécution](../GUIDE_EXECUTION.md)

## Méthode

`format_phone_number()` applique les règles du sujet : conserver les chiffres et `+`, convertir les préfixes `+33` et `0033` en `0`, supprimer les `+` restants, puis vérifier les dix chiffres et le zéro initial. La sortie est une paire `(valide, numéro_formaté)`.

Le traitement du fichier utilise `csv`, les compréhensions, `map`, `zip` et `Counter`. Les règles sont celles de l’exercice : il ne s’agit pas d’une validation exhaustive du plan de numérotation français.

## Exécution

Depuis la racine du dépôt :

```bash
python tp1-filtage-spam/src/format_phone_numbers.py
```

Depuis le dossier de ce TP :

```bash
python src/format_phone_numbers.py
```

Les chemins par défaut sont liés à l’emplacement du script ; ces deux commandes lisent les mêmes données. Les options `--input`, `--output` et `--summary` permettent de choisir d’autres fichiers.

## Entrées et sorties

| Fichier | Rôle |
| --- | --- |
| `data/liste_numeros.txt` | Données du sujet, une entrée `nom : numéro` par ligne |
| `output/output.txt` | Entrées valides, avec le numéro au format `01-23-45-67-89` |
| `output/output.summary.json` | Effectifs et tailles des groupes de doublons |

Pour les données fournies : **67 entrées, 63 numéros valides, 4 invalides et deux groupes de tailles 2 et 3**. Les noms associés aux numéros invalides et les groupes sont affichés dans la console.

Un fichier vide donne une sortie vide et un bilan à zéro. Les lignes vides sont ignorées. Une ligne mal formée entraîne un message avec son numéro de ligne et un code d’échec.

## Utilisation de la fonction

Depuis ce dossier :

```python
from src.format_phone_numbers import format_phone_number

print(format_phone_number("+(33) 6 58 47 25 14"))
# (True, '06-58-47-25-14')
```

## Tests

Depuis la racine du dépôt :

```bash
python -m unittest tests.test_tp1 -v
```

Les tests couvrent les exemples de l’énoncé, les effectifs du fichier fourni, les fichiers vides, les lignes incorrectes, les chemins et les erreurs de la commande.
