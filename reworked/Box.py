import sys
import numpy as np


class Box:
    def __init__(self, box_color):
        self.box_color = box_color
        self.row_min = sys.maxsize
        self.row_max = -1
        self.col_min = sys.maxsize
        self.col_max = -1
        self.pixel_coords = []
        self.border_pixels = []
        self.border_length = 0

    def add_point(self, row, col, is_border):
        if row > self.row_max:
            self.row_max = row
        if row < self.row_min:
            self.row_min = row
        if col > self.col_max:
            self.col_max = col
        if col < self.col_min:
            self.col_min = col
        self.pixel_coords.append((row, col))
        if is_border:
            self.border_length += 1
            self.border_pixels.append((row, col))

    def contains(self, box):
        return box.row_min > self.row_min and box.row_max < self.row_max \
               and box.col_min > self.col_min and box.col_max < self.col_max

    def get_width(self):
        return self.col_max - self.col_min

    def get_height(self):
        return self.row_max - self.row_min

    def distance(self, box):
        vertical_dist = self.__get_vertical_dist(box)
        horizontal_dist = self.__get_horizonta_dist(box)
        return np.sqrt(vertical_dist ** 2 + horizontal_dist ** 2)

    def __get_vertical_dist(self, box):
        if box.row_min > self.row_max:
            return box.row_min - self.row_max
        elif box.row_max < self.row_min:
            return self.row_min - box.row_max
        else:
            return 0

    def __get_horizonta_dist(self, box):
        if box.col_max < self.col_min:
            return self.col_min - box.col_max
        elif box.col_min > self.col_max:
            return box.col_min - self.col_max
        else:
            return 0
