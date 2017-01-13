from bblr.Utils import Utils
import numpy

class RestrictedBoltzmannModel(object):
    def __init__(self, properties):
        self.hiddenNeurons = properties.get('hiddenNeurons')
        self.learningRate = properties.get('learningRate')
        self.weightDecay = properties.get('weightDecay')
        self.momentum = properties.get('momentum')
        self.batchSize = properties.get('batchSize')
        activationFunctionName = properties.get('activation')
        
        if activationFunctionName == 'sigmoid':
            self.activation = RestrictedBoltzmannModel.sigmoid
        elif activationFunctionName == 'tanh':
            self.activation = RestrictedBoltzmannModel.tanh
        else:
            raise Exception('Unknown activation function "' + activationFunctionName + '"')
        
        # Validating the configuration.
        Utils.assertInt('Hidden neurons', self.hiddenNeurons, 0)    # TODO: should we do this proportional to the pattern dimension?
        Utils.assertFloat('Learning rate', self.learningRate, 0)
        Utils.assertFloat('Weight decay', self.weightDecay, 0)
        Utils.assertBoolean('Momentum', self.momentum)
        Utils.assertInt('Batch size', self.batchSize, 0)
        self.batchSize = int(self.batchSize)

    def train(self, patternDataSet):
        visibleNeurons = len(patternDataSet[0])
        
        # Initializing weights.
        self.weights = 0.1 * numpy.random.randn(visibleNeurons, self.hiddenNeurons)
        self.visibleOffset = numpy.zeros((1, visibleNeurons))
        self.hiddenOffset = -4.0 * numpy.ones((1, self.hiddenNeurons))      # Why -4?
        
        # Training.
        deltaWeights = numpy.zeros((visibleNeurons, self.hiddenNeurons))
        deltaVisibleOffset = numpy.zeros((1, visibleNeurons))
        deltaHiddenOffset = numpy.zeros((1, self.hiddenNeurons))
        
        numberOfBatches = len(patternDataSet) // self.batchSize
        
        epochs = 100
        for epoch in xrange(epochs):    # TODO: we should stop on convergence
            for i in xrange(numberOfBatches):
                visibleBatch0 = numpy.asarray(patternDataSet[i * self.batchSize:(i + 1) * self.batchSize])
                
                # Positive phase: sample hiddenBatch0 from batch
                hiddenBatch0Probability = self.activation(visibleBatch0, self.weights, self.hiddenOffset)
                
                # Sample hiddenBatch0: we binarize the results of the activation
                hiddenBatch0 = (hiddenBatch0Probability > numpy.random.rand(self.batchSize, self.hiddenNeurons))
                
                # Negative phase: calculate visibleBatch1 from our hiddenBatch0 samples
                # Hinton, 2010 recommends not to binarize when updating visible units
                # No need to sample the last hidden states because they're not used
                visibleBatch1 = self.activation(hiddenBatch0, self.weights.T, self.visibleOffset)
                hiddenBatch1Probability = self.activation(visibleBatch1, self.weights, self.hiddenOffset)
                
                # Momentum is set as specified by Hinton's practical guide

                if self.momentum:
                    momentum = 0.5 if epoch > 5 else 0.9
                else:
                    momentum = 1
                
                # Update increments of weights and offsets
                deltaWeights = deltaWeights * momentum + (self.learningRate / self.batchSize) * (numpy.dot(visibleBatch0.T, hiddenBatch0Probability) - numpy.dot(visibleBatch1.T, hiddenBatch1Probability)) - self.weightDecay * self.weights
                deltaVisibleOffset = deltaVisibleOffset * momentum + (self.learningRate / self.batchSize) * (numpy.sum(visibleBatch0, axis=0) - numpy.sum(visibleBatch1, axis=0))
                deltaHiddenOffset = deltaHiddenOffset * momentum + (self.learningRate / self.batchSize) * (numpy.sum(hiddenBatch0Probability, axis=0) - numpy.sum(hiddenBatch1Probability, axis=0))
                
                # Update weights and offsets
                self.weights += deltaWeights
                self.visibleOffset += deltaVisibleOffset
                self.hiddenOffset += deltaHiddenOffset

    def test(self, inputDataSet):
        return ['TODO']
    
    @staticmethod
    def sigmoid(batch, weights, offset):
        return 1.0 / (1 + numpy.exp(-numpy.dot(batch, weights) - offset))
    
    @staticmethod
    def tanh(batch, weights, offset):
        z = numpy.dot(batch, weights) + offset
        return (numpy.exp(z) - numpy.exp(-z)) // (numpy.exp(z) + numpy.exp(-z))
