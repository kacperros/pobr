from reworked.Colors import BColors
import sys
import numpy as np


class BoundingBoxesBuilder:
    def __init__(self, ):
        self.rows = 0
        self.cols = 0
        self.image_colors_view = []
        self.used = []
        self.build_parts = []
        self.boxes = []

    def builder(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.image_colors_view = np.full((rows, cols), BColors.NO.value[0])
        self.used = np.full((rows, cols), False)
        self.build_parts = []

    def append(self, image, color):
        self.build_parts.append((image, color))

    def build(self):
        self.__build_image_view()
        return self.__build_boxes()

    def __build_image_view(self):
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                for part in self.build_parts:
                    if np.any(part[0][i, j] != [0, 0, 0]):
                        self.image_colors_view[i, j] = part[1].value[0]

    def __build_boxes(self):
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if not self.used[i,j] and self.image_colors_view[i,j] != BColors.NO.value[0]:
                    self.__build_box_from(i, j)

    def __build_box_from(self, row, col):
        box_color = self.used[row, col]
        unchecked_points = [(row, col)]
        box = Box(box_color)
        while not unchecked_points:
            unchecked_points.pop()
            if self.__handle_point(row, col, box):
                unchecked_points.append()

    def __handle_point(self, row, col, box):
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
