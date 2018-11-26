# -*- coding: utf-8 -*-
# Moving Image + Recognition of Red Color + Display of Maximum Area
# import the necessary packages
import cv2
import numpy as np
import threading
import json
import sys
import math

# フレームサイズ
FRAME_W = 800
FRAME_H = 600

#読み込むピクチャのファイル名
FILE_DIST = 200
FILE_DIST_COLOR = 100

#ノイズの輪郭を制限する定数
NOISE_MIN = 1e3
NOISE_MAX = 1e5

HSV_CONV = 0.70 #HSV, 360dankai => 256dankai , 250/360 = 0.7
#colorRange = [[RedMin],[RedMax],[BlueMin],[BlueMax],[GreenMin],[GreenMax],[PurpleMin][PurpleMax],[YellowMin][YellowMax]]
colorRange = [[30*HSV_CONV,330*HSV_CONV], [200*HSV_CONV,240*HSV_CONV], [80*HSV_CONV,150*HSV_CONV], [240*HSV_CONV,300*HSV_CONV],[40*HSV_CONV,80*HSV_CONV]]

#コマンドライン引数の受け取りのため
args = sys.argv
#-----------------------------------------------------------------------------------
# Loading still Image
def loading_still_image():
  image = cv2.imread('C:\\Users\\nct20\\Documents\\GitHub\\man-hole-Taka\\python\\TubeDiameter\\image_input\\100mm.jpg')
  #template = cv2.imread('C:\\Users\\nct20\\Documents\\GitHub\\man-hole-Taka\\python\\TubeDiameter\\image_input\\'+'color_sample_'+str(FILE_DIST_COLOR)+'mm.jpg')
  return image

#キー処理＆画面終了＆保存
def key_action(image):

  k = cv2.waitKey(0)
  # ESC:プログラム終了,s:セーブ＋プログラム終了
  if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
  elif k == ord('s'): # wait for 's' key to save and exit
   cv2.imwrite('C:\\Users\\nct20\\Documents\\GitHub\\man-hole-Taka\\python\\TubeDiameter\\image_output\\'+ 'test.jpg',image)
   cv2.destroyAllWindows()

  # 終了処理
  cv2.destroyAllWindows()

# Find Target Color
def find_rect_of_target_color(getImage, colorNum):
  hsv = cv2.cvtColor(getImage, cv2.COLOR_BGR2HSV_FULL)
  h = hsv[:, :, 0]
  s = hsv[:, :, 1]
  mask = np.zeros(h.shape, dtype=np.uint8)

  #Red
  if(colorNum == 1):
      mask[( (h < colorRange[0][0]) | (h > colorRange[0][1]) ) & (s > 128)] = 255
  #Blue
  elif(colorNum == 2):
      mask[((h > colorRange[1][0]) & (h < colorRange[1][1])) & (s > 60)] = 255
  #GReeeeN
  elif(colorNum == 3):
      mask[((h > colorRange[2][0]) & (h < colorRange[2][1])) & (s > 60)] = 255
  #Purple
  elif(colorNum == 4):
      mask[((h > colorRange[3][0]) & (h < colorRange[3][1])) & (s > 50)] = 255
  #Yellow
  elif(colorNum == 5):
      mask[((h > colorRange[4][0]) & (h < colorRange[4][1])) & (s > 128)] = 255

  getImage,contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  rects = []

  for i in range(0,2):
    for contour in contours:
      approx = cv2.convexHull(contour)
      rect = cv2.minAreaRect(approx) #回転を考慮した矩形の導出
      rects.append(np.array(rect))

  return rects

def draw_rotation_rectangle(rects,image):
  #rects [[0],[1]] [[0],[1]] = [[x],[y]] [[w],[h]]
  rect = tuple(max(rects, key = (lambda x: x[1][0] * x[1][1])))
  box = cv2.boxPoints(rect)
  box = np.int0(box)

  image = cv2.drawContours(image,[box],0,(0,0,255),2)
  #print ('w:' + str(rect[1][0]) + ',h:' + str(rect[1][1]))
  #print (str(COEFFICIENT_DF*((rect[1][0]*rect[1][1])**(INDEX_DF))))


# 指定した画像(path)の物体を検出し、外接矩形の画像を出力します
def detect_contour(src, blocksize, param1):
    # グレースケール画像へ変換
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # 2値化 元は50
    # retval, th1 = cv2.threshold(gray, GRAY_THRESHOLD, 255, cv2.THRESH_BINARY)
    # th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, param1)
    # cv2.imshow('Result',th3)

    # 輪郭を抽出
    #   contours : [領域][Point No][0][x=0, y=1]
    #   cv2.CHAIN_APPROX_NONE: 中間点も保持する
    #   cv2.CHAIN_APPROX_SIMPLE: 中間点は保持しない
    image, contours, hierarchy = cv2.findContours(th3, cv2.RETR_TREE,
                                                  cv2.CHAIN_APPROX_SIMPLE)  # ObjectTrackingは、findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 矩形検出された数（デフォルトで0を指定)
    detect_count = 0

    # 各輪郭に対する処理
    for i in range(0, len(contours)):

        # 輪郭の領域を計算
        area = cv2.contourArea(contours[i])
        epsilon = 0.1 * cv2.arcLength(contours[i], True)
        approx = cv2.approxPolyDP(contours[i], epsilon, True)

        # ノイズ（小さすぎる領域）と全体の輪郭（大きすぎる領域）を除外
        if area < NOISE_MIN or NOISE_MAX < area:
            continue

        # 外接矩形
        if len(contours[i]) > 0:
            rect = contours[i]
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(approx, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # 外接矩形毎に画像を保存
            # cv2.imwrite('{C:\Users\nct20\Documents\AIS}' + str(detect_count) + '.jpg', src[y:y + h, x:x + w])

            detect_count = detect_count + 1

    # 外接矩形された画像を表示
    # cv2.imshow('output', src)

    k = cv2.waitKey(0)
    # ESC:プログラム終了,s:セーブ＋プログラム終了
    if k == 27:  # wait for ESC key to exit
        cv2.destroyAllWindows()
    elif k == ord('s'):  # wait for 's' key to save and exit
        cv2.imwrite(
            'C:\\Users\\nct20\\Documents\\GitHub\\man-hole-Taka\\python\\TubeDiameter\\image_output\\real_tube' + args[1] + '_' + str(
                blocksize) + '_' + str(int(param1)) + '.jpg', approx)
        cv2.destroyAllWindows()

    # 終了処理
    cv2.destroyAllWindows()

if __name__ == '__main__':
 print('Loading Image File now')
 for i in range(1, 2):
 # Loading Still Image
  image = loading_still_image()

  detect_contour(image, 11, float(i))

  cv2.imshow('Recognition Now.', image)
  key_action(image)