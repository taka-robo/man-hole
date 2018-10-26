import numpy as np
import matplotlib.pyplot as plt

file = "point_data/10_26/600mm_test"
csv = ".csv"
png = ".png"
data = np.loadtxt(file+csv, skiprows=0, delimiter=",")
print(data)
x = data[:, 1]
y = data[:, 2]
#Kenshyou you
firstDataX = data[0, 1]
firstDataY = data[0, 2]
DataX = data[50, 1]
DataY = data[50, 2]

print(x, y)
plt.plot(x,y,"o" ,label = "dot data")

#Draw First Dot and Quarter Dot
plt.scatter(firstDataX, firstDataY, 100, color='red')
plt.scatter(DataX, DataY, 100, color='red')

plt.xticks( np.arange(-400, 500, 100) )
plt.yticks( np.arange(-400, 500, 100) )
#plt.ylim(-500, 500)
#plt.xlim(-500,500)
plt.grid(True)
plt.legend()
plt.savefig(file+png)
plt.show()
