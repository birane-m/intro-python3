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


class Image:
    """
    Classe de manipulation d'image pour la deuxieme partie du TP4.

    L'image est stockee dans l'attribut `im` sous forme de tableau NumPy.
    OpenCV lit les images couleur avec trois canaux: bleu, vert, rouge.
    """

    def __init__(self, file_name):
        """
        Ouvre une image depuis le chemin donne.

        Args:
            file_name (str): Chemin du fichier image a ouvrir.

        Raises:
            FileNotFoundError: Si OpenCV ne parvient pas a lire le fichier.
        """
        import cv2

        self.im = cv2.imread(file_name)
        if self.im is None:
            raise FileNotFoundError(f"Impossible d'ouvrir l'image: {file_name}")

    def show_im(self, im=None, window_name="image"):
        """
        Affiche l'image dans une fenetre OpenCV.

        Args:
            im: Image a afficher. Si aucune image n'est fournie, affiche `self.im`.
            window_name (str): Nom de la fenetre d'affichage.
        """
        import cv2

        image_to_show = self.im if im is None else im
        cv2.imshow(window_name, image_to_show)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save(self, output_file):
        """
        Sauvegarde l'image courante dans un fichier.

        Args:
            output_file (str): Chemin du fichier de sortie.

        Raises:
            IOError: Si l'ecriture du fichier echoue.
        """
        import cv2

        if not cv2.imwrite(output_file, self.im):
            raise IOError(f"Impossible d'ecrire l'image: {output_file}")

    def to_gray(self):
        """
        Convertit une image couleur en noir et blanc.

        Si l'image est deja en noir et blanc, la methode ne fait rien.
        La conversion utilise la moyenne des trois canaux couleur en evitant
        les debordements de capacite des entiers `uint8`.
        """
        if len(self.im.shape) == 3:
            import numpy as np

            self.im = np.mean(self.im, axis=2).astype(np.uint8)

    def add_black_stripes(self, n):
        """
        Ajoute des bandes horizontales noires tous les `n` pixels.

        Args:
            n (int): Espacement entre deux bandes.

        Raises:
            ValueError: Si `n` n'est pas strictement positif.
        """
        if n <= 0:
            raise ValueError("n doit etre strictement positif.")

        self.im[::n] = 0

    def compute_contours(self, k):
        """
        Calcule les contours d'une image en noir et blanc.

        Pour chaque pixel suffisamment eloigne du bord, la valeur stockee est
        la difference entre le maximum et le minimum des pixels du voisinage
        carre de rayon `k`.

        Args:
            k (int): Rayon du voisinage utilise pour calculer le contour.

        Raises:
            ValueError: Si l'image est en couleur ou si `k` est negatif.
        """
        if len(self.im.shape) != 2:
            raise ValueError("L'image doit être en noir et blanc pour calculer les contours.")
        if k < 0:
            raise ValueError("k doit etre positif ou nul.")

        import numpy as np

        hauteur, largeur = self.im.shape
        temp_im = np.zeros_like(self.im)

        for i in range(k, hauteur - k):
            for j in range(k, largeur - k):
                voisinage = self.im[i - k:i + k + 1, j - k:j + k + 1]
                val_max = int(np.max(voisinage))
                val_min = int(np.min(voisinage))
                temp_im[i, j] = val_max - val_min

        self.im = temp_im.astype(np.uint8)
