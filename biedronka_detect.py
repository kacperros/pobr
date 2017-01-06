import colorspace_converters as cs_conv
import thresholders as ths


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
