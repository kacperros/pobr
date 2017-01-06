import numpy as np
import sys


class Box:
    def __init__(self):
        self.row_min = sys.maxsize
        self.row_max = -1
        self.col_min = sys.maxsize
        self.col_max = -1

    def add_point(self, row, col):
        if row > self.row_max:
            self.row_max = row
        if row < self.row_min:
            self.row_min = row
        if col > self.col_max:
            self.col_max = col
        if col < self.col_min:
            self.col_min = col


def box_2color_image(image):
    rows, cols, channels = image.shape
    conditions = np.full((rows, cols), False)
    boxes = []
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if np.array_equal(image[i, j], [0, 0, 0]) or conditions[i, j]:
                continue
            box = Box()
            conditions = new_box(box, image, conditions, (i, j))
            boxes.append(box)
    return boxes


def draw_boxes(image, boxes):
    for box in boxes:
        image = draw_box(image, box)
    return image


def draw_box(image, box):
    left_upper = (box.row_min, box.col_min)
    right_upper = (box.row_min, box.col_max)
    left_bottom = (box.row_max, box.col_min)
    right_bottom = (box.row_max, box.col_max)
    image = draw_line(image, left_bottom, left_upper)
    image = draw_line(image, left_bottom, right_bottom)
    image = draw_line(image, left_upper, right_upper)
    image = draw_line(image, right_upper, right_bottom)
    return image


def draw_line(image, point1, point2):
    start_point = point1
    end_point = point2
    if start_point[0] > end_point[0]:
        start_point = point2
        end_point = point1
    elif start_point[0] == end_point[0]:
        if start_point[1] > end_point[1]:
            start_point = point2
            end_point = point1
    for i in range(start_point[0], end_point[0] + 1):
        for j in range(start_point[1], end_point[1] + 1):
            image[i, j] = [0, 255, 0]
    return image


def new_box(box, image, conditions, start):
    unchecked_pixels = []
    checked_pixels = []
    counter = 0
    while True:
        counter+=1
        conditions[start[0], start[1]] = True
        checked_pixels.append(start)
        rows, cols, channels = image.shape
        # print((len(unchecked_pixels), len(checked_pixels), counter))
        if start[0] == rows - 1 or start[1] == cols - 1 or start[0] == 0 or start[1] == 0:
            if not np.array_equal(image[coords[0], coords[1]], [0, 0, 0]):
                box.add_point(start[0], start[1])
            if len(unchecked_pixels) == 0:
                return conditions
            start = unchecked_pixels.pop()
            continue
        box.add_point(start[0], start[1])
        for i in range(-1, 2):
            for j in range(-1, 2):
                coords = (start[0] + i, start[1] + j)
                if coords[0] == start[0] and coords[1] == start[1]:
                    continue
                if np.array_equal(image[coords[0], coords[1]], [0, 0, 0]):  # skip black
                    continue
                if coords in checked_pixels:  # skip checked
                    continue
                if coords not in unchecked_pixels:  # add unchecked
                    unchecked_pixels.append(coords)
        if len(unchecked_pixels) == 0:
            return conditions
        start = unchecked_pixels.pop()
    return conditions
