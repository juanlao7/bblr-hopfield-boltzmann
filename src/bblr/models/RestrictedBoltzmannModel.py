from bblr.Utils import Utils
import numpy
from bblr.models.Model import Model
from numpy.random import RandomState
from scipy.special import expit

class RestrictedBoltzmannModel(Model):
    STOP_WHEN_NOT_IMPROVEMENT_EPOCHS = 1000
    
    def __init__(self, properties, seedAddition):
        # Validating the configuration.
        self.seed = properties.get('seed')
        self.hiddenNeurons = properties.get('hiddenNeurons')
        self.learningRate = properties.get('learningRate')
        self.weightDecay = properties.get('weightDecay')
        self.momentum = properties.get('momentum')
        self.batchSize = properties.get('batchSize')
        
        Utils.assertInt('Random seed', self.seed)
        Utils.assertInt('Hidden neurons', self.hiddenNeurons, 0)
        Utils.assertFloat('Learning rate', self.learningRate, 0)
        Utils.assertFloat('Weight decay', self.weightDecay, 0)
        Utils.assertBoolean('Momentum', self.momentum)
        Utils.assertInt('Batch size', self.batchSize, 0)
        self.batchSize = int(self.batchSize)
        
        # Preparing the random generator.
        self.randomGenerator = RandomState()
        self.seed += seedAddition
    
    # Public methods. A model must implement these methods in order to use it in Main.py

    def train(self, patternDataSet):
        # Initializing the random generator.
        self.randomGenerator.seed(self.seed)
        
        visibleNeurons = len(patternDataSet[0])
        
        # Initializing weights according to Hinton, G. (2010). A practical guide to training restricted Boltzmann machines. Momentum, 9(1), 926.
        self.weights = 0.1 * self.randomGenerator.randn(visibleNeurons, self.hiddenNeurons)
        self.visibleOffset = numpy.zeros((1, visibleNeurons))
        self.hiddenOffset = -4.0 * numpy.ones((1, self.hiddenNeurons))
        
        # Training.
        deltaWeights = numpy.zeros((visibleNeurons, self.hiddenNeurons))
        deltaVisibleOffset = numpy.zeros((1, visibleNeurons))
        deltaHiddenOffset = numpy.zeros((1, self.hiddenNeurons))
        
        epochs = 0
        lesserDeltaWeightsNorm = numpy.linalg.norm(deltaWeights)
        stopCounter = 0
        
        while True:
            oldDeltaWeights = numpy.array(deltaWeights)
            
            for i in xrange(0, len(patternDataSet), self.batchSize):
                visibleBatch0 = numpy.asarray(patternDataSet[i:i + self.batchSize])
                
                # Positive phase: sample hiddenBatch0 from batch
                hiddenBatch0Probability = self.activation(visibleBatch0, self.weights, self.hiddenOffset)
                
                # Sample hiddenBatch0: we binarize the results of the activation function
                hiddenBatch0 = (hiddenBatch0Probability > self.randomGenerator.rand(self.batchSize, self.hiddenNeurons))
                
                # Negative phase: calculate visibleBatch1 from our hiddenBatch0 samples
                # Hinton, 2010 recommends not to binarize when updating visible units
                # No need to sample the last hidden states because they're not used
                visibleBatch1 = self.activation(hiddenBatch0, self.weights.T, self.visibleOffset)
                hiddenBatch1Probability = self.activation(visibleBatch1, self.weights, self.hiddenOffset)
                
                # Momentum is set as specified by Hinton's practical guide

                if self.momentum:
                    momentum = 0.5 if epochs > 5 else 0.9
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
            
            epochs += 1
            deltaWeightsNorm = numpy.linalg.norm(deltaWeights)
            
            if deltaWeightsNorm < lesserDeltaWeightsNorm:
                lesserDeltaWeightsNorm = deltaWeightsNorm
                stopCounter = 0
            else:
                stopCounter += 1
                
                if stopCounter > RestrictedBoltzmannModel.STOP_WHEN_NOT_IMPROVEMENT_EPOCHS:
                    break
        
        return {'trainingEpochs': epochs}
    
    def recall(self, visibleValues):
        # Initializing the random generator.
        self.randomGenerator.seed(self.seed)
        
        # Computing the output.
        hiddenProbability = self.activation(visibleValues, self.weights, self.hiddenOffset)
        hiddenValues = (hiddenProbability > self.randomGenerator.rand(1, self.hiddenNeurons))
        result = self.activation(hiddenValues, self.weights.T, self.visibleOffset)
        return tuple(map(lambda x: int(x), result[0] > 0.5)), 1
    
    # Private methods.
    
    def activation(self, batch, weights, offset):
        return expit(numpy.dot(batch, weights) + offset)

