import numpy as np

class RBM(object):
    '''
    Implementation of the Restricted Boltzmann Machine
    as an associative memory.
    '''


    def __init__(self, n_visible, n_hidden, W=None, h_offset=None, v_offset=None):
        '''
        Constructor
        '''
        if W is None:
            # Initializes W randomly as N(mu=2,var=4)
            W = 2 * np.random.randn(n_visible, n_hidden) + 2
            
        if h_offset is None:
            h_offset = np.zeros((1 ,n_hidden))
            
        if v_offset is None:
            v_offset = np.zeros((1, n_visible))
             
        self.W = W
        self.h_offset = h_offset
        self.v_offset = v_offset
        
    def train(self, X):
        '''
        
        '''
        pass
    
    def sigmoid(self, X, W, b):
        '''
        Calculates the activations of a layer using the
        sigmoid function.
        '''
        return 1.0 / (1 + np.exp(- np.dot(X,W) - b))
    
    
    
    