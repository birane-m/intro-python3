import math
import random
import string
import tempfile
import unittest
from pathlib import Path

from tests.helpers import TP2, cipher, run_cli

KEY = "zyxwvutsrqponmlkjihgfedcba"


class CipherTests(unittest.TestCase):
    def test_known_substitution_and_case(self):
        self.assertEqual(cipher.Encodeur(KEY).encode_string("Abc XYZ! 123"), "Zyx CBA! 123")

    def test_roundtrip_with_accents_and_unicode(self):
        text = "Été à Paris, déjà ! Ελληνικά İ 😀\nHello Python 3!"
        self.assertEqual(cipher.Decodeur(KEY).decode_string(cipher.Encodeur(KEY).encode_string(text)), text)

    def test_random_permutations_roundtrip(self):
        text = string.ascii_letters + string.digits + "\néà!?"
        for seed in range(10):
            key = cipher.Encodeur(seed=seed).password
            self.assertEqual(cipher.Decodeur(key).decode_string(cipher.Encodeur(key).encode_string(text)), text)

    def test_encoder_and_decoder_reject_invalid_keys(self):
        cases = [("abc", cipher.InvalidPasswordLengthError),
                 ("abcdefghijklmnopqrstuvwxyzx", cipher.InvalidPasswordLengthError),
                 ("a" * 26, cipher.DuplicateLetterError),
                 (string.ascii_uppercase, cipher.InvalidPasswordCharError),
                 (string.ascii_lowercase[:-1] + "é", cipher.InvalidPasswordCharError),
                 (42, cipher.PasswordError), ([1] * 26, cipher.PasswordError)]
        for cls in (cipher.Encodeur, cipher.Decodeur):
            for key, error in cases:
                with self.subTest(cls=cls.__name__, key=key), self.assertRaises(error):
                    cls(key)

    def test_seed_does_not_mutate_global_random(self):
        state = random.getstate()
        self.assertEqual(cipher.Encodeur(seed=4).password, cipher.Encodeur(seed=4).password)
        self.assertEqual(random.getstate(), state)

    def test_utf8_file_roundtrip_and_parent_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, encoded, decoded = [Path(tmp) / name for name in ["in.txt", "a/enc.txt", "b/dec.txt"]]
            source.write_bytes("Bonjour, été !\r\nDeuxième ligne\n".encode("utf-8"))
            cipher.Encodeur(KEY).encode_file(source, encoded)
            cipher.Decodeur(KEY).decode_file(encoded, decoded)
            self.assertEqual(decoded.read_bytes(), source.read_bytes())

    def test_missing_file_raises_in_api(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(FileNotFoundError):
            cipher.Encodeur(KEY).encode_file(Path(tmp) / "missing", Path(tmp) / "out")

    def test_cli_file_failure_is_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            for script in ["encodage.py", "decodage.py"]:
                result = run_cli(TP2 / script, Path(tmp) / "missing", KEY, Path(tmp) / "out")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn("Erreur", result.stderr)

    def test_cli_roundtrip_from_elsewhere(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, encoded, decoded = [Path(tmp) / name for name in ["in", "a/enc", "b/dec"]]
            source.write_text("Hello, été!", encoding="utf-8")
            for script, start, end in [("encodage.py", source, encoded), ("decodage.py", encoded, decoded)]:
                result = run_cli(TP2 / script, start, KEY, end, cwd=tmp)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, "")
            self.assertEqual(decoded.read_bytes(), source.read_bytes())

    def test_cli_prevents_input_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "in"
            source.write_text("hello")
            result = run_cli(TP2 / "encodage.py", source, KEY, source)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(source.read_text(), "hello")


class BreakerTests(unittest.TestCase):
    def model(self, content="ABCD 100\nBCDE 10\n", seed=0):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "quadgrams.txt"
        path.write_text(content, encoding="utf-8")
        return cipher.CodeBreaker(path, seed=seed)

    def test_score_matches_subject_formula(self):
        breaker = self.model()
        self.assertAlmostEqual(breaker.score_calculator("abcde"), math.log(100) + math.log(10))
        self.assertEqual(breaker.score_calculator("zzzz"), 0)
        self.assertEqual(breaker.score_calculator("abc"), 0)

    def test_real_model_matches_reference_score(self):
        breaker = cipher.CodeBreaker(TP2 / "data/english_quadgrams.txt")
        text = (TP2 / "data/mystery_text.txt").read_text(encoding="utf-8")
        self.assertAlmostEqual(breaker.score_calculator(breaker.string_cleaner(text)), 12176.13, places=2)

    def test_cleaner_keeps_only_ascii_letters(self):
        self.assertEqual(self.model().string_cleaner("Ab C-12éİ!"), "abc")

    def test_model_missing_or_empty_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(FileNotFoundError):
            cipher.CodeBreaker(Path(tmp) / "missing")
        with self.assertRaises(ValueError):
            self.model("")

    def test_malformed_models_are_rejected(self):
        for content in ["ABCD 0", "ABCD -1", "ABCD nan", "ABCD inf", "ABC 10", "AB1D 3",
                        "ABCD nope", "ABCD", "ABCD 1 extra", "ABCD 2\nABCD 3"]:
            with self.subTest(content=content), self.assertRaises(ValueError):
                self.model(content)

    def test_explicit_swap_can_be_reversed(self):
        breaker = self.model()
        swapped, i, j = breaker.pwd_generator(string.ascii_lowercase, 0, 25)
        self.assertEqual((i, j), (0, 25))
        self.assertEqual(breaker.pwd_generator(swapped, i, j)[0], string.ascii_lowercase)

    def test_invalid_swap_indices_are_rejected(self):
        for i, j in [(0, None), (0, 0), (-1, 2), (26, 1), (False, 2)]:
            with self.subTest(i=i, j=j), self.assertRaises(ValueError):
                self.model().pwd_generator(string.ascii_lowercase, i, j)

    def test_search_is_reproducible_bounded_and_non_decreasing(self):
        results = []
        for _ in range(2):
            breaker = self.model(seed=12)
            results.append(breaker.code_breaker("Abcde, é!", max_iterations=20))
            self.assertEqual(breaker.last_search["iterations"], 20)
            self.assertEqual(breaker.last_search["stop_reason"], "iteration_limit")
            self.assertGreaterEqual(breaker.last_search["final_score"], breaker.last_search["initial_score"])
            self.assertTrue(results[-1][1].endswith(", é!"))
        self.assertEqual(results[0], results[1])

    def test_stagnation_limit_is_respected(self):
        breaker = self.model("AAAA 2\n")
        breaker.code_breaker("abcd", stagnation_limit=4)
        self.assertEqual(breaker.last_search["iterations"], 4)
        self.assertEqual(breaker.last_search["stop_reason"], "stagnation")

    def test_search_rejects_short_text_and_bad_limits(self):
        with self.assertRaises(ValueError):
            self.model().code_breaker("éab")
        for kwargs in [{"max_iterations": 0}, {"max_iterations": True}, {"stagnation_limit": None}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.model().code_breaker("abcd", **kwargs)

    def test_breaker_cli_summary(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            source, model, output, summary = [Path(tmp) / n for n in ("in", "model", "out/result", "out/summary.json")]
            source.write_text("abcde")
            model.write_text("ABCD 5\n")
            result = run_cli(TP2 / "cassercode.py", source, model, output, "--seed", 1,
                             "--max-iterations", 5, "--summary", summary)
            self.assertEqual(result.returncode, 0, result.stderr)
            metadata = json.loads(summary.read_text())
            self.assertEqual(metadata["iterations"], 5)
            self.assertEqual(metadata["seed"], 1)
            self.assertEqual(output.read_text(), cipher.Encodeur(metadata["decryption_key"]).encode_string("abcde"))

    def test_breaker_cli_missing_model_fails_without_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / "in", Path(tmp) / "out"
            source.write_text("abcdef")
            result = run_cli(TP2 / "cassercode.py", source, Path(tmp) / "missing", output)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())
