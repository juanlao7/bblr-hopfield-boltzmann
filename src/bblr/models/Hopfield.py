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
        
    def train(self, patterns, learningRule='hebbian', normW=True):
        '''
        Training a Hopfield network consists in setting the weight matrix 
        with the correlations of the patterns we are storing. This can be 
        done using different learning rules;  we have implemented 
            - Hebbian rule
            - Storkey rule
        The learning rule can be chosen through the parameter learningRule, 
        specifying it as 'hebbian' (default) or 'storkey'. 
        
        Note the parameter normW; If set to True (default), the weight matrix 
        is normalized by the number of neurons/input dimensions.
        '''
        
        self.numPatterns = patterns.shape[0]
        self.n = patterns.shape[1]
        self.W = np.zeros((self.n, self.n))
        
        if learningRule == 'storkey':
            self.storkeyRule(patterns, normW)
        else:
            self.hebbianRule(patterns, normW)
        
        
    
    def hebbianRule(self, patterns, normW):
        '''
        Training a Hopfield networt using the Hebbian rule
        W = sum(p(k)*p(k)') for k=1..n
        '''
        for p in patterns:
            self.W = self.W + np.outer(p, p)
        self.W[np.diag_indices(self.n)] = 0
        
        if normW:
            self.W = self.W / np.double(self.n)

            
    def storkeyRule(self, patterns, normW):
        '''
        Training a Hopfield networt using the Storkey rule
        '''
        for v in range(0, self.numPatterns):
            Wlastv = self.W.copy()
            for i in range(0, self.n):
                for j in range(i+1, self.n):    
                    s = (patterns[v][i] * patterns[v][j]
                         -patterns[v][i] * self.h(v, j, i, Wlastv, patterns) 
                         -self.h(v, i, j, Wlastv, patterns) * patterns[v][j])
                    self.W[i][j] += s
                    self.W[j][i] += s
                        
        if normW:
            self.W = self.W / np.double(self.n)

            
    def h(self, v, i, j, Wlastv, patterns):
        '''
        Calculates the form of local field of neuron i defined by
        the Storkey learning rule
        '''
        s = 0.0
        for k in range(0, self.n):
            if k != i and k != j:
                s += Wlastv[i][k] * patterns[v][k]
        return s
    
    
    def recall(self, inputs, maxSteps=1000):
        '''
        Given a trained Hopfield network, a stored pattern
        can be recalled from a partial version of it, which
        will be stored in inputs.
        
        Run until convergence or until maximum number of iterations
        
        ASYNCHRONOUS APPROACH
        '''

        i = 0
        result = inputs.copy()
        if self.verbose:
                print 'Energy at step', str(i), ':', self.energy(result)
        changed = True
        while (changed and i < maxSteps):
            changed, result = self.updatingNeurons(result)
            i += 1
            if self.verbose:
                print 'Energy at step', str(i), ':', self.energy(result)
        return result
    
    
    def updatingNeurons(self, input_pattern):
        '''Iterate over every neuron and update it's output'''
        result = input_pattern.copy()
        changed = False
        for neuron in range(self.n):
            neuron_output = self.calculateNeuronOutput(neuron, result)
            if neuron_output != result[neuron]:
                result[neuron] = neuron_output
                changed = True
        return changed, result
    
    
    def calculateNeuronOutput(self, neuron, input_pattern):
        '''Calculate the output of the given neuron'''
        s = np.sum(np.multiply(self.W[neuron,:], input_pattern))
        output = 1.0 if s > 0.0 else -1.0
        return output     
    
    
    def energy(self, sample):
        '''
        Calculates the energy for a sample.
        '''
        
        return -0.5*np.dot(np.dot(sample.T, self.W), sample)
    
    
    def recallSynchronously(self, inputs, maxSteps=10):
        '''
        SYNCHRONOUS APPROACH
        '''
        
        sgn = np.vectorize(lambda x: -1 if x<0 else +1)
        
        if self.verbose:
                print 'Energy at step', str(0), ':', self.energy(inputs)
        
        for i in range(1,maxSteps+1):
            lastInputs = inputs.copy()
            inputs = sgn(np.dot(inputs, self.W))
            
            if self.verbose:
                print 'Energy at step', str(i), ':', self.energy(inputs)
                
            if np.allclose(inputs, lastInputs):
                print 'It has converged!'
                break
            
        return inputs
    
    