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
        
    
    def trainHebbian(self, patterns, normW=True):
        '''
        Training a Hopfield network consists in setting the
        weight matrix with the correlations of the patterns
        we are storing.
        
        Note the parameter normW. If set to True (default), 
        the weight matrix is normalized by the number of 
        neurons (input dimensions).
        '''
        
        rows, cols = patterns.shape
        W = np.zeros((cols,cols))
        
        # W = sum(p(k)*p(k)') for k=1..n
        for p in patterns:
            W = W + np.outer(p, p)
        W[np.diag_indices(cols)] = 0
        
        if normW:
            self.W = W / cols
        else:
            self.W = W
            
    def trainStorkey(self, patterns, normW=True):
        # each row of patterns is a fpattern/sample, each column dimension/feature
        numPatterns, n = patterns.shape
        W = np.zeros((n, n))
        for v in range(0, numPatterns):
            Wlastv = W.copy()
            for i in range(0, n):
                for j in range(0, n):
                    if i != j:
                        s = (patterns[v][i] * patterns[v][j] - 
                             patterns[v][i] * self.h(v, j, i, Wlastv, patterns) - 
                             self.h(v, i, j, Wlastv, patterns) * patterns[v][j])
                        W[i][j] += s
            
        if normW:
            self.W = W / np.double(n)
        else:
            self.W = W
            
    def h(self, miu, i, j, W, patterns):
        s = 0.0
        n = patterns.shape[1]
        for k in range(0, n):
            if k != i and k != j:
                s += W[i][k] * patterns[miu][k]
        return s
        
    
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
    
    