import numpy as np
import matplotlib.pyplot as plt

A = """
.XXX.
X...X
XXXXX
X...X
X...X
"""
 
Z = """
XXXXX
...X.
..X..
.X...
XXXXX
"""

def to_pattern(letter):
    '''
    Translates a 5x5 matrix representing a letter, with
    X being part of the letter and . not being part of it,
    to a vector representation where X=+1 and .=-1
    '''
    return np.array([+1 if c=='X' else -1 for c in letter.replace('\n','')])

def display(pattern):
    '''
    Given a pattern of +1, -1, displays it as an image. This is used
    for testing if the pattern reconstructed by the network is good.
    '''
    plt.imshow(pattern.reshape((5,5)), interpolation='nearest')
    plt.show()