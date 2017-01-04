import unittest
import colorspace_converters as cs_conv


class BiedronkaUnitTests(unittest.TestCase):
    def test_colorspace_converters_brg2hsv_pixel(self):
        pixel = [179, 155, 77]
        result = cs_conv._convert_pixel(pixel)
        self.assertAlmostEqual(result[0], 194, 1)
        self.assertAlmostEqual(result[1], 0.57, 3)
        self.assertAlmostEqual(result[2], 0.702, 3)