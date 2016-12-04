import numpy as np

class RBM(object):
    '''
    Implementation of the Restricted Boltzmann Machine
    as an associative memory.
    '''


    def __init__(self, n_visible, n_hidden, W=None, h_offset=None, v_offset=None, verbose=False):
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
        self.n_visible = n_visible
        self.n_hidden = n_hidden
        self.verbose = verbose
        
    def train(self, X, epochs, learning_rate, momentum=False, batch_size=1):
        '''
        Trains the RBM with the samples provided in X, using
        a specified number of epochs and a learning rate.
        
        This method allows for:
        - Batch learning, if batch_size = X.shape[0]
        - Online learning, if batch_size = 1
        - Mini-batch learning, otherwise (10-100 is the most recommended)
        
        It allows to train using the momentum improvement by passing
        momentum=True
        '''
        if self.verbose:
            print 'Initial weights', self.W
            print 'Initial visible offsets', self.v_offset
            print 'Initial hidden offsets', self.h_offset
        
        d_w = np.zeros((self.n_visible, self.n_hidden))
        d_v = np.zeros((1, self.n_visible))
        d_h = np.zeros((1, self.n_hidden))
        
        batches = X.shape[0] // batch_size
        for epoch in range(epochs):
            for batch in range(batches):
                # Positive phase: sample h0 from v0
                v0 = X[int(batch*batch_size):int((batch+1)*batch_size)]
                prob_h0 = self.sigmoid(v0, self.W, self.h_offset)
                
                # Sample h0: we use binary units we binarize the results of sigmoid
                h0 = prob_h0 > np.random.rand(batch_size, self.n_hidden)
                
                # Negative phase: calculate v1 from our h0 samples
                # Hinton, 2010 recommends not to binarize when updating visible units
                #No need to sample the last hidden states because they're not used
                v1 = self.sigmoid(h0, self.W.T, self.v_offset)
                prob_h1 = self.sigmoid(v1, self.W, self.h_offset)
                
                #Momentum is set as specified by Hinton's practical guide
                if momentum:
                    m = 0.5 if epoch > 5 else 0.9
                else:
                    m = 1
                
                # Update increments of weights and offsets
                d_w = d_w * m + learning_rate * (np.dot(v0.T, prob_h0) - np.dot(v1.T, prob_h1))
                d_v = d_v * m + learning_rate * (np.sum(v0, axis=0) - np.sum(v1, axis=0))
                d_h = d_h * m + learning_rate * (np.sum(prob_h0, axis=0) - np.sum(prob_h1, axis=0))
                
                # Update weights and offsets
                self.W += d_w
                self.v_offset += d_v
                self.h_offset += d_h
        
    
    def recall(self, v0):
        '''
        Given an input vector v0, reconstructs it from the
        patterns that it has learned previously.
        '''
        prob_h0 = self.sigmoid(v0, self.W, self.h_offset)
        h0 = prob_h0 > np.random.rand(1, self.n_hidden)
        
        return self.sigmoid(h0, self.W.T, self.v_offset)
    
    
    def sigmoid(self, X, W, b):
        '''
        Calculates the activations of a layer using the
        sigmoid function.
        '''
        return 1.0 / (1 + np.exp(- np.dot(X,W) - b))
