# -*- coding: utf-8 -*-
import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
pc = serial.Serial('COM3', 9600, timeout = 0.1)#接続場所は適宜変える
fig, ax = plt.subplots()
ax.set_xlabel("x[mm]")
ax.set_ylabel("y[mm]")
ax.grid()
ax.set_aspect(1)
while True:
    try:
        data = (pc.readline().rstrip()).decode('utf-8')
        temp = data.rsplit(",")
        if(len(temp)==2):
            step, radius = data.rsplit(",")
            step = float(step);radius = float(radius)
            theta = step*(360/200)*(np.pi/180)
            #print(theta);print(radius)
            x = radius*np.cos(theta);y=radius*np.sin(theta)
            print(x);print(y)
            ax.plot(x,y,".r")
            ax.set_xlim([-1000, 1000]);ax.set_ylim([-1000, 1000])
            plt.pause(.01)
    except KeyboardInterrupt:#まだ理解してないから多分使えてない
        pc.close()
        break
