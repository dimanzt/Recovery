__author__ = 'Utente'
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

x = np.linspace(0, 5, 10, endpoint=False)

#print x
#x =[0,1,2,3,4,5,6,7,8,9]
print x
#x = [[0,2],[2,4],[3,1],[4,2]]
y = multivariate_normal.pdf(x, mean=2.5, cov=1000);

print y

plt.plot(x, y)
plt.show()