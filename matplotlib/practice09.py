import matplotlib.pyplot as plt
import numpy as np
import nafusion_utils as na
na.set_style()

x1 =np.random.randint(10, 35, 20)
x2 =np.random.randint(5, 45, 20)
x3 =np.random.randint(0, 40, 20)
y1 =np.random.randint(50, 100, 20)
y2 =np.random.randint(0, 40, 20)
y3 =np.random.randint(20, 80, 20)

plt.scatter(x1, y1, marker='*', s = 80)
plt.scatter(x2, y2, marker = '^', s = 60)
plt.scatter(x3, y3, marker = 'x', s = 30)

plt.show()