from copy import copy


class PixelThreshold:
    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def threshold(self, pixel):
        pass


class PixelHThreshold(PixelThreshold):
    def __init__(self, lower_bound, upper_bound):
        super().__init__(lower_bound, upper_bound)

    def threshold(self, pixel):
        if self.lower_bound <= pixel[0] <= self.upper_bound:
            return True
        return False


class PixelSThreshold(PixelThreshold):
    def __init__(self, lower_bound, upper_bound):
        super().__init__(lower_bound, upper_bound)

    def threshold(self, pixel):
        if self.lower_bound <= pixel[1] <= self.upper_bound:
            return True
        return False


class PixelVThreshold(PixelThreshold):
    def __init__(self, lower_bound, upper_bound):
        super().__init__(lower_bound, upper_bound)

    def threshold(self, pixel):
        if self.lower_bound <= pixel[2] <= self.upper_bound:
            return True
        return False


class HSVThresholder:
    def __init__(self, hsv_image):
        self.hsv_image = hsv_image

    def threshold(self, thresholds, img=None):
        if not img is None:
            img_hsv = copy(img)
        else:
            img_hsv = copy(self.hsv_image)
        rows, cols, channels = img_hsv.shape
        for i in range(0, rows):
            for j in range(0, cols):
                img_hsv[i, j] = apply_hsv_thresholds(img_hsv[i, j], thresholds)
        return img_hsv


def apply_hsv_thresholds(pixel, thresholds):
    pixel_passed = True
    for threshold in thresholds:
        if not threshold.threshold(pixel):
            pixel_passed = False
    if not pixel_passed:
        return [0, 0, 0]
    else:
        return pixel
