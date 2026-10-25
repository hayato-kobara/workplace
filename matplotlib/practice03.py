import matplotlib.pyplot as plt
import numpy as np
import nafusion_utils as na
na.set_style()

data = np.random.randint(0, 10, 10)
plt.hist(data)

plt.show()