__author__ = 'Utente'
import numpy as np

def multivariate_pdf(vector, mean, cov):
    quadratic_form = np.dot(np.dot(vector-mean,np.linalg.inv(cov)),np.transpose(vector-mean))
    return np.exp(-.5 * quadratic_form)/ (2*np.pi * np.linalg.det(cov))


#x=np.random.normal(size=25)
#print x

c = np.cov(x,y)
print c

mean = np.array([0,0])
print mean
cov = np.array([[1,0],[0,1]])
print cov
vector = np.array([4,3])
print vector

pdf = multivariate_pdf(vector, mean, c)

print pdf