import numpy
from bblr.models.Model import Model

class HopfieldModel(Model):
    def __init__(self, properties, seedAddition):
        self.trainingRule = properties.get('trainingRule')
        
        # Validating the configuration.
        
        if self.trainingRule not in ('hebbian', 'storkey'):
            raise Exception('Unknown training rule "' + self.trainingRule + '". Only "hebbian" and "storkey" are supported')

    # Public methods. A model must implement these methods in order to use it in Main.py
    
    def train(self, patternDataSet, patternDataSetProperties):
        self.patternSize = len(patternDataSet[0])
        hopfieldDomainPatternDataSet = map(lambda pattern: self.toHopfieldDomain(pattern), patternDataSet)
        
        if self.trainingRule == 'hebbian':
            self.trainHebbian(hopfieldDomainPatternDataSet)
        else:
            self.trainStorkey(hopfieldDomainPatternDataSet)
        
        return {'trainingEpochs': 1}
    
    def recall(self, inputVector):
        result = self.toHopfieldDomain(inputVector)
        iterations = 0
        changed = True
        
        while (changed):
            changed = self.updateNeurons(result)
            iterations += 1

        return self.toStandardDomain(result), iterations
    
    # Private methods.
    
    def toHopfieldDomain(self, vector):
        return numpy.array(map(lambda x: 1.0 if x == 1 else -1.0, vector))
    
    def toStandardDomain(self, vector):
        return tuple(map(lambda x: int(x != -1.0), vector))
    
    def trainHebbian(self, patternDataSet):
        self.weights = numpy.zeros((self.patternSize, self.patternSize))
        
        for pattern in patternDataSet:
            self.weights += numpy.outer(pattern, pattern)
        
        self.weights[numpy.diag_indices(self.patternSize)] = 0
        self.weights /= self.patternSize
    
    def trainStorkey(self, patternDataSet):
        self.weights = numpy.zeros((self.patternSize, self.patternSize))
        n = self.patternSize
        
        for v in xrange(len(patternDataSet)):
            lastWeights = self.weights.copy()
            
            for i in range(0, self.patternSize):
                for j in range(i + 1, self.patternSize):
                    weight = lastWeights[i][j]
                    weight += patternDataSet[v][i] * patternDataSet[v][j] / n
                    weight -= patternDataSet[v][i] * self.h(v, j, i, lastWeights, patternDataSet) / n
                    weight -= patternDataSet[v][j] * self.h(v, i, j, lastWeights, patternDataSet) / n 
                    
                    self.weights[i][j] = weight
                    self.weights[j][i] = weight
    
    def h(self, v, i, j, lastWeights, patternDataSet):
        s = 0.0
        
        for k in xrange(self.patternSize):
            if k != i and k != j:
                s += lastWeights[i][k] * patternDataSet[v][k]
        
        return s
    
    def updateNeurons(self, inputVector):
        changed = False
        
        for neuron in xrange(self.patternSize):
            neuronOutput = self.calculateNeuronOutput(neuron, inputVector)
            
            if neuronOutput != inputVector[neuron]:
                inputVector[neuron] = neuronOutput
                changed = True
        
        return changed
    
    def calculateNeuronOutput(self, neuron, inputVector):
        return 1.0 if numpy.sum(numpy.multiply(self.weights[neuron,:], inputVector)) > 0.0 else -1.0
    
