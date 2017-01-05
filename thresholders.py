import numpy as np
import cv2


def threshold_hues(hsv_image, bounds):
    rows, cols, channels = hsv_image.shape
    for i in range(0, rows):
        for j in range(0, cols):
            passed = False
            for bounds_elem in bounds:
                if bounds_elem[0] <= hsv_image[i, j, 0] <= bounds_elem[1]:
                    passed = True
                    break
            if not passed:
                hsv_image[i, j, 2] = 0


def threshold_values(hsv_image, bounds):
    rows, cols, channels = hsv_image.shape
    for i in range(0, rows):
        for j in range(0, cols):
            passed = False
            for bounds_elem in bounds:
                if bounds_elem[0] <= hsv_image[i, j, 2] <= bounds_elem[1]:
                    passed = True
                    break
            if not passed:
                hsv_image[i, j, 2] = 0


def threshold_saturations(hsv_image, bounds):
    rows, cols, channels = hsv_image.shape
    for i in range(0, rows):
        for j in range(0, cols):
            passed = False
            for bounds_elem in bounds:
                if bounds_elem[0] <= hsv_image[i, j, 1] <= bounds_elem[1]:
                    passed = True
                    break
            if not passed:
                hsv_image[i, j, 2] = 0
