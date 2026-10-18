import unittest

from tests.helpers import TP3, dice, run_cli


class DiceTests(unittest.TestCase):
    def test_abstract_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            dice.MyRandom()

    def test_dice_bounds_and_count(self):
        for faces in [1, 4, 6, 20]:
            values = dice.DeNfaces(faces, seed=4).tirer(100)
            self.assertEqual(len(values), 100)
            self.assertTrue(all(1 <= value <= faces for value in values))

    def test_zero_draws_are_allowed(self):
        for generator in [dice.De6faces(), dice.Piece(), dice.SacNBillesSansRemise(3), dice.PaquetDe()]:
            self.assertEqual(generator.tirer(0), [])

    def test_seed_reproduces_sequence(self):
        self.assertEqual(dice.De6faces(seed=1).tirer(20), dice.De6faces(seed=1).tirer(20))

    def test_drawing_in_batches_preserves_sequence(self):
        one, two = dice.De6faces(seed=2), dice.De6faces(seed=2)
        self.assertEqual(one.tirer(3) + one.tirer(4), two.tirer(7))

    def test_bad_face_counts_are_rejected(self):
        for count in [0, -1, 2.5, True, "6"]:
            with self.subTest(count=count), self.assertRaises((TypeError, ValueError)):
                dice.DeNfaces(count)

    def test_bad_draw_counts_are_rejected_for_every_generator(self):
        generators = [dice.De6faces(), dice.Piece(), dice.SacNBillesSansRemise(3), dice.PaquetDe(),
                      dice.PaquetDe(dice.De6faces())]
        for generator in generators:
            for count in [-1, 1.5, True, "3"]:
                with self.subTest(generator=type(generator).__name__, count=count), self.assertRaises((TypeError, ValueError)):
                    generator.tirer(count)

    def test_invalid_weights_are_rejected(self):
        for weights in [[1], [-1, 2], [0, 0], [float("nan"), 1], [float("inf"), 1], ["1", 2],
                        [True, 1], [1e308, 1e308]]:
            with self.subTest(weights=weights), self.assertRaises(dice.PoidsInvalidesError):
                dice.DeNfacestruque(2, weights)

    def test_zero_weight_face_is_never_drawn(self):
        self.assertEqual(dice.DeNfacestruque(2, [0, 0.5], seed=2).tirer(30), [2] * 30)

    def test_constructor_copies_weight_list(self):
        weights = [1, 2]
        generator = dice.DeNfacestruque(2, weights)
        weights[0] = -50
        self.assertEqual(generator.poids, [1, 2])

    def test_six_face_specializations(self):
        self.assertEqual(dice.De6facestruque([0, 0, 0, 0, 0, 1]).tirer(5), [6] * 5)
        self.assertEqual(dice.De6faces().nb_faces, 6)

    def test_illustrated_dice_and_coin(self):
        self.assertLessEqual(set(dice.DeNfacesIllustrees(["a", "b"], seed=1).tirer(50)), {"a", "b"})
        self.assertLessEqual(set(dice.Piece(seed=2).tirer(50)), {"pile", "face"})
        with self.assertRaises(ValueError):
            dice.DeNfacesIllustrees()

    def test_bag_cycles_and_partial_draws(self):
        generator = dice.SacNBillesSansRemise(5, seed=12)
        values = generator.tirer(2) + generator.tirer(13)
        for i in range(0, 15, 5):
            self.assertEqual(sorted(values[i:i + 5]), list(range(1, 6)))

    def test_bad_bag_sizes_are_rejected(self):
        for count in [0, -2, False, 1.2]:
            with self.subTest(count=count), self.assertRaises((TypeError, ValueError)):
                dice.SacNBillesSansRemise(count)

    def test_pack_transposes_draws(self):
        pack = dice.PaquetDe(dice.DeNfaces(1), dice.DeNfacestruque(2, [0, 1]))
        self.assertEqual(pack.tirer(3), [(1, 2)] * 3)
        self.assertEqual(dice.PaquetDe().tirer(4), [])

    def test_pack_rejects_non_generators(self):
        with self.assertRaises(TypeError):
            dice.PaquetDe(dice.De6faces(), 4)

    def test_all_additions_copy_dice_and_preserve_order(self):
        first, second = dice.DeNfaces(4, seed=1), dice.DeNfaces(8, seed=2)
        pack = dice.PaquetDe(first)
        combinations = [first + second, pack + second, first + dice.PaquetDe(second), pack + dice.PaquetDe(second)]
        for result in combinations:
            self.assertEqual([de.nb_faces for de in result.list_de], [4, 8])
            self.assertIsNot(result.list_de[0], first)
            self.assertIsNot(result.list_de[1], second)
            self.assertEqual(result.list_de[0].rand.getstate(), first.rand.getstate())
            result.list_de[0].tirer(3)
            self.assertEqual(first.rand.getstate(), dice.DeNfaces(4, seed=1).rand.getstate())
        self.assertEqual(len(pack.list_de), 1)

    def test_repeated_die_in_addition_has_distinct_objects(self):
        de = dice.De6faces(seed=1)
        pack = de + de
        self.assertIsNot(pack.list_de[0], pack.list_de[1])
        self.assertIsNot(pack.list_de[0], de)

    def test_invalid_additions_raise_type_error(self):
        for generator in [dice.De6faces(), dice.PaquetDe()]:
            with self.assertRaises(TypeError):
                generator + 4

    def test_cli_stdout_contains_only_draws(self):
        result = run_cli(TP3 / "src/denface.py", 6, 5, "--seed", 1)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(result.stdout.splitlines()), 5)
        self.assertTrue(all(1 <= int(x) <= 6 for x in result.stdout.splitlines()))
        self.assertEqual(result.stderr, "")

    def test_weighted_cli_accepts_float_weights(self):
        result = run_cli(TP3 / "src/denfacetruque.py", 2, 4, 0, 0.5, "--seed", 2)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "2\n" * 4)

    def test_pack_cli_is_reproducible(self):
        args = [TP3 / "src/paquetde.py", 5, 6, 8, 12, "--seed", 4]
        first, second = run_cli(*args), run_cli(*args)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(len(first.stdout.splitlines()), 5)
        for row in first.stdout.splitlines():
            self.assertEqual(len(row.split()), 3)
            self.assertTrue(all(1 <= int(value) <= maximum for value, maximum in zip(row.split(), [6, 8, 12])))

    def test_invalid_cli_arguments_are_errors_on_stderr(self):
        for script, args in [("denface.py", [0, 2]), ("denface.py", [6, -1]),
                             ("denfacetruque.py", [2, 3, -1, 2]), ("paquetde.py", [3, 0]),
                             ("denface.py", []), ("denface.py", ["six", 3])]:
            with self.subTest(script=script, args=args):
                result = run_cli(TP3 / "src" / script, *args)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr)
                self.assertNotIn("Traceback", result.stderr)
