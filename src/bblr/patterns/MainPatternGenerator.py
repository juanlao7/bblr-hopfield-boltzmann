from numpy.random import RandomState
import math
from bblr.Utils import Utils

class MainPatternGenerator(object):
    MAX_TRIES = 10
    
    def __init__(self, properties, seedAddition):
        self.properties = properties
        
        # Validating the configuration.
        seed = properties.get('seed')
        dataSetSize = self.properties.get('dataSetSize')
        patternSize = properties.get('patternSize')
        extraBits = properties.get('extraBits')
        distance = properties.get('distance')
        scale = properties.get('scale')
        
        Utils.assertInt('Random seed', seed)
        Utils.assertInt('Pattern data set size', dataSetSize, 1)
        Utils.assertInt('Pattern size', patternSize, 1)

        if extraBits != None:
            Utils.assertInt('Number of extra bits', extraBits.get('number'), 1)
            
            if extraBits.get('values') not in (0, 1, 'random'):
                raise Exception('Extra bits values must be 0, 1 or "random"')
        
        if distance != None:
            Utils.assertFloat('Mean distance', distance.get('mean'), 0)
            Utils.assertFloat('Standard deviation of distance', distance.get('stdev'), 0)
        
        if scale != None:
            if scale.get('type') == '1D':
                Utils.assertInt('Scale factor for 1D', scale.get('factor'), 1)
            elif scale.get('type') == '2D':
                Utils.assertInt('Scale pattern width', scale.get('patternWidth'), 1)
                Utils.assertInt('Scale pattern height', scale.get('patternHeight'), 1)
                Utils.assertInt('Scale width factor', scale.get('widthFactor'), 1)
                Utils.assertInt('Scale height factor', scale.get('heightFactor'), 1)
                
                if scale.get('patternWidth') * scale.get('patternHeight') != patternSize:
                    raise Exception('Scale pattern width and pattern height do not fit with the given pattern size')
            else:
                raise Exception('Unknown scale type ' + scale.get('type'))
        
        # Initializing the random generator.
        randomGenerator = RandomState()
        randomGenerator.seed(seed + seedAddition)
        
        # Generating the patterns.
        self.originalPatterns = Utils.generateDataSet(randomGenerator, dataSetSize, patternSize, self.computeError if 'distance' in self.properties else None, MainPatternGenerator.MAX_TRIES)
        
        # Applying transformations.
        self.patterns = Utils.transformDataSet(randomGenerator, self.originalPatterns, self.properties)

    # Public methods. A generator must implement these methods in order to use it in Main.py
    
    def getPatterns(self):
        return self.patterns
    
    def getOriginalPatterns(self):
        return self.originalPatterns
    
    def analyze(self):
        analysis = self.analyzeDataSet(self.patterns)
        return analysis['dataSetSize'], analysis['dimension'], analysis['mean'], analysis['stdev'], analysis['mean'] / analysis['dimension'], analysis['stdev'] / analysis['dimension']
    
    # Private methods.
    
    def analyzeDataSet(self, dataSet):
        n = len(dataSet)
        ds = []
        k = 0
        
        for i in xrange(n):
            for j in xrange(i + 1, n):
                ds.append(Utils.distance(dataSet[i], dataSet[j]))
                k += 1
        
        k = float(k)
        mean = sum(ds) / k
        variance = sum(map(lambda d: (d - mean)**2, ds)) / k
        stdev = math.sqrt(variance)
        
        return {
            'dataSetSize': n,
            'dimension': len(dataSet[0]),
            'mean': mean,
            'stdev': stdev
        }

    def computeError(self, dataSet):
        analysis = self.analyzeDataSet(dataSet)
        distance = self.properties.get('distance')
        return Utils.meanSquareError([analysis['mean'], analysis['stdev']], [distance.get('mean'), distance.get('stdev')])
