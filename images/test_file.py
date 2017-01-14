import cv2

import Box
import biedronka_detect

test = 1
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
        i = 2
        file_pre = str(i) + 'r.jpg'
        file_name = 'minified/' + file_pre
    else:
        file_name = ''
        file_pre = ''
    img = cv2.imread(file_name)
    boxes = biedronka_detect._box_image_B(img)
    img = Box.draw_boxes(img, boxes)
    cv2.imwrite('results/' + file_pre + 'rb.jpg', img)
    print(str(i))

cv2.waitKey(0)
cv2.destroyAllWindows()
