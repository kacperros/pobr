from reworked.Box import Box
import numpy as np

from reworked.Cluster import Cluster
from reworked.Colors import BColors
import sys


class BoxesFilter:
    def __init__(self):
        self.boxes = {BColors.RED.value[0]: [], BColors.BLACK.value[0]: [], BColors.WHITE.value[0]: []}
        self.clusters = []

    def input(self, boxes_to_filter):
        for box in boxes_to_filter:
            self.boxes[box.box_color].append(box)

    def filter_boxes(self):
        self.__filter_out_bad_boxes()
        self.__remove_bad_whites()
        boxes = []
        for k, v in self.boxes.items():
            boxes.extend(v)
        return boxes

    def cluster_boxes(self):
        self.__group_black_red()
        self.__cluster_in_whites()
        return self.clusters

    def filter_cluster(self):
        self.__filter_out_bad_boxes()
        self.__group_black_red()
        self.__remove_bad_whites()
        self.__cluster_in_whites()
        return self.clusters

    def __filter_out_bad_boxes(self):
        for k, v in self.boxes.items():
            items = []
            for box in v:
                if not box.is_clusterable():
                    continue
                items.append(box)
            v = items
            self.boxes[k] = v

    def __group_black_red(self):
        for red in self.boxes[BColors.RED.value[0]]:
            blacks = []
            for black in self.boxes[BColors.BLACK.value[0]]:
                if red.contains(black):
                    blacks.append(black)
            if blacks:
                self.clusters.append(Cluster(red, blacks, None))

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
                if not cluster.red.contains(white):
                    if closest_distance > cluster.red.distance(white):
                        closest_white = white
                        closest_distance = cluster.red.distance(white)
            if closest_white is not None:
                cluster.white = closest_white

    def clear(self):
        self.boxes = {BColors.RED.value[0]: [], BColors.BLACK.value[0]: [], BColors.WHITE.value[0]: []}
