import numpy as np
from random import randint

def genRandomBinaryVector(n):
    '''
    Generates a vector of -1, 1 in a random pattern
    n: length of the vector
    '''
    return np.array([randint(0,1) for _ in range(1,n+1)])

def genAlternatingVector(n):
    '''
    Generates a vector of -1, 1 alternated
    n: length of the vector
    '''
    a = np.empty((n,))
    a[::2] = 1
    a[1::2] = 0
    return a

def genRepeatedVector(val, n):
    '''
    Generates a vector with just one value repeated
    val: the value of each element
    n: length of the vector
    '''
    return np.repeat(val, n)
