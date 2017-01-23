import numpy as np
from bblr.models import HopfieldPrototype


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
    from bblr.patterns import Letters as gen
    
    slg = gen.SimpleLetterGenerator()
    a = slg.toPattern(gen.A)
    z = slg.toPattern(gen.Z)
    i = slg.toPattern(gen.I)
    u = slg.toPattern(gen.U)
    partialz = slg.toPattern(partialZ)
    partiali = slg.toPattern(partialI)
    partiala2 = slg.toPattern(partialA2)
    partiala1 = slg.toPattern(partialA1)
    
    test = a
    
    hop = HopfieldPrototype.Hopfield(verbose=True)
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
    slg.display(test)
    slg.display(recovered)


def exampleWithVectors(vector_size=25):
    from bblr.patterns import BinaryVectors as gen
    
    svg = gen.SimpleVectorGenerator()
    patterns = np.vstack((svg.genAlternatingVector(vector_size), \
                         svg.genRepeatedVector(1, vector_size)))
    test = svg.genRandomBinaryVector(vector_size)
    test1 = svg.genRepeatedVector(1, vector_size)
    
    hop = HopfieldPrototype.Hopfield(verbose=True)
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