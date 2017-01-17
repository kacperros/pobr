from reworked.Box import Box
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
        #TODO: pair whites-blacks to remove bad whites
        self.__remove_far_small_whites()
        return self.clusters

    def __filter_out_bad_boxes(self):
        for k, v in self.boxes.items():
            for box in v:
                if box.col_min < 0 or box.row_min < 0:
                    del box
                if box.col_max > 100000 or box.row_max > 100000:
                    del box

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

    def __remove_far_small_whites(self):
        for cluster in self.clusters:
            closest_white = None
            closest_distance = sys.maxsize
            for white in self.boxes[BColors.WHITE.value[0]]:
                if not cluster[0].contains(white) and white.get_height() > 5 and \
                                        0.1 <= white.get_height()/cluster[0].get_height() <= 0.5:
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
