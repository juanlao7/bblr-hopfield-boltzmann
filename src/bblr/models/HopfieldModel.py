import numpy
from sre_parse import Pattern

class HopfieldModel(object):
    def __init__(self, properties):
        self.trainingRule = properties.get('trainingRule')
        
        # Validating the configuration.
        
        if self.trainingRule not in ('hebbian', 'storkey'):
            raise Exception('Unknown training rule "' + self.trainingRule + '". Only "hebbian" and "storkey" are supported')

    def train(self, patternDataSet):
        self.patternSize = len(patternDataSet[0])
        
        if self.trainingRule == 'hebbian':
            self.trainHebbian(patternDataSet)
        else:
            self.trainStorkey(patternDataSet)
    
    def test(self, inputDataSet):
        return ['TODO']
    
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
    