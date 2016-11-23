import numpy as np
import matplotlib.pyplot as plt
from bblr.models import Hopfield

A = """
.XXX.
X...X
XXXXX
X...X
X...X
"""

partialA = """
X...X
.XX..
.....
.XXX.
.XXX.
"""
 
Z = """
XXXXX
...X.
..X..
.X...
XXXXX
"""

def to_pattern(letter):
    return np.array([+1 if c=='X' else -1 for c in letter.replace('\n','')])

def display(pattern):
    plt.imshow(pattern.reshape((5,5)), interpolation='nearest')
    plt.show()
    
a = to_pattern(A)
z = to_pattern(Z)
hop = Hopfield.Hopfield(verbose=True)
patterns = np.atleast_2d((a,z))
print patterns
hop.train(patterns, normW=True)
recovered = hop.recall(to_pattern(partialA),steps=5)
display(recovered)