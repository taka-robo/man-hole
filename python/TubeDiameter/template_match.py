import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('C:\\Users\\nct20\\Documents\\GitHub\\man-hole-Taka\\python\\TubeDiameter\\image_input\\real_tube.jpg',0)
img2 = img.copy()
template = cv2.imread('C:\\Users\\nct20\\Documents\\GitHub\\man-hole-Taka\\python\\TubeDiameter\\image_input\\real_tube_template_draw4.jpg',0)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

# image のセーブ
def save_image(image,meth):
    cv2.imwrite(
        'C:\\Users\\nct20\\Documents\\GitHub\\man-hole-Taka\\python\\TubeDiameter\\image_output\\template_test\\' + 'real_tube' + str(
            meth) +'.jpg', image)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    for meth in methods:
        img = img2.copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)

        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        plt.show()
        # lstripで左端の削除
        print(meth.lstrip("real_tubecv2."))  ##
        save_image(img,meth)