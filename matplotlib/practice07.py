import matplotlib.pyplot as plt
import numpy as np
import nafusion_utils as na
na.set_style()

x = np.linspace(0, 10, 500)
y = np.exp(x)
plt.plot(x, y)
plt.yscale('log')
plt.show()