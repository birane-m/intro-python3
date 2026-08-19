# TP3 : Random Number Generator (RNG)

Ce projet implémente un système orienté objet en Python pour simuler des tirages aléatoires de dés (classiques, truqués, illustrés, pièces de monnaie, sacs de billes sans remise) et des paquets de dés.

---

### 1. Structure des classes (`src/classes.py`)

* **`MyRandom`** : Classe mère abstraite (`abc.ABC`). Elle empêche son instanciation directe et définit la méthode abstraite `tirer()`. Elle gère également l'opérateur d'addition `+` pour combiner les dés et les paquets.
* **`DeNfacestruque` / `De6facestruque`** : Simule un dé à $N$ (ou 6) faces avec une liste de poids pour chaque face. Si aucun poids n'est fourni, les faces sont équiprobables.
* **`DeNfaces` / `De6faces`** : Simule un dé équilibré classique. Hérite de `DeNfacestruque` avec des poids égaux.
* **`PaquetDe`** : Conteneur regroupant une liste de dés.
  * **Addition (`+`)** : Permet d'additionner deux paquets (`pa1 + pa2`), un paquet et un dé (`pa + de`), ou deux dés (`de1 + de2`). Utilise des copies profondes (`copy.deepcopy`) pour éviter toute dépendance mémoire entre objets.
  * **`tirer(n)`** : Effectue $n$ lancers et regroupe les résultats par lancer via `zip`.
* **`DeNfacesIllustrees` & `Piece`** : Dés dont les faces sont associées à des étiquettes (ex: `"rouge"`, `"bleu"`) ou des côtés de pièce (`"pile"`, `"face"`).
* **`SacNBillesSansRemise`** : Sac de $N$ billes tirées sans remise. Lorsque toutes les billes ont été tirées, le sac se recharge automatiquement.

---

### 2. Programmes de tirage (`src/`)

Chaque script s'exécute directement en ligne de commande :

* **Dé classique** :
  ```bash
  python3 src/denface.py <nb_faces> <nb_tirages>
  ```
* **Dé truqué** :
  ```bash
  python3 src/denfacetruque.py <nb_faces> <nb_tirages> <poids_1> ... <poids_N>
  ```
* **Paquet de dés** :
  ```bash
  python3 src/paquetde.py <nb_tirages> <faces_de1> <faces_de2> ...
  ```

---

### 3. Exécution des tests

Pour vérifier l'ensemble du projet et s'assurer que toutes les classes fonctionnent correctement :

```bash
python3 src/test_tp3.py
```
