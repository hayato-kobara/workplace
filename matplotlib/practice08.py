import matplotlib.pyplot as plt
import numpy as np
import nafusion_utils as na
na.set_style()

x = np.linspace(0, 2*np.pi, 500)
y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x, y1, label = 'sin')
plt.plot(x, y2, label = 'cos')

plt.ylim(-2, 2)


plt.legend(loc = 2)
plt.show()
