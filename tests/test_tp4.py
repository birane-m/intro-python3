import contextlib
import io
import math
import unittest

from tests.helpers import TP4, prime, run_cli


class PrimeTests(unittest.TestCase):
    def test_small_sieve_limits(self):
        for limit, expected in [(0, []), (1, []), (2, [2]), (3, [2, 3])]:
            with self.subTest(limit=limit):
                numbers = prime.NbPremier(limit)
                self.assertEqual(numbers.lprime, expected)
                self.assertEqual(len(numbers.est_prime), limit + 1)

    def test_sieve_matches_independent_trial_division(self):
        numbers = prime.NbPremier(1000)
        for value in range(1001):
            expected = value >= 2 and all(value % d for d in range(2, math.isqrt(value) + 1))
            self.assertEqual(numbers.est_nombre_premier(value), expected, value)

    def test_negative_numbers_are_not_prime(self):
        for value in [-1, -100, 0, 1]:
            self.assertFalse(prime.NbPremier(19).est_nombre_premier(value))

    def test_invalid_limits_and_queries(self):
        for limit in [-1, True, 2.5, "10"]:
            with self.subTest(limit=limit), self.assertRaises((TypeError, ValueError)):
                prime.NbPremier(limit)
        for value in [True, 2.5, "3"]:
            with self.assertRaises(TypeError):
                prime.NbPremier(20).est_nombre_premier(value)

    def test_above_limit_is_rejected(self):
        numbers = prime.NbPremier(10)
        with self.assertRaises(prime.ParameterTooHighValue):
            numbers.est_nombre_premier(11)
        with self.assertRaises(prime.ParameterTooHighValue):
            numbers.decomposition_factors(11)

    def test_factorizations_reconstruct_every_number(self):
        numbers = prime.NbPremier(500)
        for value in range(2, 501):
            factors = numbers.decomposition_factors(value)
            self.assertEqual(math.prod(factors), value)
            self.assertEqual(factors, sorted(factors))
            self.assertTrue(all(numbers.est_nombre_premier(factor) for factor in factors))

    def test_decomposition_domain(self):
        for value in [-1, 0, 1, True, 2.5]:
            with self.subTest(value=value), self.assertRaises((TypeError, ValueError)):
                prime.NbPremier(20).decomposition_factors(value)

    def test_subject_decomposition_output(self):
        for value, expected in [(68, "68=2*2*17\n"), (67, "67=67\n")]:
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                prime.NbPremier(value).decomposition(value)
            self.assertEqual(stream.getvalue(), expected)

    def test_goldbach_pairs_are_valid_and_complete(self):
        numbers = prime.NbPremier(1000)
        pairs = numbers.goldbach_pairs()
        self.assertEqual(set(pairs), set(range(4, 1001, 2)))
        for value, (a, b) in pairs.items():
            self.assertEqual(a + b, value)
            self.assertTrue(numbers.est_nombre_premier(a))
            self.assertTrue(numbers.est_nombre_premier(b))
        self.assertEqual(prime.NbPremier(3).goldbach_pairs(), {})

    def test_goldbach_cli_exact_format(self):
        result = run_cli(TP4 / "src/goldbach.py", 10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "4=2+2\n6=3+3\n8=3+5\n10=3+7\n")
        self.assertEqual(result.stderr, "")

    def test_decomposition_cli_exact_format(self):
        result = run_cli(TP4 / "src/decomposition.py", 68)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "68=2*2*17\n")

    def test_bad_number_cli_arguments(self):
        for script, args in [("decomposition.py", [0]), ("decomposition.py", [1]),
                             ("goldbach.py", [-1]), ("goldbach.py", []), ("goldbach.py", ["abc"])]:
            with self.subTest(script=script, args=args):
                result = run_cli(TP4 / "src" / script, *args)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr)
                self.assertNotIn("Traceback", result.stderr)
