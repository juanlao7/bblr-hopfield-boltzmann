import numpy as np
import matplotlib.pyplot as plt
from cvxpy.atoms.elementwise.pos import pos

A = """
.XXX.
X...X
XXXXX
X...X
X...X
"""
 
I = """
..X..
..X..
..X..
..X..
..X..
"""

U = """
X...X
X...X
X...X
X...X
XXXXX
"""

Z = """
XXXXX
...X.
..X..
.X...
XXXXX
"""

class SimpleLetterGenerator():
    
    def __init__(self, pos=1, neg=-1):
        self.pos = pos
        self.neg = neg
    
    def toPattern(self, letter):
        '''
        Translates a 5x5 matrix representing a letter, with
        X being part of the letter and . not being part of it,
        to a vector representation where X=+1 and .=-1
        '''
        return np.array([self.pos if c=='X' else self.neg for c in letter.replace('\n','')])
    
    def display(self, pattern):
        '''
        Given a pattern of +1, -1, displays it as an image. This is used
        for testing if the pattern reconstructed by the network is good.
        '''
        plt.imshow(pattern.reshape((5,5)), interpolation='nearest')
        plt.show()