import numpy

class HopfieldModel(object):
    def __init__(self, properties):
        self.trainingRule = properties.get('trainingRule')
        
        # Validating the configuration.
        
        if self.trainingRule not in ('hebbian', 'storkey'):
            raise Exception('Unknown training rule "' + self.trainingRule + '". Only "hebbian" and "storkey" are supported')

    def train(self, patternDataSet):
        self.patternSize = len(patternDataSet[0])
        self.weights = numpy.zeros((self.patternSize, self.patternSize))
        
        if self.trainingRule == 'hebbian':
            self.trainHebbian(patternDataSet)
        else:
            self.trainStorkey(patternDataSet)
    
    def trainHebbian(self, patternDataSet):
        for pattern in patternDataSet:
            self.weights += numpy.outer(pattern, pattern)
        
        self.weights[numpy.diag_indices(self.patternSize)] = 0
        self.W /= self.patternSize
    
    def trainStorkey(self, patternDataSet):
        # TODO
    