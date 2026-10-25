import matplotlib.pyplot as plt
import numpy as np
import nafusion_utils as na
na.set_style()

x1 = np.random.randint(10, 20, 20)
x2 = np.random.randint(20, 30, 20)
y1 = np.random.randint(50, 100, 20)
y2 = np.random.randint(0, 40, 20)

plt.scatter(x1, y1)
plt.scatter(x2, y2)

plt.show()