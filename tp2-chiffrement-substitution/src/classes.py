import string
import random
import math


class Encodeur:
    """
    Classe permettant de réaliser le chiffrement d'un texte par substitution monoalphabétique.
    """

    def __init__(self, pwd=None):
        """
        Initialise un objet Encodeur avec un mot de passe (alphabet désordonné de 26 lettres).

        :param pwd: Chaîne de 26 lettres minuscules uniques, ou None pour générer un mot de passe aléatoire.
        """
        if pwd is None:
            self.password = list(string.ascii_lowercase)
            random.shuffle(self.password)
        else:
            self.password = list(pwd)

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
    en utilisant des fréquences de quadgrammes (descente de gradient / hill climbing).
    """

    def __init__(self, quadgram_file):
        """
        Initialise la classe en chargeant les quadgrammes et leurs scores depuis un fichier texte/CSV.

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
        mises en minuscules, en supprimant espaces, ponctuation, chiffres et caractères spéciaux.

        :param input_string: La chaîne brute à nettoyer.
        :return: La chaîne nettoyée.
        """
        return "".join([c.lower() for c in input_string if c.lower() in string.ascii_lowercase])

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
        Calcule le score d'une chaîne de caractères (supposée nettoyée) en effectuant
        la somme des log des fréquences de ses quadgrammes.

        :param input_string: Chaîne de caractères nettoyée (minuscules).
        :return: Score (float) de la chaîne.
        """
        list_quadgrams = [input_string[i:i + 4] for i in range(len(input_string) - 3)]
        scores = [self.dico_quads.get(quad, 1) for quad in list_quadgrams]
        return sum(math.log(s) for s in scores)

    def code_breaker(self, crypted_string, nb_restarts=10):
        """
        Casse le chiffrement par substitution d'un texte chiffré par algorithme de descente de gradient.

        :param crypted_string: Chaîne de caractères chiffrée.
        :param nb_restarts: Nombre de redémarrages (restarts) aléatoires pour éviter les maxima locaux.
        :return: Tuple (meilleur_mot_de_passe, texte_decrypte).
        """
        cleaned_string = self.string_cleaner(crypted_string)
        best_overall_score = -float('inf')
        best_overall_pwd = string.ascii_lowercase

        for restart in range(nb_restarts):
            if restart == 0:
                current_pwd = string.ascii_lowercase
            else:
                pwd_list = list(string.ascii_lowercase)
                random.shuffle(pwd_list)
                current_pwd = "".join(pwd_list)

            enc = Encodeur(current_pwd)
            current_decrypted = enc.encode_string(cleaned_string)
            current_score = self.score_calculator(current_decrypted)

            stagnant_count = 0
            max_stagnant = 1000

            while stagnant_count < max_stagnant:
                new_pwd, i, j = self.pwd_generator(current_pwd)
                enc.password = list(new_pwd)
                cand_decrypted = enc.encode_string(cleaned_string)
                cand_score = self.score_calculator(cand_decrypted)

                if cand_score > current_score:
                    current_score = cand_score
                    current_pwd = new_pwd
                    stagnant_count = 0
                else:
                    stagnant_count += 1
                    enc.password = list(current_pwd)

            if current_score > best_overall_score:
                best_overall_score = current_score
                best_overall_pwd = current_pwd

        final_enc = Encodeur(best_overall_pwd)
        decrypted_full = final_enc.encode_string(crypted_string)
        return best_overall_pwd, decrypted_full
