import numpy as np


class Cluster:
    def __init__(self, red, black, white):
        self.red = red
        self.blacks = black
        self.white = white

    def is_biedronka_cluster(self):
        return not (self.red.distance(self.white) > np.sqrt(
            (self.white.get_height() / 3) ** 2 + (self.white.get_width() / 3) ** 2) or
                    self.red.get_width() * self.red.get_height() * 1.2 < self.white.get_width() * self.white.get_height()
                    or len(self.blacks) > 5)

    def get_boxes(self):
        boxes = [self.red, self.white]
        boxes.extend(self.blacks)
        return boxes
