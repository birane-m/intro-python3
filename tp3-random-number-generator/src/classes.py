import abc
from random import Random

class PoidsInvalidesError(Exception):
    """Exception levée quand le nombre de poids ne correspond pas au nombre de faces."""
    pass

class MyRandom(abc.ABC):
    """Classe mère abstraite représentant un générateur de nombres aléatoires."""
    
    @abc.abstractmethod
    def __init__(self, seed=None):
        self.rand = Random(seed)

    @abc.abstractmethod
    def tirer(self, nb_tirs=1):
        """Méthode abstraite définissant le comportement de tirage."""
        pass

class DeNfacestruque(MyRandom):
    """Classe de base pour un dé truqué à N faces."""
    def __init__(self, n_f, poids=None, seed=None):
        self.nb_faces = n_f 
        
        # Si aucun poids n'est fourni, on crée une liste de '1' (équiprobable)
        if poids is None:
            poids = [1] * self.nb_faces
        # Sinon, on vérifie que la liste fournie a la bonne taille
        elif len(poids) != n_f:
            raise PoidsInvalidesError(f"Impossible de créer le dé : {n_f} faces prévues, mais {len(poids)} poids fournis.")

        self.poids = poids
        super().__init__(seed)

    def tirer(self, nb_tirs=1):
        return self.rand.choices(list(range(1, self.nb_faces + 1)), weights=self.poids, k=nb_tirs)

class De6facestruque(DeNfacestruque):
    """Classe représentant un dé truqué à 6 faces."""
    def __init__(self, poids=None, seed=None):
        super().__init__(6, poids, seed)

class DeNfaces(DeNfacestruque):
    """Classe représentant un dé classique (non truqué) à N faces."""   
    def __init__(self, n_f, seed=None):
        super().__init__(n_f, None, seed)

class De6faces(DeNfaces):
    """Classe représentant un dé classique (non truqué) à 6 faces."""
    def __init__(self, seed=None):
        super().__init__(6, seed)