__author__ = 'Utente'
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

#carico un punto  x,y nell'array
vector = np.array([4,3])
print 'coordinate del punto'
print vector
#calcolo la media s
#x_mean=np.mean(array,axis=0)
mean=np.array([0,0]).T
print mean
#print 'x_mean: ' + str(x_mean)
cov = np.array([[1,0],[0,1]])
print cov

#rv=multivariate_normal(mean=[2.25,2.25],cov=cov)
pdf_point=multivariate_normal.pdf(vector,mean=mean,cov=cov)
print 'pdf_point :' + str(pdf_point)
areaRet=5*5
prob_point=pdf_point*areaRet
print 'probabilita: '+ str(prob_point)
#print rv.pdf() 5.93115273525e-07
#print str(rv)
#np.cov(array)
#var = multivariate_normal(mean=[0,0], cov=[[1,0],[0,1]])
#ar.pdf([1,0])