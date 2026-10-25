import matplotlib.pyplot as plt
import numpy as np
import nafusion_utils as na
na.set_style()

x = ['Sam', 'John', 'Kevin', 'Adam'] 
y = np.random.randint(0, 200,4)

plt.bar(x, y)
plt.show()