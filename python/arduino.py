# -*- coding: utf-8 -*-
import math
def CircleFitting(x,y):
    """最小二乗法による円フィッティングをする関数
        input: x,y 円フィッティングする点群

        output  cxe 中心x座標
                cye 中心y座標
                re  半径

        参考
        一般式による最小二乗法（円の最小二乗法）　画像処理ソリューション
        http://imagingsolution.blog107.fc2.com/blog-entry-16.html
    """

    sumx  = sum(x)
    sumy  = sum(y)
    sumx2 = sum([ix ** 2 for ix in x])
    sumy2 = sum([iy ** 2 for iy in y])
    sumxy = sum([ix * iy for (ix,iy) in zip(x,y)])

    F = np.array([[sumx2,sumxy,sumx],
                  [sumxy,sumy2,sumy],
                  [sumx,sumy,len(x)]])

    G = np.array([[-sum([ix ** 3 + ix*iy **2 for (ix,iy) in zip(x,y)])],
                  [-sum([ix ** 2 *iy + iy **3 for (ix,iy) in zip(x,y)])],
                  [-sum([ix ** 2 + iy **2 for (ix,iy) in zip(x,y)])]])

    T=np.linalg.inv(F).dot(G)

    cxe=float(T[0]/-2)
    cye=float(T[1]/-2)
    re=math.sqrt(cxe**2+cye**2-T[2])
    #print (cxe,cye,re)
    return (cxe,cye,re)
if __name__ == '__main__':from matplotlib.widgets import Button
import serial
import matplotlib.pyplot as plt
import numpy as np
import serial.tools.list_ports
pc = serial.Serial("COM3") #接続場所は適宜変える#windows version
pc.baudrate = 115200
x=[];y=[]
cx=0;cy=0;r=300
count=0;
while True:
    try:
        data = (pc.readline().rstrip()).decode('utf-8')
        temp = data.rsplit(",")
        if(len(temp)==2):
            count+=1
            step, radius = data.rsplit(",")
            step = float(step); radius = float(radius)
            theta = step*(360/200)*(np.pi/180)
            x.append(radius*np.cos(theta)); y.append(radius*np.sin(theta))
            if(count==399):
                (cxe, cye, re) = CircleFitting(x, y)
                print(cxe,cye,re)
                theta = np.arange(0, 2 * math.pi, 0.1)
                xe = []
                ye = []
                for itheta in theta:
                    xe.append(re * math.cos(itheta) + cxe)
                    ye.append(re * math.sin(itheta) + cye)
                xe.append(xe[0])
                ye.append(ye[0])
                plt.plot(x, y, "ob", label="raw data")
                plt.plot(xe, ye, "-r", label="estimated")
                plt.plot(cxe, cye, "xb", label="center")
                plt.axis("equal")
                plt.grid(True)
                plt.text(400,0,re,fontsize=20)
                plt.legend()
                plt.show()
    except KeyboardInterrupt:#まだ理解してないから多分使えてない
        pc.close()
        break
