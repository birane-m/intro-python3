# TP1 - Filtrage de numéros de téléphone

Projet Python de nettoyage, validation et reformatage de numéros de téléphone français saisis dans des formats hétérogènes.

## Problème

Le fichier d'entrée contient des lignes au format `Nom : numéro`, mais les numéros ne sont pas tous écrits de la même manière: espaces, tirets, parenthèses, préfixes `+33` ou `0033`, chiffres manquants ou en trop.

L'objectif est de produire une liste exploitable de numéros valides et homogènes, tout en identifiant les entrées incorrectes.

## Solution proposée

La fonction `format_phone_number` nettoie chaque numéro en conservant uniquement les chiffres utiles, convertit les préfixes internationaux français en format national, puis vérifie que le résultat commence par `0` et contient exactement 10 chiffres.

Les numéros valides sont reformattés sous la forme `01-23-45-67-89`.

Le script principal:
1. lit `data/liste_numeros.txt` ;
2. valide et reformate les numéros ;
3. écrit les entrées valides dans `output/output.txt` ;
4. affiche les personnes ayant fourni un numéro invalide ;
5. détecte les personnes partageant un même numéro.

Exemple d'utilisation directe de la fonction:

```python
from format_phone_numbers import format_phone_number

print(format_phone_number("+33 6 12 34 56 78"))
print(format_phone_number("09 30 (804) 59"))
```

Sortie:

```text
(True, '06-12-34-56-78')
(False, None)
```

## Exemples de tests

Depuis le dossier du TP1:

```bash
python3 src/format_phone_numbers.py
```

Le programme génère ou met à jour:

```text
output/output.txt
```

On peut aussi vérifier rapidement la fonction de formatage:

```bash
python3 -c "import sys; sys.path.insert(0, 'src'); from format_phone_numbers import format_phone_number; print(format_phone_number('+33 6 12 34 56 78'))"
```

Sortie attendue:

```text
(True, '06-12-34-56-78')
```

## Exécution

Cloner le dépôt:

```bash
git clone https://github.com/birane-m/intro-python3.git
```

Se placer dans le dossier du TP1:

```bash
cd intro-python3/tp1-filtage-spam
```

Lancer le script:

```bash
python3 src/format_phone_numbers.py
```

Prérequis: Python 3. Aucune dépendance externe n'est nécessaire.

## Structure

```text
tp1-filtage-spam/
├── data/
│   └── liste_numeros.txt
├── src/
│   └── format_phone_numbers.py
├── output/
│   └── output.txt
└── README.md
```
