from numpy.random import RandomState
import math
from bblr.Utils import Utils

class MainInputGenerator(object):
    MAX_TRIES = 400
    
    def __init__(self, properties, originalPatternDataSet, patternDataSet, patternDataSetProperties, seedAddition):
        self.properties = properties
        
        # Validating the configuration.
        seed = properties.get('seed')
        inputsPerPattern = self.properties.get('inputsPerPattern')
        target = properties.get('target')
        minDistance = properties.get('minDistance')
        
        Utils.assertInt('Random seed', seed)
        Utils.assertInt('Inputs per pattern', inputsPerPattern, 1)
        
        if target not in ('originalPatterns', 'transformedPatterns'):
            raise Exception('Target must be "originalPatterns" or "transformedPatterns"') 
        
        if minDistance == None:
            raise Exception('Minimum distance not defined.')
        
        mean = minDistance.get('mean')
        meanIsProportion = Utils.assertProportionOrFloat('Mean minimum distance', mean, 0, 0)
        stdev = minDistance.get('stdev')
        stdevIsProportion = Utils.assertProportionOrFloat('Standard deviation of minimum distance', stdev, 0, 0)
        
        if meanIsProportion or stdevIsProportion and 'distance' not in patternDataSetProperties:
            raise Exception('Trying to create an input data set proportional to the distance of the pattern data set, but pattern data set has not defined distance.')
        
        if meanIsProportion:
            mean *= patternDataSetProperties['distance']['mean']
        
        if stdevIsProportion:
            stdev *= patternDataSetProperties['distance']['stdev']
        
        # Initializing the random generator.
        randomGenerator = RandomState()
        randomGenerator.seed(seed + seedAddition)
        
        # Generating the inputs.
        patternSize = patternDataSetProperties.get('patternSize')
        self.originalInputs = []
        self.targetDataSet = originalPatternDataSet if target == 'originalPatterns' else patternDataSet
        
        if stdev == 0:
            allFlips = [min(patternSize, int(round(mean)))] * (len(self.targetDataSet) * inputsPerPattern)
        else:
            allFlips = map(lambda x: max(0, min(patternSize, int(round(x)))), randomGenerator.normal(mean, stdev, len(self.targetDataSet) * inputsPerPattern))
        
        for i in xrange(len(self.targetDataSet)):
            insertedInputs = set()
            j = 0
            
            while j < inputsPerPattern:
                inputVector = list(self.targetDataSet[i])
                flips = allFlips[i + j] 
                componentsToFlip = range(patternSize)
                
                for k in xrange(flips):
                    componentIndex = randomGenerator.randint(0, patternSize - k)
                    component = componentsToFlip.pop(componentIndex)
                    inputVector[component] = int(not inputVector[component])
                
                inputVector = tuple(inputVector)
                
                if inputVector not in insertedInputs:
                    self.originalInputs.append(inputVector)
                    insertedInputs.add(inputVector)
                    j += 1
                        
        # Applying transformations.
        
        if target == 'originalPatterns':
            self.inputs = Utils.transformDataSet(randomGenerator, self.originalInputs, patternDataSetProperties)
        else:
            self.inputs = self.originalInputs

    # Public methods. A generator must implement these methods in order to use it in Main.py
    
    def getInputs(self):
        return self.inputs
    
    def analyze(self):
        return self.analyzeDataSet(self.originalInputs)
    
    # Private methods.
    
    def analyzeDataSet(self, dataSet):
        minDs = map(lambda x: Utils.minDistance(x, self.targetDataSet), dataSet)
        n = float(len(dataSet))
        mean = sum(minDs) / n
        variance = sum(map(lambda minD: (minD - mean)**2, minDs)) / n
        stdev = math.sqrt(variance)
        
        return {
            'inputDataSetSize': n,
            'inputDimension': len(dataSet[0]),
            'inputMinimumDistanceMean': mean,
            'inputMinimumDistanceStdev': stdev
        }

    def computeError(self, dataSet):
        analysis = self.analyzeDataSet(dataSet)
        minDistance = self.properties.get('minDistance')
        return Utils.meanSquareError([analysis['mean'], analysis['stdev']], [minDistance.get('mean'), minDistance.get('stdev')])
