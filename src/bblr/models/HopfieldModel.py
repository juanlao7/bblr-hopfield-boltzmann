import numpy
from bblr.models.Model import Model

class HopfieldModel(Model):
    def __init__(self, properties, seedAddition):
        self.trainingRule = properties.get('trainingRule')
        
        # Validating the configuration.
        
        if self.trainingRule not in ('hebbian', 'storkey'):
            raise Exception('Unknown training rule "' + self.trainingRule + '". Only "hebbian" and "storkey" are supported')

    # Public methods. A model must implement these methods in order to use it in Main.py
    
    def train(self, patternDataSet):
        self.patternSize = len(patternDataSet[0])
        
        if self.trainingRule == 'hebbian':
            self.trainHebbian(patternDataSet)
        else:
            self.trainStorkey(patternDataSet)
        
        return {'trainingEpochs': 1}
    
    def recall(self, inputVector):
        #print 'Input:', inputVector
        result = numpy.array(map(lambda x: 1.0 if x == 1 else -1.0, inputVector))
        #print 'Converted to -1.0..1.0:', result
        iterations = 0
        changed = True
        
        while (changed):
            #print 'updating neurons'
            changed = self.updateNeurons(result)
            #print 'Current:', result
            iterations += 1
            
        #print 'Converged!'
        #raise 'we'

        #return map(lambda x: int(x != -1.0), result), iterations
        return result, iterations
    
    # Private methods.
    
    def trainHebbian(self, patternDataSet):
        self.weights = numpy.zeros((self.patternSize, self.patternSize))
        
        for pattern in patternDataSet:
            self.weights += numpy.outer(pattern, pattern)
        
        self.weights[numpy.diag_indices(self.patternSize)] = 0
        self.weights /= self.patternSize
    
    def trainStorkey(self, patternDataSet):
        self.weights = numpy.zeros((self.patternSize, self.patternSize))
        
        for v in xrange(len(patternDataSet)):
            lastWeights = self.weights.copy()
            
            for i in range(0, self.patternSize):
                for j in range(i + 1, self.patternSize):    
                    s = (patternDataSet[v][i] * patternDataSet[v][j]
                        - patternDataSet[v][i] * self.h(v, j, i, lastWeights, patternDataSet) 
                        - patternDataSet[v][j] * self.h(v, i, j, lastWeights, patternDataSet))
                    
                    self.weights[i][j] += s
                    self.weights[j][i] += s
                        
        self.weights /= self.patternSize
    
    def h(self, v, i, j, lastWeights, patternDataSet):
        s = 0.0
        
        for k in range(self.patternSize):
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
    
