__author__ = 'Utente'
from numpy import *
import math
from matplotlib.mlab import bivariate_normal
# covariance matrix
sigma = matrix([[1,0],[0,1]])
# mean vector
print sigma
mu = array([50,50])
print mu
# input
x = array([50,50])
print x
def norm_pdf_multivariate(x, mu, sigma):
  size = len(x)
  print 'size x: ' +str(size)
  print 'size mu: ' +str(len(mu))
  print 'sigmashape: ' +str(sigma.shape)

  if size == len(mu) and (size, size) == sigma.shape:
    det = linalg.det(sigma)
    if det == 0:
        raise NameError("The covariance matrix can't be singular")

    norm_const = 1.0/ ( math.pow((2*pi),float(size)/2) * math.pow(det,1.0/2) )
    x_mu = matrix(x - mu)
    inv = sigma.I
    result = math.pow(math.e, -0.5 * (x_mu * inv * x_mu.T))
    return norm_const * result
  else:
    raise NameError("The dimensions of the input don't match")

print norm_pdf_multivariate(x, mu, sigma)
mlab_gauss=bivariate_normal(0,0,sigmax=1.0,sigmay=1.0,mux=0,muy=0,sigmaxy=1)
print mlab_gauss