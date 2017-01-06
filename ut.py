import unittest
import colorspace_converters as cs_conv
import Box
import thresholders as ths
import cv2


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

    def test_thresholder_hue(self):
        img = cv2.imread("images/four_pix.png")
        img = cs_conv.bgr2hsv(img)
        img = ths.threshold_hues(img, [[0, 20], [340, 360]])
        img = cs_conv.hsv2bgr(img)
        self.assertListEqual(list(img[0, 0]), [0, 0, 0])
        self.assertListEqual(list(img[0, 1]), [0, 0, 0])
        self.assertListEqual(list(img[1, 0]), [0, 0, 255])
        self.assertListEqual(list(img[1, 1]), [255, 255, 255])

    def test_text_boxing(self):
        img = cv2.imread("images/boxing_text_img.png")
        boxes = Box.box_2color_image(img)
        self.assertEqual(len(boxes), 1)
        print("Done")
