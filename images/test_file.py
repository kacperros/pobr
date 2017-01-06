import cv2

import Box
import biedronka_detect

test = 2
done = False
for i in range(1, 17):
    if test == 1:
        if i == 6 or i == 1 or i == 7:
            continue
        file_pre = str(i) + 'r.jpg'
        file_name = 'minified/' + file_pre
    elif test == 2:
        if i == 6 or i != 3:
            continue
        file_pre = str(i) + '.jpg'
        file_name = file_pre
    elif test == 3:
        if done:
            break
        done = True
        i = 14
        file_pre = str(i) + 'r.jpg'
        file_name = 'minified/' + file_pre
    else:
        file_name = ''
        file_pre = ''
    img = cv2.imread(file_name)
    img_white = biedronka_detect.find_white(img)
    img_red = biedronka_detect.find_red(img)
    # img = segment_detector.mark_regions(img)
    boxes = Box.box_2color_image(img_red)
    boxes2 = Box.box_2color_image(img_white)
    img_red = Box.draw_boxes(img_red, boxes)
    img_white = Box.draw_boxes(img_white, boxes2)
    cv2.imwrite('results/' + file_pre + 'r', img_red)
    cv2.imwrite('results/' + file_pre + 'w', img_red)

cv2.waitKey(0)
cv2.destroyAllWindows()
