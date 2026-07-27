# TP - Filtrage de numéros de téléphone

Fonction de nettoyage, validation et reformatage de numéros de téléphone français saisis dans des formats hétérogènes (espaces, tirets, parenthèses, `+33`, `0033`, etc.), appliquée à un fichier `Nom : numéro` pour n'en garder que les entrées valides.

## Fonctionnement

Un numéro est considéré comme valide s'il commence par `0` et comporte 10 chiffres une fois nettoyé. Les numéros valides sont reformatés sous la forme `01-23-45-67-89`.

Le script :
1. lit `data/liste_numeros.txt` (paires `Nom : numéro`) ;
2. filtre et reformate les numéros valides, puis écrit le résultat dans `output/output.txt` ;
3. affiche les noms des personnes ayant transmis un numéro invalide ;
4. détecte les personnes partageant un même numéro (foyers).

## Utilisation

```bash
python3 format_phone_numbers.py
```

Le fichier d'entrée doit se trouver dans `data/liste_numeros.txt`. Le résultat est généré dans `output/output.txt`.

## Structure

```
tp1-filtage-spam/
├── data/
│   └── liste_numeros.txt
├── src/
│   └── format_phone_numbers.py
├── output/
│   └── output.txt
└── README.md
```