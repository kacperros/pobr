import Box
import colorspace_converters as cs_conv
from reworked.BoxesFilter import BoxesFilter
from reworked.ClustersGrouper import ClustersGrouper
from reworked.threshold import HSVThresholder, PixelHThreshold, PixelVThreshold, PixelSThreshold
from reworked.Colors import BColors
from reworked.BoundingBoxesBuilder import BoundingBoxesBuilder
import cv2
import copy
import numpy as np


class BiedronkaDetector:
    def __init__(self, bgr_image):
        self.bgr_image = bgr_image
        print('Assigned Original')
        self.hsv_image = cs_conv.bgr2hsv(copy.copy(bgr_image))
        print('Assigned HSV')
        self.gray_image = cs_conv.bgr2gray(copy.copy(bgr_image))
        print('Assigned Gray')
        self.hsv_inverted = cs_conv.bgr2hsv(cs_conv.invert(copy.copy(bgr_image)))
        print('Assigned Inverted HSV')
        self.thresholder = HSVThresholder(copy.copy(self.hsv_image))
        print('Created Thresholder')
        self.bounding_boxes_builder = BoundingBoxesBuilder()
        self.bounding_boxes_builder.builder(bgr_image.shape[0], bgr_image.shape[1])
        self.boxes_filter = BoxesFilter()
        self.clusters_handler = ClustersGrouper()
        print('Created BBB')

    def detect(self):
        self.__threshold_image()
        boxes = self.bounding_boxes_builder.build()
        self.boxes_filter.input(boxes)
        clusters = self.boxes_filter.filter()
        self.clusters_handler.add_clusters(clusters)
        cluster_groups = self.clusters_handler.handle_clusters()
        ret = []
        for cluster_group in cluster_groups:
            cluster_group.clean_cluster()
            ret.append(cluster_group.box_cluster())
        return ret

    def __threshold_image(self):
        r_bottom_image = self.thresholder.threshold(
            [PixelHThreshold(0, 10), PixelVThreshold(0.5, 1.0), PixelSThreshold(0.3, 1.0)])
        self.bounding_boxes_builder.append(r_bottom_image, BColors.RED)
        print('Red bottom thresh done')
        r_top_image = self.thresholder.threshold(
            [PixelHThreshold(350, 360), PixelVThreshold(0.5, 1.0), PixelSThreshold(0.3, 1.0)])
        self.bounding_boxes_builder.append(r_top_image, BColors.RED)
        print('Red top thresh done')
        w_image = self.thresholder.threshold([PixelVThreshold(0.75, 1), PixelSThreshold(0, 0.2)])
        self.bounding_boxes_builder.append(w_image, BColors.WHITE)
        print('White thresh done')
        rev_b_image = self.thresholder.threshold([PixelVThreshold(0.65, 1), PixelSThreshold(0, 0.2)], self.hsv_inverted)
        self.bounding_boxes_builder.append(rev_b_image, BColors.BLACK)
        print('Black thresh done')

