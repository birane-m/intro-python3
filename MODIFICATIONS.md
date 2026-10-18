# Corrections et choix de conception

Cette révision part du ZIP fourni le 18 octobre 2026. Les sources principales correspondent à la révision publique `9a23e4d458c4f479f1237ade757d771b41a10473` ; le ZIP fournit aussi des ressources locales, dont le script d’exploration NumPy.

## TP1

- Chemins par défaut ancrés sur le dossier du TP, avec options pour les personnaliser.
- Lecture et écriture UTF-8 ; création des dossiers de sortie.
- Traitement des fichiers vides et des lignes blanches ; erreur localisée pour les lignes mal formées.
- Bilan JSON séparé du fichier des numéros, sans ajout des coordonnées personnelles dans le bilan.
- Règles de nettoyage et format du sujet conservés ; 63 numéros valides sur 67.

## TP2

- Validation commune des clés de l’encodeur et du décodeur, avant inversion.
- Substitution limitée à l’alphabet ASCII ; accents et autres caractères conservés.
- Erreurs de lecture et d’écriture propagées, puis traduites en diagnostics et codes d’échec dans les commandes.
- Modèle de quadgrammes obligatoire, non vide, avec fréquences positives finies.
- Logarithmes précalculés ; score brut et traitement des quadgrammes absents conservés.
- Générateur aléatoire propre à chaque objet ; graine, budget d’itérations et bilan optionnels.
- Sens de la clé retournée explicité : clé de déchiffrement.
- Critère d’arrêt par défaut conservé : 1000 permutations consécutives sans amélioration.

## TP3

- Validation des nombres de faces, billes et tirages ; validation des poids et de leur somme.
- Copie de la liste de poids reçue au constructeur.
- Copies profondes pour toutes les formes d’addition, y compris `dé + dé`.
- Distinction documentée entre copie des objets et indépendance statistique.
- Commandes historiques conservées ; options de graine et diagnostics ajoutés sans texte superflu sur stdout.
- L’ancien script de démonstration des tests redirige vers la suite `unittest` du TP3.
- La partie facultative utilisant un service quantique reste hors périmètre.

## TP4

- Crible cohérent pour les limites 0 et 1 ; marquage limité aux facteurs jusqu’à `isqrt(n)`.
- Nombres négatifs reconnus non premiers ; requêtes au-delà de la borne rejetées.
- Décomposition limitée aux entiers au moins égaux à 2, avec une méthode retournant les facteurs.
- Couples de Goldbach accessibles séparément de leur affichage strict.
- Images testables depuis un tableau, validations des paramètres et erreurs de sauvegarde lisibles.
- Conversion par moyenne conservée ; contours max-min à boucles et bordure nulle conservés.
- Script `PremierContactNumpy.py` rétabli depuis le ZIP, nettoyé et sans effet de bord à l’import.

## Organisation commune

- Tests unitaires et tests des commandes à la racine.
- `Makefile`, dépendances communes par inclusion et workflow GitHub Actions.
- Démonstration avec index Markdown, fichiers par TP et bilans JSON.
- Archive sans dossier enveloppe, environnement virtuel ni métadonnées Git.
- README principal et README de chaque TP réécrits ; guide d’exécution et consignes d’intégration ajoutés.
- Les énoncés et données de référence sont conservés. Aucune licence sur les supports de cours n’est présumée.

Les vérifications réellement exécutées et les limites de cette validation sont décrites dans [validation/README.md](validation/README.md). Le workflow distant sera exécuté après intégration et push ; sa présence n’implique pas qu’il a déjà réussi sur GitHub.
