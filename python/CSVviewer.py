import numpy as np
import matplotlib.pyplot as plt

file = "600mm_706mm"
csv = ".csv"
png = ".png"
data = np.loadtxt(file+csv, skiprows=0, delimiter=",")
print(data)
x = data[:, 1]
y = data[:, 2]
print(x, y)
plt.plot(x,y,"ro")
plt.ylim(-500, 500)
plt.xlim(-500,500)
plt.legend()
plt.savefig(file+png)
plt.show()
