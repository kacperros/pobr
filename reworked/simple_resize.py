import numpy as np
import copy


def __compress_pixels(pixels):
    result = np.zeros(3)
    for i in range(0, 4):
        for j in range(0, 4):
            result = np.add(result, pixels[i, j].astype(int))
    result = np.divide(result, np.full((1, 3), 16))
    return result


def simple_resize_by4(image):
    img = copy.copy(image)
    rows, cols, channels = img.shape
    rows -= (rows % 4)
    cols -= (cols % 4)
    img = img[0:rows, 0:cols]
    result_img = np.full((rows / 4, cols / 4, 3), 1)
    for i in range(0, int(rows / 4)):
        for j in range(0, int(cols / 4)):
            result_img[i, j] = __compress_pixels(img[i * 4:i * 4 + 4, j * 4:j * 4 + 4])
    return result_img
