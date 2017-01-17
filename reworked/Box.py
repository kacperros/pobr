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
        own_h = self.row_max-self.row_min
        own_w = self.col_max - self.col_min
        own_center = (int(self.row_max - own_h/2), int(self.col_max - own_w/2))
        other_h = box.row_max-box.row_min
        other_w = box.col_max - box.col_min
        other_center = (box.row_max - other_h/2, box.col_max - other_w/2)
        dr = np.abs(own_center[0] - other_center[0])
        dc = np.abs(own_center[1] - other_center[1])
        dist_r = dr - (own_h/2 + other_h/2)
        dist_c = dc - (own_w/2 + other_w/2)
        if dist_r < 0 and dist_c < 0:
            return 0
        return np.sqrt(dist_c ** 2 + dist_r ** 2)
