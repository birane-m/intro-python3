# TP2 — Chiffrement par substitution

Implémenter une substitution monoalphabétique, son inverse et une recherche locale de clé fondée sur les quadgrammes anglais.

[Énoncé](docs/TP2.pdf) · [Installation commune](../README.md#installation) · [Commandes détaillées](../GUIDE_EXECUTION.md#tp2--chiffrer-et-déchiffrer)

## Modèle

- `Encodeur` valide une permutation des 26 lettres minuscules, puis substitue les lettres du texte en conservant la casse.
- `Decodeur` valide la clé originale avant de construire sa permutation inverse.
- `CodeBreaker` échange deux lettres d’une clé candidate et conserve les améliorations de score.

Seules les lettres ASCII `a-z` et `A-Z` sont chiffrées. Les accents, espaces, chiffres, ponctuations et autres caractères sont conservés. Le nettoyage utilisé pour le score garde uniquement les lettres ASCII et les passe en minuscules.

Ce chiffrement historique est un exercice pédagogique, impropre à la protection de données réelles.

## Chiffrer et déchiffrer

Après l’installation commune, depuis le dossier du TP2 :

```bash
python encodage.py data/test_encoding.txt zyxwvutsrqponmlkjihgfedcba output/encoded.txt
python decodage.py output/encoded.txt zyxwvutsrqponmlkjihgfedcba output/decoded.txt
```

Les deux commandes reçoivent **la même clé de chiffrement originale**. Les dossiers de sortie sont créés automatiquement. Les fichiers sont lus et écrits en UTF-8.

Une clé répétant une lettre, contenant une majuscule ou ayant une longueur différente de 26 est rejetée. Les erreurs de lecture et d’écriture produisent un code d’échec et un diagnostic sur `stderr`.

## Rechercher une clé

```bash
python cassercode.py data/mystery_text.txt data/english_quadgrams.txt output/candidat.txt \
  --seed 42 --max-iterations 5000 --summary output/recherche.json
```

Les trois premiers arguments restent ceux du rendu demandé. Les options ajoutent la reproductibilité, une limite globale facultative et un bilan JSON.

Le score suit l’énoncé : somme des logarithmes des fréquences brutes des quadgrammes connus. Les quadgrammes absents contribuent zéro. Le score de référence du fichier `mystery_text.txt` nettoyé est **12176,13**, à l’arrondi du sujet. Les logarithmes du modèle sont préparés une seule fois.

La recherche commence avec l’alphabet dans l’ordre et s’arrête par défaut après 1000 permutations consécutives sans amélioration. Elle peut rester bloquée sur un optimum local : un candidat produit n’est pas nécessairement le texte original. Le modèle fourni est anglais ; ses scores ne sont pas une mesure universelle de qualité linguistique.

Le bilan JSON contient les scores, la graine demandée, le nombre d’itérations, la cause d’arrêt et la clé de **déchiffrement** trouvée. Un fichier de quadgrammes absent, vide ou invalide arrête la commande.

## Utilisation des classes

Depuis le dossier du TP2 :

```python
from src.classes import Encodeur, Decodeur

key = "zyxwvutsrqponmlkjihgfedcba"
encoded = Encodeur(key).encode_string("Bonjour, été !")
assert Decodeur(key).decode_string(encoded) == "Bonjour, été !"
```

## Organisation et tests

`src/classes.py` contient les classes et `src/cli.py` la gestion commune des commandes. `data/` contient le texte d’essai, le texte mystère et les fréquences ; `docs/` contient l’énoncé. Les résultats individuels peuvent être écrits dans `output/`.

Depuis la racine du dépôt :

```bash
python -m unittest tests.test_tp2 -v
```

Les tests vérifient les clés invalides, les allers-retours, les caractères Unicode, les erreurs de fichiers, le score de référence et les critères d’arrêt de la recherche.
