import colorspace_converters as cs_conv
import thresholders as ths
import Box as box
from enum import Enum


class BiedronkaColor(Enum):
    RED = 1,
    BLACK = 2,
    WHITE = 3


def box_RWB(image):
    boxes = []
    boxes.extend(_box_image_B(image))
    boxes.extend(_box_image_R(image))
    boxes.extend(_box_image_W(image))
    return boxes


def _box_image_R(image):
    img = find_red(image)
    return box.box_2color_image(img, BiedronkaColor.RED)


def _box_image_B(image):
    img = find_black_ret_as_white(image)
    return box.box_2color_image(img, BiedronkaColor.BLACK)


def _box_image_W(image):
    img = find_white(image)
    return box.box_2color_image(img, BiedronkaColor.WHITE)


def find_red(bgr_img):
    img = cs_conv.bgr2hsv(bgr_img)
    img = ths.threshold_hues(img, [[0, 10], [350, 360]])
    img = ths.threshold_values(img, [[0.5, 1.0]])
    img = ths.threshold_saturations(img, [[0.3, 1.0]])
    img = cs_conv.hsv2bgr(img)
    return img


def find_white(image):
    img = cs_conv.bgr2hsv(image)
    img = ths.threshold_values(img, [[0.8, 1]])
    img = ths.threshold_saturations(img, [[0, 0.2]])
    img = cs_conv.hsv2bgr(img)
    return img


def find_black_ret_as_white(image):
    img = cs_conv.invert(image)
    img = cs_conv.bgr2hsv(img)
    img = ths.threshold_values(img, [[0.60, 1]])
    img = ths.threshold_saturations(img, [[0, 0.3]])
    img = cs_conv.hsv2bgr(img)
    return img
