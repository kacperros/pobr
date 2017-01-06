import cv2
import numpy as np
import colorspace_converters
from copy import copy


def mark_regions(image):
    rows, cols, channels = image.shape
    result = copy(image)
    image = colorspace_converters.bgr2gray(image)
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if _check_for_border(image[i - 1:i + 2, j - 1:j + 2]):
                result[i, j] = [0, 255, 0]
    return result


def _check_for_border(image_slice):
    center_val = image_slice[1, 1, 0]
    for i in range(0, 2):
        for j in range(0, 2):
            if np.abs(center_val - image_slice[i, j, 0]) > 8:
                return True
    return False


def detect_regions(image):
    pass
