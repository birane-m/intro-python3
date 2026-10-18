"""Crible d'Ératosthène et traitements d'images demandés dans le TP4."""

from math import isqrt
from pathlib import Path


def _integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} doit être un entier.")
    if value < minimum:
        raise ValueError(f"{name} doit être supérieur ou égal à {minimum}.")
    return value


class ParameterTooHighValue(ValueError):
    """Valeur demandée supérieure à la limite du crible."""


class NbPremier:
    """Prépare les nombres premiers entre 0 et n, bornes incluses."""

    def __init__(self, n):
        self.est_prime, self.lprime, self.facteurs = self.eratosthene(n)

    def eratosthene(self, n):
        _integer(n, "La limite du crible")
        flags = [False] * (n + 1)
        flags[2:] = [True] * max(0, n - 1)
        factors = list(range(n + 1))
        for i in range(2, isqrt(n) + 1):
            if flags[i]:
                flags[i * i::i] = [False] * len(flags[i * i::i])
                # Mémorise un facteur premier, pas nécessairement le plus grand.
                factors[i * i::i] = [i] * len(factors[i * i::i])
        return flags, [i for i, prime in enumerate(flags) if prime], factors

    def _check_upper_bound(self, k):
        if k >= len(self.est_prime):
            raise ParameterTooHighValue(f"{k} dépasse la limite du crible ({len(self.est_prime) - 1}).")

    def est_nombre_premier(self, k):
        if isinstance(k, bool) or not isinstance(k, int):
            raise TypeError("Le nombre à tester doit être un entier.")
        self._check_upper_bound(k)
        return k >= 2 and self.est_prime[k]

    def goldbach_pairs(self):
        """Retourne un couple de premiers pour chaque pair de 4 à n.

        Une vérification sur cet intervalle fini ne prouve pas la conjecture.
        """
        pairs = {
            value: next(((first, value - first) for first in self.lprime
                         if first <= value // 2 and self.est_prime[value - first]), None)
            for value in range(4, len(self.est_prime), 2)
        }
        if any(pair is None for pair in pairs.values()):
            raise RuntimeError("Un entier pair sans décomposition a été rencontré.")
        return pairs

    def test_goldbach(self):
        for value, (first, second) in self.goldbach_pairs().items():
            print(f"{value}={first}+{second}")

    def decomposition_factors(self, k):
        """Retourne les facteurs premiers triés d'un entier k >= 2."""
        _integer(k, "Le nombre à décomposer", minimum=2)
        self._check_upper_bound(k)
        found = []
        while k > 1:
            factor = self.facteurs[k]
            found.append(factor)
            k //= factor
        return sorted(found)

    def decomposition(self, k):
        factors = self.decomposition_factors(k)
        print(f"{k}=" + "*".join(map(str, factors)))


class Image:
    """Image uint8, en BGR (OpenCV) ou en niveaux de gris."""

    def __init__(self, file_name):
        import cv2

        if not Path(file_name).is_file():
            raise FileNotFoundError(f"Image introuvable : {file_name}")
        try:
            self.im = cv2.imread(str(file_name))
        except cv2.error as exc:
            raise OSError(f"Impossible de lire l'image : {file_name}") from exc
        if self.im is None:
            raise FileNotFoundError(f"Impossible d'ouvrir l'image : {file_name}")

    @classmethod
    def from_array(cls, array):
        """Construit une image à partir d'une copie d'un tableau uint8 valide."""
        import numpy as np

        values = np.asarray(array)
        if values.dtype != np.uint8 or values.size == 0:
            raise ValueError("Un tableau uint8 non vide est requis.")
        if values.ndim not in (2, 3) or (values.ndim == 3 and values.shape[2] != 3):
            raise ValueError("Forme attendue : (hauteur, largeur) ou (hauteur, largeur, 3).")
        image = cls.__new__(cls)
        image.im = values.copy()
        return image

    def show_im(self, im=None, window_name="image"):
        """Ouvre une fenêtre ; nécessite un environnement graphique."""
        import cv2

        cv2.imshow(window_name, self.im if im is None else im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save(self, output_file):
        import cv2

        output = Path(output_file)
        output.parent.mkdir(parents=True, exist_ok=True)
        try:
            saved = cv2.imwrite(str(output), self.im)
        except cv2.error as exc:
            raise OSError(f"Format d'image non pris en charge ou écriture impossible : {output}") from exc
        if not saved:
            raise OSError(f"Impossible d'écrire l'image : {output}")

    def to_gray(self):
        """Moyenne des canaux, comme dans le sujet, puis troncature en uint8."""
        if self.im.ndim == 3:
            import numpy as np

            self.im = np.mean(self.im, axis=2).astype(np.uint8)

    def add_black_stripes(self, n):
        """Noircit une ligne sur n, en commençant par la première."""
        _integer(n, "L'espacement des bandes", minimum=1)
        self.im[::n] = 0

    def compute_contours(self, k):
        """Contraste max-min dans un carré de rayon k ; bordure laissée à zéro.

        Version pédagogique à boucles explicites, de coût O(H * W * (2k+1)^2).
        """
        import numpy as np

        _integer(k, "Le rayon du voisinage")
        if self.im.ndim != 2:
            raise ValueError("Convertir l'image en niveaux de gris avant le calcul des contours.")
        height, width = self.im.shape
        result = np.zeros_like(self.im)
        for i in range(k, height - k):
            for j in range(k, width - k):
                area = self.im[i - k:i + k + 1, j - k:j + k + 1]
                result[i, j] = int(np.max(area)) - int(np.min(area))
        self.im = result
