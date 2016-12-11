import numpy as np
from bblr.models import Boltzmann


partialA = """
XXXXX
...XX
..XXX
.XXXX
XXXXX
"""

def exampleWithLetters():
    from bblr.generators import SimpleLetterGenerator as gen
    
    a = gen.to_pattern(gen.A, neg=0)
    z = gen.to_pattern(gen.Z, neg=0)
    rbm = Boltzmann.RBM(25, 15, verbose=False)

    patterns = np.atleast_2d((a,z))
    rbm.train(patterns, epochs=100000, learning_rate=0.01, momentum=True)
    recovered = rbm.recall(gen.to_pattern(partialA, neg=0))
    print "Recovered", recovered
    gen.display(recovered)


def exampleWithVectors(vector_size=5):
    from bblr.generators import SimpleVectorGenerator as gen
    
    patterns = np.vstack((gen.genAlternatingVector(vector_size), \
                         gen.genRepeatedVector(1, vector_size)))
    test = gen.genRandomBinaryVector(vector_size, neg=0)
    print 'Training patterns:', patterns
    print 'Test patterns:', test
    
    rbm = Boltzmann.RBM(n_visible=vector_size, n_hidden=5, verbose=False)
    rbm.train(patterns, epochs=100000, learning_rate=0.01, batch_size=2)
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
    
