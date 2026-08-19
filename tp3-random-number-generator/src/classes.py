"""
Module classes.py
-----------------
Ce module contient la hiérarchie de classes pour la génération de nombres
aléatoires et la simulation de jets de dés (classiques, truqués, illustrés,
pièce de monnaie, sac de billes, et paquet de dés).

Conforme aux spécifications du TP3 - Introduction à Python.
"""

import abc
import copy
from random import Random


class PoidsInvalidesError(Exception):
    """Exception personnalisée levée lorsque le nombre de poids fournis
    ne correspond pas au nombre de faces du dé."""
    pass


class MyRandom(abc.ABC):
    """Classe abstraite de base pour les générateurs de nombres aléatoires.
    
    Elle encapsule un objet Random de la bibliothèque standard et impose
    l'implémentation de la méthode `tirer`.
    """

    @abc.abstractmethod
    def __init__(self, seed=None):
        """Constructeur abstrait.
        
        Args:
            seed: Graine d'initialisation du générateur aléatoire (par défaut None).
        """
        self.rand = Random(seed)

    @abc.abstractmethod
    def tirer(self, nb_tirs=1):
        """Méthode abstraite pour effectuer un ou plusieurs tirages.
        
        Args:
            nb_tirs (int): Nombre de tirages à effectuer (par défaut 1).
            
        Returns:
            list: Liste contenant les résultats des tirages.
        """
        pass

    def __add__(self, other):
        """Surcharge de l'opérateur d'addition `+` pour un dé.
        
        Permet les opérations :
        - dé + paquet  -> crée un nouveau PaquetDe contenant [dé, *paquet.list_de]
        - dé1 + dé2    -> crée un nouveau PaquetDe contenant [dé1, dé2]
        
        Args:
            other: Un objet `PaquetDe` ou une autre instance de `MyRandom`.
            
        Returns:
            PaquetDe: Un nouveau paquet de dés.
            
        Raises:
            TypeError: Si `other` n'est ni un dé (MyRandom) ni un PaquetDe.
        """
        if isinstance(other, PaquetDe):
            return PaquetDe(self) + other
        elif isinstance(other, MyRandom):
            return PaquetDe(self, other)
        else:
            raise TypeError(
                f"Un dé de type '{type(self).__name__}' ne peut être additionné "
                f"qu'avec un dé (MyRandom) ou un PaquetDe, pas avec '{type(other).__name__}'."
            )


class DeNfacestruque(MyRandom):
    """Classe représentant un dé truqué à N faces.
    
    Chaque face possède un poids spécifique déterminant sa probabilité d'apparition.
    """

    def __init__(self, n_f, poids=None, seed=None):
        """Constructeur du dé truqué à N faces.
        
        Args:
            n_f (int): Nombre de faces du dé.
            poids (list[int|float], optional): Poids de chaque face.
                Si None, les faces sont équiprobables.
            seed: Graine aléatoire.
            
        Raises:
            PoidsInvalidesError: Si la taille de la liste `poids` ne vaut pas `n_f`.
        """
        self.nb_faces = n_f

        if poids is None:
            self.poids = [1] * self.nb_faces
        elif len(poids) != n_f:
            raise PoidsInvalidesError(
                f"Impossible de créer le dé : {n_f} faces prévues, mais {len(poids)} poids fournis."
            )
        else:
            self.poids = poids

        super().__init__(seed)

    def tirer(self, nb_tirs=1):
        """Effectue `nb_tirs` tirages pondérés selon les poids des faces.
        
        Returns:
            list[int]: Résultats des tirages (valeurs entre 1 et N).
        """
        return self.rand.choices(
            list(range(1, self.nb_faces + 1)),
            weights=self.poids,
            k=nb_tirs
        )


class De6facestruque(DeNfacestruque):
    """Classe représentant un dé truqué à 6 faces."""

    def __init__(self, poids=None, seed=None):
        """Constructeur du dé truqué à 6 faces.
        
        Args:
            poids (list, optional): Liste de 6 poids. Si None, équiprobable.
            seed: Graine aléatoire.
        """
        super().__init__(6, poids=poids, seed=seed)


class DeNfaces(DeNfacestruque):
    """Classe représentant un dé équilibré (non truqué) à N faces.
    
    Hérite de `DeNfacestruque` avec des poids tous égaux (équiprobabilité).
    """

    def __init__(self, n_f, seed=None):
        """Constructeur du dé équilibré à N faces.
        
        Args:
            n_f (int): Nombre de faces du dé.
            seed: Graine aléatoire.
        """
        super().__init__(n_f, poids=None, seed=seed)


class De6faces(DeNfaces):
    """Classe représentant un dé équilibré à 6 faces."""

    def __init__(self, seed=None):
        """Constructeur du dé équilibré à 6 faces.
        
        Args:
            seed: Graine aléatoire.
        """
        super().__init__(6, seed=seed)


