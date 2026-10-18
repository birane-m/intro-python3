"""Substitution monoalphabétique et recherche locale selon l'énoncé du TP2.

Seules les lettres ASCII sont substituées. Les autres caractères sont conservés.
Ce chiffrement historique est un exercice, pas un outil de protection de données.
"""

import math
import random
import string
from pathlib import Path


class PasswordError(ValueError):
    """Clé de substitution invalide."""


class InvalidPasswordLengthError(PasswordError):
    def __init__(self, pwd):
        super().__init__(f"La clé doit contenir 26 lettres ; {len(pwd)} reçues.")


class InvalidPasswordCharError(PasswordError):
    def __init__(self, pwd):
        super().__init__("La clé doit contenir uniquement les lettres minuscules a-z.")


class DuplicateLetterError(PasswordError):
    def __init__(self, pwd):
        super().__init__("Chaque lettre de a-z doit apparaître une seule fois dans la clé.")


def validate_password(password) -> str:
    """Valide la clé originale, avant toute inversion ou substitution."""
    if isinstance(password, list):
        if not all(isinstance(c, str) for c in password):
            raise PasswordError("Les éléments de la clé doivent être des lettres.")
        password = "".join(password)
    if not isinstance(password, str):
        raise PasswordError("La clé doit être une chaîne ou une liste de lettres.")
    if len(password) != 26:
        raise InvalidPasswordLengthError(password)
    if not all(c in string.ascii_lowercase for c in password):
        raise InvalidPasswordCharError(password)
    if len(set(password)) != 26:
        raise DuplicateLetterError(password)
    return password


class Encodeur:
    """Chiffre avec une permutation de l'alphabet latin ; conserve la casse."""

    def __init__(self, pwd=None, *, seed=None):
        if pwd is None:
            self.password = list(string.ascii_lowercase)
            random.Random(seed).shuffle(self.password)
        else:
            self.password = list(validate_password(pwd))

    def encode_string(self, input_string):
        return "".join(
            self.password[ord(c) - ord("a")] if c in string.ascii_lowercase
            else self.password[ord(c) - ord("A")].upper() if c in string.ascii_uppercase
            else c
            for c in input_string
        )

    def encode_file(self, input_file, output_file):
        """Lit puis écrit en UTF-8 ; laisse remonter les erreurs de fichiers."""
        content = Path(input_file).read_bytes().decode("utf-8")
        encoded = self.encode_string(content)
        output = Path(output_file)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(encoded.encode("utf-8"))


class Decodeur:
    """Déchiffre à partir de la clé originale de chiffrement."""

    def __init__(self, password):
        password = validate_password(password)
        pairs = sorted(zip(password, string.ascii_lowercase))
        inverse = "".join(original for _, original in pairs)
        self.decodeur = Encodeur(inverse)

    def decode_string(self, input_string):
        return self.decodeur.encode_string(input_string)

    def decode_file(self, input_file, output_file):
        self.decodeur.encode_file(input_file, output_file)


class CodeBreaker:
    """Recherche locale par échanges de lettres et score de quadgrammes du sujet.

    Le score somme les logarithmes des fréquences brutes connues. Les quadgrammes
    absents contribuent zéro. La recherche n'assure pas de retrouver le texte initial.
    """

    def __init__(self, quadgram_file, *, seed=None):
        self.dico_quads = {}
        with Path(quadgram_file).open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                parts = line.split()
                if len(parts) != 2:
                    raise ValueError(f"Quadgrammes, ligne {line_number} : deux colonnes attendues.")
                quad, raw_frequency = parts
                quad = quad.lower()
                if len(quad) != 4 or any(c not in string.ascii_lowercase for c in quad):
                    raise ValueError(f"Quadgramme invalide à la ligne {line_number}.")
                frequency = float(raw_frequency)
                if not math.isfinite(frequency) or frequency <= 0:
                    raise ValueError(f"Fréquence non positive ou non finie à la ligne {line_number}.")
                if quad in self.dico_quads:
                    raise ValueError(f"Quadgramme répété à la ligne {line_number}.")
                self.dico_quads[quad] = frequency
        if not self.dico_quads:
            raise ValueError("Le fichier de quadgrammes est vide.")
        self._log_frequencies = {quad: math.log(value) for quad, value in self.dico_quads.items()}
        self.seed = seed
        self.rand = random.Random(seed)
        self.last_search = None

    def string_cleaner(self, input_string):
        return "".join(c.lower() for c in input_string if c in string.ascii_letters)

    def pwd_generator(self, mdp, i=None, j=None):
        letters = list(validate_password(mdp))
        if (i is None) != (j is None):
            raise ValueError("Fournir les deux indices, ou aucun.")
        if i is None:
            i, j = self.rand.sample(range(26), 2)
        if any(isinstance(k, bool) or not isinstance(k, int) or not 0 <= k < 26 for k in (i, j)):
            raise ValueError("Les indices doivent être des entiers entre 0 et 25.")
        if i == j:
            raise ValueError("Les deux indices doivent être distincts.")
        letters[i], letters[j] = letters[j], letters[i]
        return "".join(letters), i, j

    def score_calculator(self, input_string):
        quadgrams = [input_string[i:i + 4] for i in range(len(input_string) - 3)]
        scores = [self._log_frequencies.get(quad, 0.0) for quad in quadgrams]
        return sum(scores)

    def code_breaker(self, crypted_string, *, stagnation_limit=1000, max_iterations=None):
        """Retourne (clé de déchiffrement, texte candidat).

        Arrêt après 1000 échecs consécutifs par défaut, comme dans le TP.
        Une limite globale d'itérations peut être ajoutée explicitement.
        """
        for name, value in (("stagnation_limit", stagnation_limit), ("max_iterations", max_iterations)):
            if value is not None and (isinstance(value, bool) or not isinstance(value, int) or value <= 0):
                raise ValueError(f"{name} doit être un entier strictement positif.")
        if stagnation_limit is None:
            raise ValueError("stagnation_limit doit être un entier strictement positif.")
        cleaned = self.string_cleaner(crypted_string)
        if len(cleaned) < 4:
            raise ValueError("Il faut au moins quatre lettres a-z pour utiliser des quadgrammes.")
        encoder = Encodeur(string.ascii_lowercase)
        current_score = self.score_calculator(cleaned)
        initial_score = current_score
        stagnant = iterations = 0
        while stagnant < stagnation_limit and (max_iterations is None or iterations < max_iterations):
            new_pwd, i, j = self.pwd_generator(encoder.password)
            encoder.password = list(new_pwd)
            candidate_score = self.score_calculator(encoder.encode_string(cleaned))
            iterations += 1
            if candidate_score > current_score:
                current_score = candidate_score
                stagnant = 0
            else:
                encoder.password[i], encoder.password[j] = encoder.password[j], encoder.password[i]
                stagnant += 1
        self.last_search = {
            "seed": self.seed, "iterations": iterations,
            "stagnation_limit": stagnation_limit, "max_iterations": max_iterations,
            "initial_score": initial_score, "final_score": current_score,
            "stop_reason": "stagnation" if stagnant >= stagnation_limit else "iteration_limit",
        }
        return "".join(encoder.password), encoder.encode_string(crypted_string)
