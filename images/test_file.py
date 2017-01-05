import cv2
import colorspace_converters as cs_conv
import thresholders as ths

img = cv2.imread("four_pix.png")

cs_conv.bgr2hsv(img)
ths.threshold_hues(img, [[0, 20], [344, 360]])
cs_conv.hsv2bgr(img)

cv2.imwrite('converted_img.png', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

