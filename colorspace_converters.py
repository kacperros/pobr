import numpy as np
import cv2


def bgr2hsv(image):
    width, height = image.shape
    for i in range(0, width):
        for j in range(0, height):
            image[i, j] = _convert_pixel(image[i, j])


def _convert_pixel(pixel):
    b = pixel[0] / 255
    g = pixel[1] / 255
    r = pixel[2] / 255
    c_max = np.amax([b, g, r])
    c_min = np.amin([b, g, r])
    delta = c_max - c_min
    if delta == 0:
        h = 0
    elif c_max == r:
        h = 60 * (((g - b) / delta) % 6)
    elif c_max == g:
        h = 60 * (((b - r) / delta) + 2)
    else:
        h = 60 * (((r - g) / delta) + 4)
    if c_max == 0:
        s = 0
    else:
        s = delta / c_max
    return [round(h, 0), round(s, 3), round(c_max, 3)]
