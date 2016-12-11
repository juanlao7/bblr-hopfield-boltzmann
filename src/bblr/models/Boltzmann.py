import numpy as np

def sigmoid(X, W, b):
    '''
    Calculates the activations of a layer using the
    sigmoid function, in [0,1].
    '''
    xw = np.dot(X, W)
    return 1.0 / (1 + np.exp(- xw - b))


def tanh(X, W, b):
    '''
    Calculates the activations of a layer using the
    tanh function, in [-1,1].
    '''
    z = np.dot(X,W) + b
    return (np.exp(z) - np.exp(-z)) // (np.exp(z) + np.exp(-z))


class RBM(object):
    '''
    Implementation of the Restricted Boltzmann Machine
    as an associative memory.
    '''

    def __init__(self, n_visible, n_hidden, W=None, h_offset=None, v_offset=None, activation=sigmoid,verbose=False):
        '''
        Constructor
        '''
        if W is None:
            W = 0.1 * np.random.randn(n_visible, n_hidden)
        if h_offset is None:
            h_offset = -4.0 * np.ones((1, n_hidden))
        if v_offset is None:
            v_offset = np.zeros((1, n_visible))
            
        self.W = W
        self.h_offset = h_offset
        self.v_offset = v_offset
        self.n_visible = n_visible
        self.n_hidden = n_hidden
        self.verbose = verbose
        self.activation = activation
        
    def train(self, X, epochs, learning_rate, decay=0, momentum=False, batch_size=1):
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
                prob_h0 = self.activation(v0, self.W, self.h_offset)
                
                # Sample h0: we use binary units we binarize the results of sigmoid
                h0 = prob_h0 > np.random.rand(batch_size, self.n_hidden)
                
                # Negative phase: calculate v1 from our h0 samples
                # Hinton, 2010 recommends not to binarize when updating visible units
                #No need to sample the last hidden states because they're not used
                v1 = self.activation(h0, self.W.T, self.v_offset)
                prob_h1 = self.activation(v1, self.W, self.h_offset)
                
                #Momentum is set as specified by Hinton's practical guide
                if momentum:
                    m = 0.5 if epoch > 5 else 0.9
                else:
                    m = 1
                
                # Update increments of weights and offsets
                d_w = d_w * m + (learning_rate/batch_size) * (np.dot(v0.T, prob_h0) - np.dot(v1.T, prob_h1)) - decay * self.W
                d_v = d_v * m + (learning_rate/batch_size) * (np.sum(v0, axis=0) - np.sum(v1, axis=0))
                d_h = d_h * m + (learning_rate/batch_size) * (np.sum(prob_h0, axis=0) - np.sum(prob_h1, axis=0))
                
                # Update weights and offsets
                self.W += d_w
                self.v_offset += d_v
                self.h_offset += d_h
        
    
    def recall(self, v0):
        '''
        Given an input vector v0, reconstructs it from the
        patterns that it has learned previously.
        '''
        prob_h0 = self.activation(v0, self.W, self.h_offset)
        h0 = prob_h0 > np.random.rand(1, self.n_hidden)
        
        return self.activation(h0, self.W.T, self.v_offset)
