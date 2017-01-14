from reworked.Colors import BColors
import sys
import numpy as np


class BoundingBoxesBuilder:
    def __init__(self, ):
        self.rows = 0
        self.cols = 0
        self.image_colors_view = []
        self.build_parts = []

    def builder(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.image_colors_view = np.full((rows, cols), BColors.NO.value)
        self.build_parts = []

    def append(self, image, color):
        self.build_parts.append((image, color))

    def build(self):
        pass



class Box:
    def __init__(self, box_color):
        self.box_color = box_color
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
