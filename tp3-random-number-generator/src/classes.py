"""Générateurs pédagogiques du TP3 : héritage, abstraction et composition."""

import abc
import copy
import math
from numbers import Real
from random import Random


class PoidsInvalidesError(ValueError):
    """Poids de mauvaise taille, négatifs, non finis ou de somme nulle."""


def _integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} doit être un entier.")
    if value < minimum:
        raise ValueError(f"{name} doit être supérieur ou égal à {minimum}.")
    return value


class MyRandom(abc.ABC):
    """Contrat de tirage ; chaque instance possède son propre générateur."""

    @abc.abstractmethod
    def __init__(self, seed=None):
        self.rand = Random(seed)

    @abc.abstractmethod
    def tirer(self, nb_tirs=1):
        """Retourne une liste de tirages ; zéro tirage donne une liste vide."""

    def __add__(self, other):
        if isinstance(other, PaquetDe):
            return PaquetDe(self) + other
        if isinstance(other, MyRandom):
            return PaquetDe(self) + other
        return NotImplemented


class DeNfacestruque(MyRandom):
    """Dé à N faces numérotées, avec des poids finis et non négatifs."""

    def __init__(self, n_f, poids=None, seed=None):
        self.nb_faces = _integer(n_f, "Le nombre de faces", minimum=1)
        values = [1] * n_f if poids is None else list(poids)
        if len(values) != n_f:
            raise PoidsInvalidesError(f"{n_f} poids attendus, {len(values)} reçus.")
        try:
            valid = all(isinstance(w, Real) and not isinstance(w, bool)
                        and math.isfinite(w) and w >= 0 for w in values)
            total = math.fsum(values) if valid else 0
        except (OverflowError, TypeError, ValueError) as exc:
            raise PoidsInvalidesError("Les poids doivent être des nombres finis.") from exc
        if not valid or not math.isfinite(total) or total <= 0:
            raise PoidsInvalidesError("Poids finis et non négatifs requis, de somme strictement positive.")
        self.poids = values
        super().__init__(seed)

    def tirer(self, nb_tirs=1):
        _integer(nb_tirs, "Le nombre de tirages")
        return self.rand.choices(range(1, self.nb_faces + 1), weights=self.poids, k=nb_tirs)


class De6facestruque(DeNfacestruque):
    def __init__(self, poids=None, seed=None):
        super().__init__(6, poids=poids, seed=seed)


class DeNfaces(DeNfacestruque):
    def __init__(self, n_f, seed=None):
        super().__init__(n_f, seed=seed)


class De6faces(DeNfaces):
    def __init__(self, seed=None):
        super().__init__(6, seed=seed)


class PaquetDe:
    """Composition de générateurs MyRandom.

    Le constructeur conserve les dés passés explicitement. L'addition crée des
    copies profondes de chaque dé, sans avancer les générateurs des opérandes.
    Copier un générateur copie aussi son état : cela n'assure pas l'indépendance
    statistique de deux dés copiés à partir du même état.
    """

    def __init__(self, *list_de):
        if any(not isinstance(de, MyRandom) for de in list_de):
            raise TypeError("Chaque élément du paquet doit hériter de MyRandom.")
        self.list_de = list(list_de)

    def __add__(self, other):
        if isinstance(other, PaquetDe):
            dice = self.list_de + other.list_de
        elif isinstance(other, MyRandom):
            dice = self.list_de + [other]
        else:
            return NotImplemented
        return PaquetDe(*(copy.deepcopy(de) for de in dice))

    def tirer(self, nb_tirs=1):
        _integer(nb_tirs, "Le nombre de tirages")
        return list(zip(*(de.tirer(nb_tirs) for de in self.list_de)))


class DeNfacesIllustrees(DeNfaces):
    """Dé dont les faces portent des étiquettes ou des objets."""

    def __init__(self, *elements, seed=None):
        self.elements = list(elements[0]) if len(elements) == 1 and isinstance(elements[0], (list, tuple)) else list(elements)
        if not self.elements:
            raise ValueError("Un dé illustré doit avoir au moins une face.")
        super().__init__(len(self.elements), seed=seed)

    def tirer(self, nb_tirs=1):
        return [self.elements[index - 1] for index in super().tirer(nb_tirs)]


class Piece(DeNfacesIllustrees):
    def __init__(self, seed=None):
        super().__init__("pile", "face", seed=seed)


class SacNBillesSansRemise(MyRandom):
    """Sac numéroté de 1 à N, rechargé après chaque cycle complet."""

    def __init__(self, nb_billes, seed=None):
        self.nb_billes = _integer(nb_billes, "Le nombre de billes", minimum=1)
        self.billes_restantes = []
        super().__init__(seed)

    def _recharger(self):
        self.billes_restantes = self.rand.sample(range(1, self.nb_billes + 1), self.nb_billes)

    def tirer(self, nb_tirs=1):
        _integer(nb_tirs, "Le nombre de tirages")
        results = []
        for _ in range(nb_tirs):
            if not self.billes_restantes:
                self._recharger()
            results.append(self.billes_restantes.pop())
        return results
