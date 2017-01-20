import numpy as np
import copy

gaussian_matrix = np.array([[1, 2, 1],
                            [2, 4, 2],
                            [1, 2, 1]])


def filter_gaussian(image):
    img = copy.copy(image)
    rows, cols, channels = image.shape
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            img[i, j] = convolve(gaussian_matrix, image[i - 1:i + 2, j - 1:j + 2].astype(int))
    return img


def filter_median(image):
    img = copy.copy(image)
    rows, cols, channels = image.shape
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            img[i, j] = median(image[i - 1:i + 2, j - 1:j + 2].astype(int))
    return img


def median(pixels):
    pixels_list = []
    for i in range(0, 3):
        for j in range(0, 3):
            pixels_list.append([i, j, (int(pixels[i, j, 0]) + int(pixels[i, j, 1]) + int(pixels[i, j, 2])) / 3])
    pixels_list.sort(key=lambda x: x[2])
    return pixels[pixels_list[5][0], pixels_list[5][1]]


def convolve(filtr, pixels):
    res = np.zeros(3)
    for i in range(0, 3):
        for j in range(0, 3):
            res = np.add(res, pixels[i, j] * filtr[i, j])
    return np.divide(res, np.full(3, 16))
