import numpy as np
from random import randint

class SimpleVectorGenerator():
    
    def __init__(self, pos=1, neg=-1):
        self.pos = pos
        self.neg = neg
    
    def genRandomBinaryVector(self, n):
        '''
        Generates a vector of -1, 1 in a random pattern
        n: length of the vector
        '''
        v = np.array([randint(0,1) for _ in range(1,n+1)])
        return [self.pos if x==1 else self.neg for x in v]
    
    def genAlternatingVector(self, n):
        '''
        Generates a vector of -1, 1 alternated
        n: length of the vector
        '''
        a = np.empty((n,))
        a[::2] = self.pos
        a[1::2] = self.neg
        return a
    
    def genRepeatedVector(self, val, n):
        '''
        Generates a vector with just one value repeated
        val: the value of each element
        n: length of the vector
        '''
        return np.repeat(val, n)
