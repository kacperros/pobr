import numpy as np


class Box:
    def __init__(self):
        self.row_min = 0
        self.row_max = 0
        self.col_min = 0
        self.col_max = 0


def box_2color_image(image):
    rows, cols, channels = image.shape
    conditions = np.full((rows, cols), -1)
    boxes = []
    for i in range(0, rows):
        for j in range(0, cols):
            if np.array_equal(image[i, j], [0, 0, 0]) or conditions[i, j] != -1:
                continue
            boxes.append(new_box(image, conditions))


def new_box(image, conditions):
    pass
