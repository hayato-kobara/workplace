import matplotlib.pyplot as plt
import numpy as np
import nafusion_utils as na
na.set_style()

data = [5, 3, 4, 2, 0, 3, 2, 1, 4, 6, 8, 5]

plt.plot(data)
plt.xticks(np.arange(0, 12, 1))
plt.yticks(np.arange(0, 10, 2))
plt.annotate('min value', xy = (4.2, 0), xytext = (8, 1),arrowprops = dict(facecolor = 'black', shrink = 0.05))
plt.show()