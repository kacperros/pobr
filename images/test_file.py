import cv2
import colorspace_converters as cs_conv
import thresholders as ths
import segment_detector
import biedronka_detect
import Box

test = 3
done = False
for i in range(1, 3):
    if test == 1:
        if i == 6 or i == 1:
            continue
        file_pre = str(i) + 'r.jpg'
        file_name = 'minified/' + file_pre
    elif test == 2:
        if i == 6 or i != 3:
            continue
        file_pre = str(i) + '.jpg'
        file_name = file_pre
    else:
        if done:
            break
        done = True
        i = 14
        file_pre = str(i) + 'r.jpg'
        file_name = 'minified/' + file_pre
    img = cv2.imread(file_name)
    img = biedronka_detect.find_red(img)
    img = segment_detector.mark_regions(img)
    Box.box_2color_image(img)
    cv2.imwrite('results/' + file_pre, img)

cv2.waitKey(0)
cv2.destroyAllWindows()
