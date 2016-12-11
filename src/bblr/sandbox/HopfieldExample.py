import numpy as np
from bblr.models import Hopfield


partialA1 = """
X...X
.XX..
.....
.XXX.
.XXX.
"""
partialA2 = """
.XXXX
X..XX
XXXXX
X...X
XX..X
"""

partialI = """
.X...
..X..
.X...
..X..
...X.
"""

partialZ = """
.XXXX
...X.
X....
.X...
XX.XX
"""


def exampleWithLetters():
    from bblr.generators import SimpleLetterGenerator as gen
    
    a = gen.to_pattern(gen.A)
    z = gen.to_pattern(gen.Z)
    i = gen.to_pattern(gen.I)
    u = gen.to_pattern(gen.U)
    partialz = gen.to_pattern(partialZ)
    partiali = gen.to_pattern(partialI)
    partiala2 = gen.to_pattern(partialA2)
    partiala1 = gen.to_pattern(partialA1)
    
    test = a
    
    hop = Hopfield.Hopfield(verbose=True)
    patterns = np.atleast_2d((i, u, z, a))
    '''Using Storkey rule'''
    hop.train(patterns, learningRule='storkey')
    '''Using Hebbian rule'''
    #hop.train(patterns)
    recovered = hop.recall(test)
    #recovered = hop.recall(i)
    print 'Patterns', patterns
    print 'Test patterns:\n', test
    print "Recovered\n", recovered
    gen.display(test)
    gen.display(recovered)


def exampleWithVectors(vector_size=25):
    from bblr.generators import SimpleVectorGenerator as gen
    
    patterns = np.vstack((gen.genAlternatingVector(vector_size), \
                         gen.genRepeatedVector(1, vector_size)))
    test = gen.genRandomBinaryVector(vector_size)
    test1 = gen.genRepeatedVector(1, vector_size)
    
    hop = Hopfield.Hopfield(verbose=True)
    hop.train(patterns, learningRule='storkey')
    recovered = hop.recall(test, maxSteps=11)
    print 'Training patterns:', patterns
    print 'Test patterns:', test
    print 'Recovered:', np.around(recovered)
    
'''
Main
'''
#exampleWithVectors()
exampleWithLetters()