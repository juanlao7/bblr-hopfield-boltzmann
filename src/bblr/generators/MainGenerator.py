import random

class MainGenerator(object):
    properties = None
    dataSetSize = 0
    patternRandomGenerator = random.Random()
    extraBitsRandomGenerator = None
    
    def __init__(self, properties):
        self.properties = properties
        self.dataSetSize = self.properties.get('dataSetSize')
        
        # Validating the configuration
        seed = properties.get('seed')
        patternSize = properties.get('patternSize')
        extraBits = properties.get('extraBits')
        constraint = properties.get('constraint')
        scale = properties.get('scale')
        
        self.assertInt('Random seed', seed)
        self.assertInt('Data set size', self.dataSetSize, 1)
        self.assertInt('Pattern size', patternSize, 1)
                
        if extraBits != None:
            self.assertInt('Number of extra bits', extraBits.get('number'), 1)
            
            if extraBits.get('values') not in (0, 1, 'random'):
                raise Exception('Extra bits values must be 0, 1 or "random"')
        
        if constraint != None:
            self.assertFloat('Average distance', constraint.get('average'), 0)
            self.assertFloat('Standard deviation', constraint.get('stdev'), 0)
        
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
        
        # Initializing the random generators
        self.patternRandomGenerator.seed(seed)
        
        if extraBits != None:
            self.extraBitsRandomGenerator = random.Random()
            self.extraBitsRandomGenerator.seed(seed + 1)        # To generate different numbers than the other generator
    
    # Public methods. A generator must implement these methods in order to use it in Main.py
    
    def hasNext(self):
        return self.dataSetSize > 0
    
    def next(self):
        if self.dataSetSize <= 0:
            return None
        
        self.dataSetSize -= 1
        return self.scale(self.addExtraBits(self.generatePattern()))
    
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
    
    def generatePattern(self):
        # TODO: implement this
        return [self.patternRandomGenerator.randint(0, 1) for i in xrange(self.properties.get('patternSize'))]
    
    def addExtraBits(self, pattern):
        extraBits = self.properties.get('extraBits')
        
        if extraBits == None:
            return pattern
        
        if extraBits.get('values') in (0, 1):
            return pattern + [extraBits.get('values')] * extraBits.get('number')
        
        return pattern + [self.extraBitsRandomGenerator.randint(0, 1) for i in xrange(extraBits.get('number'))]

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

