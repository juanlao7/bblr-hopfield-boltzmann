from numpy.random import RandomState
import math

class MainGenerator(object):
    MAX_TRIES = 10
    
    def __init__(self, properties):
        self.properties = properties
        self.remainingPatterns = self.properties.get('dataSetSize')
        
        # Validating the configuration.
        seed = properties.get('seed')
        patternSize = properties.get('patternSize')
        extraBits = properties.get('extraBits')
        distance = properties.get('distance')
        scale = properties.get('scale')
        
        self.assertInt('Random seed', seed)
        self.assertInt('Data set size', self.remainingPatterns, 1)
        self.assertInt('Pattern size', patternSize, 1)

        if extraBits != None:
            self.assertInt('Number of extra bits', extraBits.get('number'), 1)
            
            if extraBits.get('values') not in (0, 1, 'random'):
                raise Exception('Extra bits values must be 0, 1 or "random"')
        
        if distance != None:
            self.assertFloat('Mean distance', distance.get('mean'), 0)
            self.assertFloat('Standard deviation of distance', distance.get('stdev'), 0)
        
        if scale != None:
            if scale.get('type') == '1D':
                self.assertInt('Scale factor for 1D', scale.get('factor'), 1)
            elif scale.get('type') == '2D':
                self.assertInt('Scale pattern width', scale.get('patternWidth'), 1)
                self.assertInt('Scale pattern height', scale.get('patternHeight'), 1)
                self.assertInt('Scale width factor', scale.get('widthFactor'), 1)
                self.assertInt('Scale height factor', scale.get('heightFactor'), 1)
                
                if scale.get('patternWidth') * scale.get('patternHeight') != patternSize:
                    raise Exception('Scale pattern width and pattern height do not fit with the given pattern size')
            else:
                raise Exception('Unknown scale type ' + scale.get('type'))
        
        # Initializing the random generator.
        self.randomGenerator = RandomState()
        self.randomGenerator.seed(seed)
        
        # Generating the patterns (greedy algorithm, approximate solution)
        self.patterns = []
        
        for i in xrange(self.remainingPatterns):
            self.patterns.append(self.generatePattern())
        
        if distance != None:
            bestError = self.analyzeDataSet(self.patterns)
            tries = 0
            
            while tries < MainGenerator.MAX_TRIES:
                candidate = self.generatePattern()
                improved = False
                
                for vectorToDiscard in self.patterns:
                    patternsCopy = list(self.patterns)
                    patternsCopy.remove(vectorToDiscard)
                    patternsCopy.append(candidate)
                    candidateError = self.analyzeDataSet(patternsCopy)
                    
                    if candidateError < bestError:
                        improved = True
                        self.patterns = patternsCopy
                        bestError = candidateError
                        break
                
                if improved:
                    tries = 0
                else:
                    tries += 1
        
        # Applying transformations
        self.patterns = map(lambda x: self.scale(self.addExtraBits(list(x))), self.patterns)

    # Public methods. A generator must implement these methods in order to use it in Main.py
    
    def getPatterns(self):
        return self.patterns
    
    # Private methods.
    
    def assertInt(self, name, value, minValue=None):
        if type(value) is not int:
            raise Exception(name + ' must be an integer')
        
        if minValue != None and value < minValue:
            raise Exception(name + ' must be equal or greater than ' + str(minValue))
        
    def assertFloat(self, name, value, minValue=None):
        if type(value) is not float and type(value) is not int:
            raise Exception(name + ' must be a floating-point number')
        
        if minValue != None and value < minValue:
            raise Exception(name + ' must be equal or greater than ' + str(minValue))
    
    def randomBits(self, randomGenerator, size):
        return list(randomGenerator.random_integers(0, 1, size))

    def generatePattern(self):
        while True:
            pattern = tuple(self.randomBits(self.randomGenerator, self.properties.get('patternSize')))
            
            if pattern not in self.patterns:
                return pattern
    
    def addExtraBits(self, pattern):
        extraBits = self.properties.get('extraBits')
        
        if extraBits == None:
            return pattern
        
        if extraBits.get('values') in (0, 1):
            return pattern + [extraBits.get('values')] * extraBits.get('number')
        
        return pattern + self.randomBits(self.randomGenerator, extraBits.get('number'))

    def scale(self, pattern):
        scale = self.properties.get('scale')
        
        if scale == None:
            return pattern
        
        if scale.get('type') == '1D':
            return self.scaleImpl(pattern, scale.get('factor'))
        elif scale.get('type') == '2D':
            patternWidth = scale.get('patternWidth')
            patternHeight = scale.get('patternHeight')
            pattern2D = [[pattern[i * patternWidth + j] for j in xrange(patternWidth)] for i in xrange(patternHeight)]
            
            pattern2D = map(lambda x: self.scaleImpl(x, scale.get('widthFactor')), pattern2D)
            pattern2D = self.scaleImpl(pattern2D, scale.get('heightFactor'))
            
            return [j for i in pattern2D for j in i]
    
    def scaleImpl(self, listOfItems, factor):
        return [j for i in listOfItems for j in [i] * factor]

    def distance(self, a, b):
        d = 0
        
        for i in xrange(len(a)):
            if a[i] != b[i]:
                d += 1
        
        return d

    def analyzeDataSet(self, dataSet):
        n = len(dataSet)
        mean = 0.0
        k = 0
        
        for i in xrange(n):
            for j in xrange(i + 1, n):
                d = self.distance(dataSet[i], dataSet[j])
                mean += d
                k += 1
        
        mean /= k 
        variance = 0.0
    
        for i in xrange(n):
            for j in xrange(i + 1, n):
                d = self.distance(dataSet[i], dataSet[j])
                variance += (d - mean)**2
                
        variance /= k
        stdev = math.sqrt(variance)
        distance = self.properties.get('distance')
        return self.meanSquareError([mean, stdev], [distance.get('mean'), distance.get('stdev')])
    
    def meanSquareError(self, y, target):
        error = 0.0
        n = len(y)
        
        for i in xrange(n):
            error += (target[i] - y[i])**2
        
        return error / n
