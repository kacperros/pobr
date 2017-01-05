import unittest
import colorspace_converters as cs_conv


class BiedronkaUnitTests(unittest.TestCase):
    def test_colorspace_converters_brg2hsv_pixel(self):
        pixel = [179, 155, 77]
        result = cs_conv._convert_pixel_bgr2hsv(pixel)
        self.assertAlmostEqual(result[0], 194, 1)
        self.assertAlmostEqual(result[1], 0.57, 3)
        self.assertAlmostEqual(result[2], 0.702, 3)

    def test_colorspace_converters_hsv2bgr_pixel(self):
        pixel = [194, 0.57, 0.702]
        result = cs_conv._convert_pixel_hsv2bgr(pixel)
        self.assertEqual(result[0], 179)
        self.assertEqual(result[1], 155)
        self.assertEqual(result[2], 77)