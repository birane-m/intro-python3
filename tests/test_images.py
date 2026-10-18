import tempfile
import unittest
from pathlib import Path

from tests.helpers import TP4, prime, run_cli

try:
    import cv2
    import numpy as np
    IMAGE_DEPENDENCIES = True
except ImportError:
    IMAGE_DEPENDENCIES = False


@unittest.skipUnless(IMAGE_DEPENDENCIES, "Installer les dépendances du TP4 pour les tests d'images.")
class ImageTests(unittest.TestCase):
    def test_mean_channels_without_overflow(self):
        array = np.array([[[255, 255, 255], [0, 30, 60], [1, 2, 2]]], dtype=np.uint8)
        image = prime.Image.from_array(array)
        image.to_gray()
        np.testing.assert_array_equal(image.im, [[255, 30, 1]])
        self.assertEqual(image.im.dtype, np.uint8)

    def test_gray_conversion_is_idempotent(self):
        image = prime.Image.from_array(np.arange(9, dtype=np.uint8).reshape(3, 3))
        original = image.im.copy()
        image.to_gray()
        np.testing.assert_array_equal(image.im, original)

    def test_array_constructor_copies_input(self):
        array = np.ones((3, 4), dtype=np.uint8)
        image = prime.Image.from_array(array)
        image.im[:] = 0
        self.assertTrue(np.all(array == 1))

    def test_bad_arrays_are_rejected(self):
        for array in [np.zeros((3, 3)), np.zeros((0, 3), dtype=np.uint8),
                      np.zeros((3,), dtype=np.uint8), np.zeros((2, 2, 4), dtype=np.uint8)]:
            with self.subTest(shape=array.shape), self.assertRaises(ValueError):
                prime.Image.from_array(array)

    def test_stripes_on_gray_and_color(self):
        for shape in [(5, 4), (5, 4, 3)]:
            image = prime.Image.from_array(np.full(shape, 255, dtype=np.uint8))
            image.add_black_stripes(2)
            self.assertTrue(np.all(image.im[::2] == 0))
            self.assertTrue(np.all(image.im[1::2] == 255))

    def test_bad_stripe_steps_are_rejected(self):
        image = prime.Image.from_array(np.ones((3, 3), dtype=np.uint8))
        for value in [0, -1, True, 1.5]:
            with self.subTest(value=value), self.assertRaises((TypeError, ValueError)):
                image.add_black_stripes(value)

    def test_contours_known_pixels_and_zero_border(self):
        image = prime.Image.from_array(np.arange(25, dtype=np.uint8).reshape(5, 5))
        image.compute_contours(1)
        expected = np.zeros((5, 5), dtype=np.uint8)
        expected[1:-1, 1:-1] = 12
        np.testing.assert_array_equal(image.im, expected)

    def test_contours_maximum_range_does_not_overflow(self):
        array = np.zeros((3, 3), dtype=np.uint8)
        array[0, 0] = 255
        image = prime.Image.from_array(array)
        image.compute_contours(1)
        self.assertEqual(int(image.im[1, 1]), 255)
        self.assertEqual(int(image.im.sum()), 255)

    def test_zero_radius_and_oversized_neighborhood(self):
        for radius in [0, 3, 100]:
            image = prime.Image.from_array(np.ones((3, 3), dtype=np.uint8))
            image.compute_contours(radius)
            self.assertFalse(np.any(image.im))

    def test_invalid_contour_inputs(self):
        with self.assertRaises(ValueError):
            prime.Image.from_array(np.ones((3, 3, 3), dtype=np.uint8)).compute_contours(1)
        image = prime.Image.from_array(np.ones((3, 3), dtype=np.uint8))
        for radius in [-1, True, 0.5]:
            with self.subTest(radius=radius), self.assertRaises((TypeError, ValueError)):
                image.compute_contours(radius)

    def test_png_roundtrip_and_parent_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            array = np.arange(36, dtype=np.uint8).reshape(3, 4, 3)
            output = Path(tmp) / "new/image.png"
            prime.Image.from_array(array).save(output)
            np.testing.assert_array_equal(prime.Image(output).im, array)

    def test_missing_image(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(FileNotFoundError):
            prime.Image(Path(tmp) / "missing.png")

    def test_conversion_cli_saves_exact_grayscale_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / "in.png", Path(tmp) / "nested/out.png"
            array = np.array([[[255, 255, 255], [0, 30, 60]]], dtype=np.uint8)
            cv2.imwrite(str(source), array)
            result = run_cli(TP4 / "nb.py", source, output, cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            np.testing.assert_array_equal(cv2.imread(str(output), cv2.IMREAD_UNCHANGED), [[255, 30]])
            self.assertEqual(result.stdout, "")

    def test_conversion_cli_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "in.png"
            cv2.imwrite(str(source), np.zeros((2, 2, 3), dtype=np.uint8))
            for input_file, output in [(Path(tmp) / "missing", Path(tmp) / "out.png"),
                                       (source, source), (source, Path(tmp) / "out.invalidformat")]:
                with self.subTest(output=output):
                    result = run_cli(TP4 / "nb.py", input_file, output)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("Erreur", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual(result.stdout, "")

    def test_exploration_script_runs_from_elsewhere(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_cli(TP4 / "src/PremierContactNumpy.py", cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Broadcasting", result.stdout)
            self.assertIn("uint8", result.stdout)
