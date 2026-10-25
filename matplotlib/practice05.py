import matplotlib.pyplot as plt
import numpy as np
import nafusion_utils as na
na.set_style()

x = np.arange(10)
y = np.random.randint(-10,10,10)

plt.title('Result')
plt.xlabel('x axis')
plt.ylabel('y axis')

plt.plot(x, y)
plt.show()