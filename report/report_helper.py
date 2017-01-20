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


def scale_image(image_number):
    image = cv2.imread('0_initial/' + str(image_number) + '.jpg')
    scaled = scaler.simple_resize_by4(image)
    cv2.imwrite('1_resized/' + str(image_number) + '.jpg', scaled)
    print('Scaled down image ' + str(image_number))


def filter_image(image_number):
    image = cv2.imread('1_resized/' + str(image_number) + '.jpg')
    image = filtr.filter_median(image)
    cv2.imwrite('2_filtered/' + str(image_number) + '.jpg', image)
    print('Filtered image' + str(image_number))


def threshold_image(image_number):
    bgr_image = cv2.imread('2_filtered/' + str(image_number) + '.jpg')
    hsv_image = cs_conv.bgr2hsv(copy.copy(bgr_image))
    print('Converted to HSV')
    hsv_inverted = cs_conv.bgr2hsv(cs_conv.invert(copy.copy(bgr_image)))
    print('Inverted than converted to HSV')
    thresholder = HSVThresholder(copy.copy(hsv_image))
    print('Created thresholder')

    r_bottom_image = thresholder.threshold(
        [PixelHThreshold(0, 10), PixelVThreshold(0.5, 1.0), PixelSThreshold(0.3, 1.0)])
    cv2.imwrite('3_thresholded/' + str(image_number) + '_red_bottom.jpg', cs_conv.hsv2bgr(copy.copy(r_bottom_image)))
    print('Red bottom thresh done')
    r_top_image = thresholder.threshold(
        [PixelHThreshold(350, 360), PixelVThreshold(0.5, 1.0), PixelSThreshold(0.3, 1.0)])
    cv2.imwrite('3_thresholded/' + str(image_number) + '_red_top.jpg', cs_conv.hsv2bgr(copy.copy(r_top_image)))
    print('Red top thresh done')
    w_image = thresholder.threshold([PixelVThreshold(0.75, 1), PixelSThreshold(0, 0.2)])
    cv2.imwrite('3_thresholded/' + str(image_number) + '_white.jpg', cs_conv.hsv2bgr(copy.copy(w_image)))
    print('White thresh done')
    rev_b_image = thresholder.threshold([PixelVThreshold(0.65, 1), PixelSThreshold(0, 0.2)], hsv_inverted)
    cv2.imwrite('3_thresholded/' + str(image_number) + '_black_rev.jpg', cs_conv.hsv2bgr(copy.copy(rev_b_image)))
    print('Black thresh done')
    print('Finished Thresholding image ' + str(image_number))
    return [r_bottom_image, r_top_image, w_image, rev_b_image, bgr_image]


def get_bounding_boxes(images, resized_img, image_number):
    bounding_boxes_builder = BoundingBoxesBuilder()
    bounding_boxes_builder.builder(resized_img.shape[0], resized_img.shape[1])
    bounding_boxes_builder.append(images[0], BColors.RED)
    bounding_boxes_builder.append(images[1], BColors.RED)
    bounding_boxes_builder.append(images[2], BColors.WHITE)
    bounding_boxes_builder.append(images[3], BColors.BLACK)
    print('All images input for BBB')
    boxes_built = bounding_boxes_builder.build()
    image = bdraw.draw_boxes(copy.copy(resized_img), boxes_built)
    cv2.imwrite('4_segmented/' + str(image_number) + '.jpg', image)
    print('Built bounding boxes')
    return boxes_built


def filter_boxes(boxes_to_filter, resized_img, image_number):
    boxes_filter = BoxesFilter()
    boxes_filter.input(boxes_to_filter)
    print('Started filtering boxes')
    result = boxes_filter.filter_boxes()
    image = bdraw.draw_boxes(copy.copy(resized_img), result)
    cv2.imwrite('5_seg_filtered/' + str(image_number) + '.jpg', image)
    print('Done filtering boxes')
    return result


def cluster_boxes(boxes_post_filter, resized_img, image_number):
    boxes_filter = BoxesFilter()
    boxes_filter.input(boxes_post_filter)
    print('Started clustering boxes')
    clusters2 = boxes_filter.cluster_boxes()
    print('Done clustering')
    boxes_from_clusters = []
    for cluster in clusters2:
        boxes_from_clusters.extend(cluster.get_boxes())
    image = bdraw.draw_boxes(copy.copy(resized_img), boxes_from_clusters)
    cv2.imwrite('6_seg_clustered/' + str(image_number) + '.jpg', image)
    return clusters2


def group_clusters(clusters_grouped, resized_img, image_number):
    clusters_grouper = ClustersGrouper()
    clusters_grouper.add_clusters(clusters_grouped)
    print('Started grouping clusters')
    groups = clusters_grouper.handle_clusters()
    print('Done grouping')
    k = 0
    for group in groups:
        image = bdraw.draw_boxes(copy.copy(resized_img), group.get_boxes())
        cv2.imwrite('7_cluster_grouped/' + str(image_number) + 'cluster' + str(k) + '.jpg', image)
        k += 1
    return groups


def finalize_clusters(groups, resized_img, image_number, number_tried):
    cluster_boxs = []
    print('Started finalizing')
    for group in groups:
        if not group.is_biedronka():
            group.clean_cluster()
            if not group.is_biedronka():
                number_tried += 1
                rework_apply_erosion(image_number, resized_img, number_tried)
        cluster_boxs.append(group.box_cluster())
    print('Done Finalizing')
    image = bdraw.draw_boxes(copy.copy(resized_img), cluster_boxs)
    cv2.imwrite('8_clustered_final/' + str(image_number) + '.jpg', image)


def rework_apply_erosion(image_number, image_scaled, number_tried):
    if number_tried > 3:
        return
    img_thresholded = threshold_image(image_number)
    reds = [cs_conv.hsv2bgr(img_thresholded[0]), cs_conv.hsv2bgr(img_thresholded[1])]
    for j in range(0, 6):
        for t in range(0, 2):
            reds[t] = filtr.filter_ranking(reds[t], 0)
    cv2.imwrite('3_thresholded/' + str(image_number) + '_red_bottom.jpg', reds[0])
    print('Red bottom thresh done')
    cv2.imwrite('3_thresholded/' + str(image_number) + '_red_bottom.jpg', reds[1])
    print('Red bottom thresh done')
    img_thresholded[0] = cs_conv.bgr2hsv(reds[0])
    img_thresholded[1] = cs_conv.bgr2hsv(reds[1])
    boxesr = get_bounding_boxes(img_thresholded, image_scaled, i)
    boxes_filteredr = filter_boxes(boxesr, image_scaled, i)
    clustersr = cluster_boxes(boxes_filteredr, image_scaled, i)
    cluster_groupsr = group_clusters(clustersr, image_scaled, i)
    finalize_clusters(cluster_groupsr, image_scaled, i, number_tried)


scale = False
mfiltr = True
for i in range(1, 12):
    print('Right away, Sir')
    if scale:
        scale_image(i)
    resized = cv2.imread('1_resized/' + str(i) + '.jpg')
    if mfiltr:
        filter_image(i)
    thresholded = threshold_image(i)
    boxes = get_bounding_boxes(thresholded, resized, i)
    boxes_filtered = filter_boxes(boxes, resized, i)
    clusters = cluster_boxes(boxes_filtered, resized, i)
    cluster_groups = group_clusters(clusters, resized, i)
    finalize_clusters(cluster_groups, resized, i, 0)
    print('Done Sir')
