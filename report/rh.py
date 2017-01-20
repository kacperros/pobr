import cv2
import reworked.Box
import reworked.colorspace_converters as cs_conv
from reworked.BoxesFilter import BoxesFilter
from reworked.ClustersGrouper import ClustersGrouper
import reworked.box_drawer as bdraw
from reworked.threshold import HSVThresholder, PixelHThreshold, PixelVThreshold, PixelSThreshold
from reworked.Colors import BColors
from reworked.BoundingBoxesBuilder import BoundingBoxesBuilder
import cv2
import copy
import numpy as np
import reworked.simple_resize as scaler
import reworked.filtering as filtr


bgr_image = cv2.imread('2_filtered/' + str(8) + '.jpg')
hsv_image = cs_conv.bgr2hsv(copy.copy(bgr_image))
print('Inverted than converted to HSV')
thresholder = HSVThresholder(copy.copy(hsv_image))
print('Created thresholder')

# r_bottom_image = thresholder.threshold(
#     [PixelHThreshold(0, 10), PixelVThreshold(0.5, 1.0), PixelSThreshold(0.3, 1.0)])
# r_bottom_image = cs_conv.hsv2bgr(r_bottom_image)
# cv2.imshow('red_bot_pre', r_bottom_image)
# # for i in range(0, 10):
# #     r_bottom_image = filtr.filter_ranking(r_bottom_image, 0)
# cv2.imshow('red_bot_post', r_bottom_image)
# print('Red bottom thresh done')


r_top_image = thresholder.threshold(
    [PixelHThreshold(350, 360), PixelVThreshold(0.5, 1.0), PixelSThreshold(0.3, 1.0)])
r_top_image = cs_conv.hsv2bgr(r_top_image)
cv2.imwrite('red_top_pre.jpg', r_top_image)
for j in range(0, 4):
    r_top_image = filtr.filter_ranking(r_top_image, 0)
cv2.imwrite('red_top_post.jpg', r_top_image)
print('Red top thresh done')

cv2.waitKey(0)
cv2.destroyAllWindows()
