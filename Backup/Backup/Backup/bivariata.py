__author__ = 'Utente'
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

x, y = np.mgrid[-100:100:1, -100:100:1]
#print x
#print y
pos = np.empty(x.shape + (2,))
pos[:, :, 0] = x
#print pos
pos[:, :, 1] = y

rv = multivariate_normal([30, 30], [[1000, 0.3], [0.3, 1000]])
print rv[0]
plt.contourf(x, y, rv.pdf(pos))

plt.show()