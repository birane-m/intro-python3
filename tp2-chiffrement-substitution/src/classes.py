import string
import random
import math


class PasswordError(Exception):
    """
    Classe de base pour les exceptions liées à un mot de passe invalide.
    Permet de capturer n'importe quelle erreur de mot de passe avec une seule clause except.
    """
    pass


class InvalidPasswordLengthError(PasswordError):
    """
    Exception levée lorsque le mot de passe n'a pas la bonne longueur (26 lettres requises).
    """

    def __init__(self, pwd):
        message = f"Longueur de mot de passe invalide : {len(pwd)} lettres reçues au lieu de 26."
        super().__init__(message)


class InvalidPasswordCharError(PasswordError):
    """
    Exception levée lorsque le mot de passe contient des caractères interdits (non-minuscules).
    """

    def __init__(self, pwd):
        message = f"Le mot de passe doit contenir uniquement des lettres minuscules (a-z). Reçu : '{pwd}'."
        super().__init__(message)


class DuplicateLetterError(PasswordError):
    """
    Exception levée lorsqu'une lettre apparaît plus d'une fois dans le mot de passe.
    """

    def __init__(self, pwd):
        message = f"Le mot de passe contient des lettres en doublon. Chaque lettre de a-z doit être unique."
        super().__init__(message)


