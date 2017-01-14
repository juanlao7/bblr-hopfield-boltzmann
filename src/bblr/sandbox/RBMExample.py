import numpy as np
from bblr.models import Boltzmann


partialA = """
XXXXX
...XX
XXX..
XX...
XXXXX
"""

def exampleWithLetters():
    from bblr.patterns import Letters as gen
    
    slg = gen.SimpleLetterGenerator(pos=1, neg=0)
    a = slg.toPattern(gen.A)
    z = slg.toPattern(gen.Z)
    rbm = Boltzmann.RBM(25, 5, verbose=False)

    patterns = np.atleast_2d((a,z))
    rbm.train(patterns, thr=0.00001, learning_rate=0.01, momentum=True)
    recovered = rbm.recall(slg.toPattern(partialA))
    print "Recovered", recovered
    slg.display(recovered)


def exampleWithVectors(vector_size=5):
    from bblr.patterns import BinaryVectors as gen
    
    svg = gen.SimpleVectorGenerator(pos=1, neg=0)
    patterns = np.vstack((svg.genAlternatingVector(vector_size), \
                         svg.genRepeatedVector(1, vector_size)))
    test = svg.genRandomBinaryVector(vector_size)
    print 'Training patterns:', patterns
    print 'Test patterns:', test
    
    rbm = Boltzmann.RBM(n_visible=vector_size, n_hidden=5, verbose=False)
    rbm.train(patterns, thr=0.00001, learning_rate=0.01, batch_size=2)
    recovered = rbm.recall(test)
    print 'Recovered:', np.around(recovered)
    
'''
Main
'''
print 'Example with vectors 0,1:'
print '--------------------------'
exampleWithVectors()
print '\n Example with letters A,Z'
print '---------------------------'
exampleWithLetters()    
    
