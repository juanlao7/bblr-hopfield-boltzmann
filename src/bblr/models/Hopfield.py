import numpy as np

class Hopfield():
    '''
    Implementation of the Hopfield network as an associative
    memory using numpy.
    '''


    def __init__(self, verbose=False):
        '''
        Constructor
        If the verbose flag is indicated, the network will
        output execution logs.
        '''
        
        self.verbose = verbose;
        
    
    def train(self, patterns, normW=False):
        '''
        Training a Hopfield network consists in setting the
        weight matrix with the correlations of the patterns
        we are storing.
        
        Note the parameter normW. If set to True, the weight
        matrix is normalized by the number of patterns.
        '''
        
        rows, cols = patterns.shape
        W = np.zeros((cols,cols))
        
        # W = sum(p(k)*p(k)') for k=1..n
        for p in patterns:
            W = W + np.outer(p, p)
        W[np.diag_indices(cols)] = 0
        
        if normW:
            self.W = W / rows
        else:
            self.W = W
        
    
    def recall(self, inputs, steps=5):
        '''
        Given a trained Hopfield network, a stored pattern
        can be recalled from a partial version of it, which
        will be stored in inputs.
        
        The higher the number of steps, the better the
        reconstruction may be.
        '''
        
        sgn = np.vectorize(lambda x: -1 if x<0 else +1)
        for i in xrange(steps):
            inputs = sgn(np.dot(inputs, self.W))
            
            if self.verbose:
                print 'Energy at step', i, ':', self.energy(inputs)
        return inputs
        
    
    def energy(self, sample):
        '''
        Calculates the energy for a sample.
        '''
        
        return -0.5*np.dot(np.dot(sample.T, self.W), sample)
    
    