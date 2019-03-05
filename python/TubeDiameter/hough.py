# -*- coding: utf-8 -*-
import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread('C:\\Users\\nct20\\Documents\\GitHub\\man-hole-Taka\\python\\TubeDiameter\\image_input\\sample.jpeg',1)

def save_image(image,param1,param2):
    cv2.imwrite(
        'C:\\Users\\nct20\\Documents\\GitHub\\man-hole-Taka\\python\\TubeDiameter\\image_output\\hough_test\\' + 'real_tube' + str(
            param1) +'-'+ str(param2) +'.jpg', image)
    cv2.destroyAllWindows()

#キー処理＆画面終了＆保存
def key_action(image,param2):

  k = cv2.waitKey(0)
  # ESC:プログラム終了,s:セーブ＋プログラム終了
  if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
  elif k == ord('s'): # wait for 's' key to save and exit
   cv2.imwrite('C:\\Users\\nct20\\Documents\\GitHub\\man-hole-Taka\\python\\TubeDiameter\\image_output\\'+ 'test' + str(param2) + '.jpg',image)
   cv2.destroyAllWindows()

  # 終了処理
  cv2.destroyAllWindows()

def Hough(img,param1,param2):
    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ガウシアンフィルタ
    gray = cv2.medianBlur(gray, 5)

    plt.imshow(gray, cmap='gray')
    plt.axis('off')
    plt.show()

    # ハフ変換による円検出
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=param1, param2=param2)
    circles = np.squeeze(circles, axis=0)  # (1, N, 3) -> (N, 3)
    cv2.imshow('Hough'+'-'+str(param1)+'-'+str(param2),img)
    #key_action(img,param2)
    save_image(img,param1,param2)

if __name__ == '__main__':
    for i in range(200, 202):
        for j in range(41,51):
            Hough(img,i,j)
            print('Hello')
