from reworked.Box import Box
import numpy as np
from reworked.Colors import BColors
import sys


class BoxesFilter:
    def __init__(self):
        self.boxes = {BColors.RED.value[0]: [], BColors.BLACK.value[0]: [], BColors.WHITE.value[0]: []}
        self.clusters = []

    def input(self, boxes_to_filter):
        for box in boxes_to_filter:
            self.boxes[box.box_color].append(box)

    def filter(self):
        self.__filter_out_bad_boxes()
        self.__remove_unpaired_black_reds()
        self.__remove_bad_whites()
        self.__cluster_in_whites()
        return self.clusters

    def __filter_out_bad_boxes(self):
        for k, v in self.boxes.items():
            items = []
            for box in v:
                if box.col_min < 0 or box.row_min < 0:
                    continue
                if box.col_max > 100000 or box.row_max > 100000:
                    continue
                if box.get_height() < 5 or box.get_width() < 5:
                    continue
                items.append(box)
            v = items
            self.boxes[k] = v

    def __remove_unpaired_black_reds(self):
        self.__group_black_red()

    def __group_black_red(self):
        for red in self.boxes[BColors.RED.value[0]]:
            blacks = []
            for black in self.boxes[BColors.BLACK.value[0]]:
                if red.contains(black):
                    blacks.append(black)
            if blacks:
                self.clusters.append((red, blacks, []))

    def __remove_bad_whites(self):
        whites = self.boxes[BColors.WHITE.value[0]]
        good_whites = []
        for white in whites:
            if white.get_height() < 5 or white.get_width() < 5:
                continue
            if not 0.7 <= white.get_height()/white.get_width() <= 1.4:
                continue
            if not 0.5 <= len(white.pixel_coords) / (white.get_height() * white.get_width()) <= 0.8:
                continue
            if not 50 <= white.border_length**2/len(white.pixel_coords) <= 150:
                continue
            good_whites.append(white)
        self.boxes[BColors.WHITE.value[0]] = good_whites

    def __cluster_in_whites(self):
        for cluster in self.clusters:
            closest_white = None
            closest_distance = sys.maxsize
            for white in self.boxes[BColors.WHITE.value[0]]:
                if not cluster[0].contains(white):
                    if closest_distance > cluster[0].distance(white):
                        closest_white = white
                        closest_distance = cluster[0].distance(white)
            if closest_white is not None:
                cluster[2].append(closest_white)

    def __get_remaining_boxes(self):
        boxes = []
        for cluster in self.clusters:
            boxes.append(cluster[0])
            boxes.extend(cluster[1])
            boxes.extend(cluster[2])
        return boxes

    def clear(self):
        self.boxes = {BColors.RED.value[0]: [], BColors.BLACK.value[0]: [], BColors.WHITE.value[0]: []}
