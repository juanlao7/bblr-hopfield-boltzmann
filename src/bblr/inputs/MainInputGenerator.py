from numpy.random import RandomState
import math
from bblr.Utils import Utils
from bblr import patterns

class MainInputGenerator(object):
    MAX_TRIES = 400
    
    def __init__(self, properties, originalPatternDataSet, patternDataSetProperties, seedAddition):
        self.properties = properties
        self.originalPatternDataSet = originalPatternDataSet
        
        # Validating the configuration.
        seed = properties.get('seed')
        inputsPerPattern = self.properties.get('inputsPerPattern')
        minDistance = properties.get('minDistance')
        
        Utils.assertInt('Random seed', seed)
        Utils.assertInt('Inputs per pattern', inputsPerPattern, 1)
        
        if minDistance == None:
            raise Exception('Minimum distance not defined.')
        
        mean = minDistance.get('mean')
        Utils.assertFloat('Mean minimum distance', mean, 0)
        stdev = minDistance.get('stdev')
        Utils.assertFloat('Standard deviation of minimum distance', stdev, 0)
        
        # Initializing the random generator.
        randomGenerator = RandomState()
        randomGenerator.seed(seed + seedAddition)
        
        # Generating the inputs.
        patternSize = patternDataSetProperties.get('patternSize')
        self.originalInputs = []
        allFlips = map(lambda x: max(0, min(patternSize, int(round(x)))), randomGenerator.normal(mean, stdev, len(originalPatternDataSet) * inputsPerPattern))
        p = 0
        
        for pattern in originalPatternDataSet:
            for i in xrange(inputsPerPattern):
                inputVector = list(pattern)
                flips = allFlips[p + i] 
                componentsToFlip = range(patternSize)
                
                for j in xrange(flips):
                    componentIndex = randomGenerator.randint(0, flips - j)
                    component = componentsToFlip.pop(componentIndex)
                    inputVector[component] = int(not inputVector[component])
                
                self.originalInputs.append(tuple(inputVector))
                
            p += 1
        
        # Applying transformations.
        self.inputs = Utils.transformDataSet(randomGenerator, self.originalInputs, patternDataSetProperties)

    # Public methods. A generator must implement these methods in order to use it in Main.py
    
    def getInputs(self):
        return self.inputs
    
    def analyze(self):
        analysis = self.analyzeDataSet(self.originalInputs)
        return analysis['dataSetSize'], analysis['dimension'], analysis['mean'], analysis['stdev'], analysis['mean'] / analysis['dimension'], analysis['stdev'] / analysis['dimension']
    
    # Private methods.
    
    def analyzeDataSet(self, dataSet):
        minDs = map(lambda x: Utils.minDistance(x, self.originalPatternDataSet), dataSet)
        n = float(len(dataSet))
        mean = sum(minDs) / n
        variance = sum(map(lambda minD: (minD - mean)**2, minDs)) / n
        stdev = math.sqrt(variance)
        
        return {
            'dataSetSize': n,
            'dimension': len(dataSet[0]),
            'mean': mean,
            'stdev': stdev
        }

    def computeError(self, dataSet):
        analysis = self.analyzeDataSet(dataSet)
        minDistance = self.properties.get('minDistance')
        return Utils.meanSquareError([analysis['mean'], analysis['stdev']], [minDistance.get('mean'), minDistance.get('stdev')])