class Encodeur:
    """
    Classe permettant de réaliser le chiffrement d'un texte par substitution monoalphabétique.
    """

    def __init__(self, pwd=None):
        """
        Initialise un objet Encodeur avec un mot de passe (alphabet désordonné de 26 lettres).

        :param pwd: Chaîne de 26 lettres minuscules uniques, ou None pour générer un mot de passe aléatoire.
        :raises InvalidPasswordLengthError: Si la longueur du mot de passe n'est pas de 26 lettres.
        :raises InvalidPasswordCharError: Si le mot de passe contient autre chose que des lettres minuscules.
        :raises DuplicateLetterError: Si des lettres sont répétées dans le mot de passe.
        """
        if pwd is None:
            self.password = list(string.ascii_lowercase)
            random.shuffle(self.password)
        else:
            pwd_str = "".join(pwd) if isinstance(pwd, list) else str(pwd)
            if len(pwd_str) != 26:
                raise InvalidPasswordLengthError(pwd_str)
            if not all(c in string.ascii_lowercase for c in pwd_str):
                raise InvalidPasswordCharError(pwd_str)
            if len(set(pwd_str)) != 26:
                raise DuplicateLetterError(pwd_str)
            self.password = list(pwd_str)


    def encode_string(self, input_string):
        """
        Chiffre une chaîne de caractères en appliquant la substitution alphabétique.
        Les minuscules deviennent les minuscules du mot de passe.
        Les majuscules deviennent les majuscules du mot de passe.
        Les caractères non-alphabétiques sont conservés intacts.

        :param input_string: La chaîne de caractères à encoder.
        :return: La chaîne encodée.
        """
        crypted_string = [
            self.password[ord(c) - ord('a')] if c.islower()
            else self.password[ord(c.lower()) - ord('a')].upper() if c.isupper()
            else c
            for c in input_string
        ]
        return ''.join(crypted_string)

    def encode_file(self, input_file, output_file):
        """
        Chiffre le contenu d'un fichier d'entrée et écrit le texte chiffré dans le fichier de sortie.

        :param input_file: Chemin du fichier d'entrée à lire.
        :param output_file: Chemin du fichier de sortie à écrire.
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as text_file:
                content = text_file.read()
        except IOError:
            print(f"Cannot open file {input_file}")
            return

        encoded_content = self.encode_string(content)

        try:
            with open(output_file, 'w', encoding='utf-8') as text_file:
                text_file.write(encoded_content)
        except IOError:
            print(f"Cannot open file {output_file}")


class Decodeur:
    """
    Classe permettant de déchiffrer un texte chiffré par substitution
    en utilisant le mot de passe de chiffrement original.
    """

    def __init__(self, password):
        """
        Initialise le décodeur en générant le mot de passe inverse associé au mot de passe de codage.

        :param password: Le mot de passe de codage original.
        """
        paires = zip(password, string.ascii_lowercase)
        paires_triees = sorted(paires)
        mdp_inverse = "".join([lettre_originale for lettre_codee, lettre_originale in paires_triees])
        self.decodeur = Encodeur(mdp_inverse)

    def decode_string(self, input_string):
        """
        Déchiffre une chaîne de caractères à l'aide de l'encodeur avec le mot de passe inverse.

        :param input_string: La chaîne chiffrée à déchiffrer.
        :return: La chaîne déchiffrée.
        """
        return self.decodeur.encode_string(input_string)

    def decode_file(self, input_file, output_file):
        """
        Déchiffre le contenu d'un fichier chiffré et enregistre le résultat dans le fichier de sortie.

        :param input_file: Chemin du fichier chiffré.
        :param output_file: Chemin du fichier de sortie.
        """
        return self.decodeur.encode_file(input_file, output_file)


class CodeBreaker:
    """
    Classe permettant d'attaquer et de casser un chiffrement par substitution sans connaître le mot de passe,
    selon les instructions de l'énoncé TP2 (Section 4).
    """

    def __init__(self, quadgram_file):
        """
        Initialise la classe en chargeant le fichier de quadgrammes.

        :param quadgram_file: Chemin du fichier contenant les quadgrammes et leurs fréquences.
        """
        self.dico_quads = {}
        try:
            with open(quadgram_file, "r", encoding="utf-8") as q_f:
                for line in q_f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        self.dico_quads[parts[0].lower()] = float(parts[1])
        except IOError:
            print(f"Cannot open file {quadgram_file}")

    def string_cleaner(self, input_string):
        """
        Nettoie une chaîne de caractères en ne conservant que les lettres de l'alphabet (a-z)
        mises en minuscules (supprime ponctuation, espaces, chiffres).

        :param input_string: La chaîne brute à nettoyer.
        :return: La chaîne nettoyée.
        """
        return "".join([c.lower() for c in input_string if c.isalpha()])

    def pwd_generator(self, mdp, i=None, j=None):
        """
        Permute deux lettres aux positions i et j dans un mot de passe.
        Si i et j ne sont pas fournis, ils sont choisis au hasard.

        :param mdp: Le mot de passe (chaîne de caractères ou liste).
        :param i: Indice de la première lettre (optionnel).
        :param j: Indice de la deuxième lettre (optionnel).
        :return: Un tuple (nouveau_mot_de_passe_str, i, j).
        """
        mdp_list = list(mdp)
        if i is None or j is None:
            i = random.randint(0, len(mdp_list) - 1)
            j = random.randint(0, len(mdp_list) - 1)

        mdp_list[i], mdp_list[j] = mdp_list[j], mdp_list[i]
        return "".join(mdp_list), i, j

    def score_calculator(self, input_string):
        """
        Calcule le score d'une chaîne de caractères nettoyée en effectuant
        la somme des log des fréquences de ses quadgrammes.

        :param input_string: Chaîne nettoyée (minuscules).
        :return: Score (float) de la chaîne.
        """
        list_quadgrams = [input_string[i:i + 4] for i in range(len(input_string) - 3)]
        return sum(math.log(self.dico_quads[quad]) for quad in list_quadgrams if quad in self.dico_quads)

    def code_breaker(self, crypted_string):
        """
        Casse le code de cryptage selon l'algorithme exact de la section 4.3 du sujet TP2 :
        1. Nettoyage du texte.
        2. Encodeur initialisé avec l'alphabet "abcdefghijklmnopqrstuvwxyz".
        3. Boucle d'échanges de 2 lettres jusqu'à 1000 permutations consécutives sans amélioration.
        4. Déchiffrement du texte complet avec le mot de passe trouvé.

        :param crypted_string: Chaîne de caractères chiffrée.
        :return: Tuple (mot_de_passe_trouve, texte_decrypte).
        """
        cleaned_string = self.string_cleaner(crypted_string)
        encoder = Encodeur(string.ascii_lowercase)

        current_decrypted = encoder.encode_string(cleaned_string)
        current_score = self.score_calculator(current_decrypted)

        stagnant_count = 0
        while stagnant_count < 1000:
            new_pwd, i, j = self.pwd_generator(encoder.password, None, None)
            encoder.password = list(new_pwd)

            cand_decrypted = encoder.encode_string(cleaned_string)
            cand_score = self.score_calculator(cand_decrypted)

            if cand_score > current_score:
                current_score = cand_score
                stagnant_count = 0
            else:
                # Annuler la permutation
                encoder.password[i], encoder.password[j] = encoder.password[j], encoder.password[i]
                stagnant_count += 1

        found_pwd = "".join(encoder.password)
        decrypted_full = encoder.encode_string(crypted_string)
        return found_pwd, decrypted_full

