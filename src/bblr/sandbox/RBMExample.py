import numpy as np
from bblr.models import RBM


partialA = """
.XXXX
X..XX
XXXXX
X...X
XX..X
"""

def exampleWithLetters():
    from bblr.generators import SimpleLetterGenerator as gen
    
    a = gen.to_pattern(gen.A)
    z = gen.to_pattern(gen.Z)
    rbm = RBM.RBM(25, 1000, verbose=True)
    patterns = np.atleast_2d((a,z))
    print patterns
    rbm.train(patterns, epochs=200, learning_rate=0.1)
    recovered = rbm.recall(gen.to_pattern(partialA))
    print "Recovered", recovered
    gen.display(recovered)


def exampleWithVectors(vector_size=5):
    from bblr.generators import SimpleVectorGenerator as gen
    
    patterns = np.vstack((gen.genAlternatingVector(vector_size), \
                         gen.genRepeatedVector(1, vector_size)))
    test = gen.genRandomBinaryVector(vector_size)
    print 'Training patterns:', patterns
    print 'Test patterns:', test
    
    rbm = RBM.RBM(n_visible=vector_size, n_hidden=3, verbose=True)
    rbm.train(patterns, epochs=100, learning_rate=0.01)
    recovered = rbm.recall(test)
    print 'Recovered:', np.around(recovered)
    
'''
Main
'''
print 'Example with vectors -1,1:'
print '--------------------------'
exampleWithVectors()
print '\n Example with letters A,Z'
print '---------------------------'
exampleWithLetters()    
    
