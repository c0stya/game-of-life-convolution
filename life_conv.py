import numpy as np
from scipy.signal import convolve2d

field = np.random.randint(0, 2, size=(10, 10))
kernel = np.ones((3, 3))

for i in range(100):
    new_field = convolve2d(field, kernel, mode="same")
    field = (new_field == 3) + (new_field == 4) * field
