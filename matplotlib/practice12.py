import matplotlib.pyplot as plt
import numpy as np
import nafusion_utils as na
na.set_style()

data = [5, 3, 4, 2, 0, 3, 2, 1, 4, 6, 8, 5]

plt.plot(data)
plt.grid(True)

plt.show()