class PaquetDe:
    """Classe représentant un ensemble (paquet) de dés.
    
    Cette classe n'hérite pas de `MyRandom` mais contient une liste d'objets `MyRandom`.
    """

    def __init__(self, *list_de):
        """Constructeur d'un paquet de dés.
        
        Args:
            *list_de: Un ou plusieurs dés (instances héritant de `MyRandom`).
            
        Raises:
            TypeError: Si l'un des arguments ne hérite pas de `MyRandom`.
        """
        self.list_de = []
        for de in list_de:
            if not isinstance(de, MyRandom):
                raise TypeError(
                    f"Tous les éléments du paquet doivent hériter de MyRandom. "
                    f"Type invalide reçu : '{type(de).__name__}'."
                )
            self.list_de.append(de)

    def __add__(self, other):
        """Surcharge de l'opérateur `+` pour ajouter un dé ou un autre paquet.
        
        Utilise `copy.deepcopy` pour éviter toute dépendance directe ou mutation indésirable.
        
        Args:
            other: Un dé (`MyRandom`) ou un `PaquetDe`.
            
        Returns:
            PaquetDe: Un nouveau paquet contenant la combinaison des dés.
            
        Raises:
            TypeError: Si `other` n'est ni un `MyRandom` ni un `PaquetDe`.
        """
        if isinstance(other, PaquetDe):
            nouvelle_liste = copy.deepcopy(self.list_de + other.list_de)
            return PaquetDe(*nouvelle_liste)
        elif isinstance(other, MyRandom):
            nouvelle_liste = copy.deepcopy(self.list_de + [other])
            return PaquetDe(*nouvelle_liste)
        else:
            raise TypeError(
                f"L'élément à ajouter doit être une sous-classe de MyRandom ou un PaquetDe, "
                f"pas '{type(other).__name__}'."
            )

    def tirer(self, nb_tirs=1):
        """Effectue `nb_tirs` lancers pour l'ensemble des dés du paquet.
        
        Les résultats sont regroupés par lancer (transposition par zip) :
        le i-ème élément de la liste retournée contient le tuple des résultats
        de tous les dés pour le i-ème lancer.
        
        Args:
            nb_tirs (int): Nombre de lancers à effectuer (par défaut 1).
            
        Returns:
            list[tuple]: Liste de tuples représentant les résultats par lancer.
        """
        if not self.list_de:
            return []

        # Tirage pour chaque dé dans le paquet
        l_tirages = [de.tirer(nb_tirs) for de in self.list_de]

        # Regroupement par lancer via zip (*l_tirages)
        return list(zip(*l_tirages))


# --- Section 1.6 : Améliorations ---

class DeNfacesIllustrees(DeNfaces):
    """Dé non truqué à N faces où chaque face est associée à une étiquette ou un objet.
    
    Exemple :
        myde = DeNfacesIllustrees("rouge", "bleu", "vert")
    """

    def __init__(self, *elements, seed=None):
        """Constructeur du dé illustré.
        
        Args:
            *elements: Les étiquettes / objets associés aux faces.
                       Peut également être passé sous forme de liste d'éléments.
            seed: Graine aléatoire.
        """
        if len(elements) == 1 and isinstance(elements[0], (list, tuple)):
            self.elements = list(elements[0])
        else:
            self.elements = list(elements)

        if not self.elements:
            raise ValueError("Un dé illustré doit avoir au moins une face.")

        super().__init__(len(self.elements), seed=seed)

    def tirer(self, nb_tirs=1):
        """Effectue `nb_tirs` tirages et renvoie les étiquettes correspondantes.
        
        Returns:
            list: Liste des étiquettes tirées au hasard.
        """
        indices = super().tirer(nb_tirs)
        return [self.elements[idx - 1] for idx in indices]


class Piece(DeNfacesIllustrees):
    """Classe représentant une pièce de monnaie (Pile ou Face)."""

    def __init__(self, seed=None):
        """Constructeur d'une pièce de monnaie.
        
        Args:
            seed: Graine aléatoire.
        """
        super().__init__("pile", "face", seed=seed)


class SacNBillesSansRemise(MyRandom):
    """Classe simulant un sac de N billes numérotées de 1 à N, tirées sans remise.
    
    Lorsque le sac est vide, il se recharge automatiquement avec toutes les billes.
    """

    def __init__(self, nb_billes, seed=None):
        """Constructeur du sac de billes.
        
        Args:
            nb_billes (int): Nombre de billes dans le sac (de 1 à N).
            seed: Graine aléatoire.
        """
        super().__init__(seed)
        self.nb_billes = nb_billes
        self.billes_restantes = []

    def _recharger(self):
        """Recharge le sac en effectuant une permutation aléatoire des billes 1 à N."""
        self.billes_restantes = self.rand.sample(
            range(1, self.nb_billes + 1),
            self.nb_billes
        )

    def tirer(self, nb_tirs=1):
        """Tire `nb_tirs` billes du sac sans remise.
        
        Recharge le sac si nécessaire.
        
        Returns:
            list[int]: Numéros des billes tirées.
        """
        resultats = []
        for _ in range(nb_tirs):
            if not self.billes_restantes:
                self._recharger()
            resultats.append(self.billes_restantes.pop())
        return resultats
