'''
Created on 20 ene. 2017

@author: jorge

Two statistical tests for comparing algorithms.
'''

#Wilcoxon Test when number of data <30

from math import sqrt
import numpy as np
from scipy.stats import rankdata

def R(d,sign):
    if sign=='-':
        d=[-i for i in d]
    
    posd=[rank(i,d)+1 for i in d if i>0]
    zerod=[(rank(i,d) + 1)/2 for i in d if i==0]
    
    return sum(posd)+sum(zerod)

def rank(i,d):
    ranked=rankdata(d)
    return ranked[d.index(i)]

def wilcoxon(alg1, alg2):
    if len(alg1)!=len(alg2):
        return 0
    N=float(len(alg1))
    d=[alg1[i]-alg2[i] for i in range(len(alg1))]

    Rpos=R(d,'+')
    Rneg=R(d,'-')
    #T=min((Rpos,Rneg))
    
    if Rpos>Rneg:
        T=float(Rneg)
        winner='1'
    else:
        T=float(Rpos)
        winner='2'
    z=(T-N*(N+1)/4)/(sqrt(N*(N+1)*(2*N+1)/24))

    if z< -1.96:
        print('The neural network '+winner+' is better.')
    else:
        print('Both neural networks performed the same.')
    return z


#T-Test when number of data >30

from scipy.stats import ttest_ind


def ttest(data1, data2):
    t,p_value=ttest_ind(data1, data2, axis=0, equal_var=False)
    winner='1' if np.mean(data1)>np.mean(data2) else '2'
    if p_value<0.05:
        print('The neural network '+winner+ ' performed the best.')
    else:
        print('Both neural networks performed the same.')
    return t, p_value
    
'''
from scipy import stats 

print('T-Test')

rvs1 = stats.norm.rvs(loc=5,scale=10,size=500)
rvs2 = stats.norm.rvs(loc=5,scale=10,size=500)
t, p_value=ttest(rvs1,rvs2)       

print('\n \nWilcoxon')

rvs1 = np.random.randint(100, size=15)
rvs2 = np.random.randint(100, size=15)
z=wilcoxon(rvs1, rvs2)     
  '''      
        