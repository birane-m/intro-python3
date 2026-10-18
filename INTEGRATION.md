# Intégrer cette version au dépôt existant

L’archive contient directement `README.md`, `tests/`, les quatre dossiers de TP et les autres fichiers du projet. **Elle n’ajoute pas de dossier `intro-python3/` autour de ces fichiers.**

Elle ne contient ni historique `.git`, ni environnement virtuel, ni copie de paquet tiers. Conserver le dossier de travail existant : l’extraction y remplace les fichiers du projet et préserve son historique Git. Les fichiers locaux absents de l’archive ne sont pas supprimés.

## Extraire à la racine

Depuis le dossier existant `intro-python3`, après avoir conservé une copie des éventuelles modifications locales à garder :

```bash
pwd
git rev-parse --show-toplevel
git status --short --branch
unzip -o "$HOME/Téléchargements/intro-python3-ameliore.zip" -d .
```

Adapter uniquement le chemin de téléchargement si nécessaire. Ne pas supprimer le dossier existant et ne pas refaire `git init`.

## Installer et vérifier

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/run_examples.py
```

Ouvrir `outputs/index.md` pour consulter les résultats.

## Retirer les anciennes sorties du suivi Git

Deux résultats générés étaient suivis dans la version de départ. La nouvelle règle d’exclusion ne retire pas automatiquement les fichiers déjà suivis. Cette commande les retire uniquement de l’index et les laisse sur disque :

```bash
git rm --cached --ignore-unmatch -- \
  tp1-filtage-spam/output/output.txt \
  tp4-nombres-premiers-et-images/output/chien_nb.jpg
```

Les environnements et fichiers de travail locaux peuvent rester en place. `utilities/`, le paquet tiers sous `tp3-random-number-generator/data/` et les anciens résultats ne sont pas nécessaires pour lancer les solutions et ne sont pas inclus dans l’archive de sources.

## Examiner les changements

```bash
git status --short --branch
git --no-pager diff --stat
git --no-pager diff --check
```

Un découpage possible pour la revue et les commits :

1. corrections des TP et tests associés ;
2. commandes communes, génération des exemples, archivage et workflow de tests ;
3. README, guide d’exécution et bilan de validation.

L’archive ne crée aucun commit et ne fait aucun push.
