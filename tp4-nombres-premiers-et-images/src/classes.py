class ParameterTooHighValue(Exception):
    """
    Exception levée lorsqu'un paramètre k demandé dépasse 
    la limite n définie lors de l'initialisation de la classe.
    """
    pass


class NbPremier:
    """
    Classe permettant de manipuler des nombres premiers via le crible d'Ératosthène.
    Offre des méthodes pour vérifier la primalité, tester la conjecture de Goldbach 
    et décomposer un nombre en facteurs premiers.
    """

    def __init__(self, n):
        """
        Initialise les structures de données jusqu'à l'entier n.
        
        Args:
            n (int): La limite supérieure pour le calcul des nombres premiers.
        """
        self.est_prime, self.lprime, self.facteurs = self.eratosthene(n)

    def eratosthene(self, n):
        """
        Génère les nombres premiers en utilisant le crible d'Ératosthène optimisé 
        avec le slicing Python. Garde également une trace des facteurs pour la décomposition.
        
        Args:
            n (int): La limite supérieure.
            
        Returns:
            tuple: (liste de booléens, liste des nombres premiers, liste des facteurs)
        """
        # Initialisation : 0 et 1 ne sont pas premiers, le reste est présumé vrai
        l = [False, False] + [True] * (n - 1)
        
        # Liste traçant le plus grand diviseur trouvé pour chaque nombre
        facteurs = list(range(n + 1))

        for i in range(2, n + 1):
            if l[i]:
                # On barre tous les multiples de i à partir de i*i
                l[i*i::i] = [False] * len(l[i*i::i])
                # On mémorise le facteur premier i dans les cases de ses multiples
                facteurs[i*i::i] = [i] * len(facteurs[i*i::i])

        # Extraction des nombres premiers identifiés
        lprime = [i for i in range(2, n + 1) if l[i]]

        return l, lprime, facteurs

    def est_nombre_premier(self, k):
        """
        Vérifie si un nombre k est premier en temps constant O(1).
        
        Args:
            k (int): Le nombre à tester.
            
        Raises:
            ParameterTooHighValue: Si k est supérieur à la limite n d'initialisation.
            
        Returns:
            bool: True si k est premier, False sinon.
        """
        if k > len(self.est_prime) - 1:
            raise ParameterTooHighValue(
                f"Valeur de k = {k} trop élevée. Saisir un entier <= {len(self.est_prime) - 1}."
            ) 
        
        return self.est_prime[k]

    def test_goldbach(self):
        """
        Vérifie la conjecture de Goldbach pour tous les nombres pairs entre 4 et n.
        Affiche le résultat sous le format strict demandé (ex: 4=2+2).
        """
        n = len(self.est_prime) - 1
        
        # Création du dictionnaire associant {p: (a, b)}
        dico = {
            p: next((a, p - a) for a in self.lprime if self.est_prime[p - a])
            for p in range(4, n + 1, 2)
        }

        # Affichage formaté
        for p in range(4, n + 1, 2):
            print(f"{p}={dico[p][0]}+{dico[p][1]}")

    def decomposition(self, k):
        """
        Affiche la décomposition en facteurs premiers d'un entier k.
        Utilise la trace mémorisée lors du crible pour une complexité optimale.
        
        Args:
            k (int): Le nombre à décomposer.
            
        Raises:
            ParameterTooHighValue: Si k est supérieur à la limite n d'initialisation.
        """
        if k > len(self.est_prime) - 1:
            raise ParameterTooHighValue(
                f"Valeur de k = {k} trop élevée. Saisir un entier <= {len(self.est_prime) - 1}."
            )

        n_origin = k
        facteurs_trouves = []

        # Remontée des facteurs successifs
        while k > 1:
            facteur = self.facteurs[k]
            facteurs_trouves.append(facteur)
            k = k // facteur

        facteurs_trouves.sort()
        str_facteurs = "*".join(map(str, facteurs_trouves))
        print(f"{n_origin}={str_facteurs}")


