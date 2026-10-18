# Validation de la version livrée

Validation locale du 18 octobre 2026 sous Linux avec Python 3.12.14, NumPy 2.5.4 et OpenCV 4.14.0. Les numéros de version exacts et les commandes sont enregistrés dans [summary.json](summary.json).

## Résultat des tests

- **87 tests exécutés, aucun échec, aucune erreur, aucun test ignoré**, images comprises.
- **68 tests** pour les seules parties sans dépendances externes.
- [Journal de la suite complète](tests.log).

Les tests couvrent les fonctions métier, les erreurs d’entrée, les commandes et leurs formats, les fichiers temporaires, les copies des générateurs et les traitements d’images. Ils sont exécutés sans interface graphique ni appel réseau.

## Vérifications complémentaires

- Syntaxe des sources et tests compatible avec Python 3.10, vérifiée par l’analyseur de Python 3.12.
- Données d’entrée et énoncés PDF identiques à ceux du projet de départ.
- TP1 : 67 entrées, 63 valides, 4 invalides, doublons regroupés par tailles 2 et 3.
- TP2 : score de référence 12176,13 à l’arrondi du sujet ; aller-retour UTF-8 préservant aussi les fins de ligne.
- Crible confronté à une division d’essai indépendante ; produits des facteurs et couples de Goldbach contrôlés.
- Lecture et écriture de PNG, moyennes, bandes, contours et bordures vérifiés.
- Exemples générés avec leurs bilans et leur index ; comparaison des images inspectée visuellement.
- Liens Markdown locaux vérifiés et archive de sources contrôlée lors de la livraison.

## Limites

Cette validation décrit les fichiers livrés. Elle devra être relancée après des changements. La compatibilité d’exécution avec Python 3.10 et 3.13 et le comportement sous Windows ne sont pas affirmés comme testés localement. Le workflow GitHub Actions est configuré pour 3.10, 3.12 et 3.13 ; il s’exécutera après le push.

Les dépendances de `requirements.txt` ont des bornes de versions, pas un verrouillage exact. Pour reproduire au plus près cet environnement Linux/Python 3.12 :

```bash
python -m pip install numpy==2.5.4 opencv-python==4.14.0.94
```

Le casseur de code est heuristique ; ses tests ne garantissent pas la récupération du texte original pour tout message. Les tests de Goldbach portent sur des bornes finies.
