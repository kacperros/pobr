import numpy as np
import cv2


def bgr2hsv(image):
    rows, cols, channels = image.shape
    image = image.astype(float)
    for i in range(0, rows):
        for j in range(0, cols):
            image[i, j] = _convert_pixel_bgr2hsv(image[i, j])
    return image


def _convert_pixel_bgr2hsv(pixel):
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


def hsv2bgr(hsv_image):
    rows, cols, channels = hsv_image.shape
    for i in range(0, rows):
        for j in range(0, cols):
            hsv_image[i, j] = _convert_pixel_hsv2bgr(hsv_image[i, j])
    hsv_image = hsv_image.astype(int)
    return hsv_image


def _convert_pixel_hsv2bgr(hsv_pix):
    c = hsv_pix[2] * hsv_pix[1]
    x = c * (1 - np.abs((hsv_pix[0] / 60) % 2 - 1))
    m = hsv_pix[2] - c
    if 0 <= hsv_pix[0] < 60:
        rgb = [c, x, 0]
    elif 60 <= hsv_pix[0] < 120:
        rgb = [x, c, 0]
    elif 120 <= hsv_pix[0] < 180:
        rgb = [0, c, x]
    elif 180 <= hsv_pix[0] < 240:
        rgb = [0, x, c]
    elif 240 <= hsv_pix[0] < 300:
        rgb = [x, 0, c]
    else:
        rgb = [c, 0, x]
    return [round((rgb[2] + m) * 255, 0), round((rgb[1] + m) * 255, 0), round((rgb[0] + m) * 255, 0)]


def bgr2gray(image):
    rows, cols, channels = image.shape
    for i in range(0, rows):
        for j in range(0, cols):
            image[i, j] = [
                (image[i, j, 0] + image[i, j, 1] + image[i, j, 2]) / 3,
                (image[i, j, 0] + image[i, j, 1] + image[i, j, 2]) / 3,
                (image[i, j, 0] + image[i, j, 1] + image[i, j, 2]) / 3
            ]
    return image
