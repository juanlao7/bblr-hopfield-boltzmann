from numpy.random import RandomState
import bisect

class MainGenerator(object):
    properties = None
    remainingPatterns = 0
    grayPatterns = []
    patternRandomGenerator = RandomState()
    extraBitsRandomGenerator = None
    
    def __init__(self, properties):
        self.properties = properties
        self.remainingPatterns = self.properties.get('dataSetSize')
        
        # Validating the configuration
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
        
        # Initializing the random generators
        self.patternRandomGenerator.seed(seed)
        
        if extraBits != None:
            self.extraBitsRandomGenerator = RandomState()
            self.extraBitsRandomGenerator.seed(seed + 1)        # To generate different numbers than the other generator
    
    # Public methods. A generator must implement these methods in order to use it in Main.py
    
    def hasNext(self):
        return self.remainingPatterns > 0
    
    def next(self):
        if self.remainingPatterns <= 0:
            return None
        
        self.remainingPatterns -= 1
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
    
    def randomBits(self, randomGenerator, size):
        return list(randomGenerator.random_integers(0, 1, size))

    def generatePattern(self):
        patternSize = self.properties.get('patternSize')
        distance = self.properties.get('distance')
        
        if distance == None:
            return self.randomBits(self.patternRandomGenerator, patternSize)
        
        if len(self.grayPatterns) == 0:
            pattern = self.randomBits(self.patternRandomGenerator, patternSize)
        else:
            desiredDistance = int(round(max(0, min(distance.get('mean') + distance.get('stdev') * self.patternRandomGenerator.standard_normal(), patternSize))))
            bestX, bestDistance = self.findBestFit(desiredDistance)
            print desiredDistance, bestDistance
            bestX = int(round(bestX))
            pattern = self.int2gray(bestX)
            pattern = [0] * (patternSize - len(pattern)) + pattern      # Adding leading 0s
        
        bisect.insort(self.grayPatterns, self.gray2int(pattern))
        return pattern
    
    def addExtraBits(self, pattern):
        extraBits = self.properties.get('extraBits')
        
        if extraBits == None:
            return pattern
        
        if extraBits.get('values') in (0, 1):
            return pattern + [extraBits.get('values')] * extraBits.get('number')
        
        return pattern + self.randomBits(self.extraBitsRandomGenerator, extraBits.get('number'))

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
    
    def findBestFit(self, desiredDistance):
        # Let d(x) be the mean distance between x and all the n patterns in the set, that is equal to 1/n * sum(i from 0 to n, abs(i - x))
        # We want x such that d(x) = desiredDistance
        # In other words, we want x such that f(x) = d(x) - desiredDistance = 0
        # Or, if x does not exist, we want x' such that f(x') is the global minimum of f
        
        # a) We know that d(x) is "convex" (actually, we work with integers and not reals) for x from -inf to +inf
        # So there are 0 or 2 x such that f(x) = 0
        
        # b) We also know that d(x) is a composition of lines with different slope, and they intersect exactly in the patterns of the set.
        # For example, if the set contains the patterns 1, 4, 5, 8, then d(x) is composed by line from -inf to 1, a line from 1 to 4,
        # a line from 4 to 5, a line from 5 to 8 and a line from 8 to +inf.
        
        # Taking in account (a) and (b), we deduce that, if x exists, there will be 2 possible x, and they will be:
        #    1. In the line that goes from -inf to the first pattern if f(first pattern) <= 0
        #    2. In the line that goes from the last pattern to +inf if f(last pattern) <= 0
        #    3. In the line that goes from pattern A to pattern B if f(A) * f(B) <= 0
        # Note that x cannot be negative
        
        # If x does not exist, then we x' such that f(x') is the global minimum of f.
        # If patterns are sortered, x' will be in the first pattern i such that f(i) < f(i+1) or pattern i+1 does not exist
        
        if self.targetFunction(self.grayPatterns[0], desiredDistance) <= 0:
            # x is in the line that goes from -inf to the first pattern.
            root = self.findRoot(self.grayPatterns[0] - 1, self.grayPatterns[0], desiredDistance=desiredDistance)
            
            if root >= 0:
                return root, 0
        
        if self.targetFunction(self.grayPatterns[-1], desiredDistance) <= 0:
            # x is in the line that goes from the last pattern to +inf
            return self.findRoot(self.grayPatterns[-1], self.grayPatterns[-1] + 1, desiredDistance=desiredDistance), 0
        
        y1 = self.meanDistance(self.grayPatterns[0])
        
        for i in xrange(len(self.grayPatterns) - 1):
            x0 = self.grayPatterns[i]
            y0 = y1
            x1 = self.grayPatterns[i + 1]
            y1 = self.targetFunction(x1, desiredDistance)
            
            if y0 < y1:
                # x' is in the first pattern i such that f(i) < f(i+1)
                return x0, y0
            
            if y0 * y1 <= 0:
                # x is in the line that goes from pattern i to pattern i+1
                return self.findRoot(x0, x1, y0, y1), 0
        
        # x' is in the first pattern i such that i+1 does not exist
        return self.grayPatterns[-1], self.targetFunction(self.grayPatterns[-1], desiredDistance)

    def findRoot(self, x0, x1, y0=None, y1=None, desiredDistance=0):
        if y0 == None:
            y0 = self.targetFunction(x0, desiredDistance)
        
        if y1 == None:
            y1 = self.targetFunction(x1, desiredDistance)
        
        m = (y0 - y1) / float(x0 - x1)
        n = (x0 * y1 - x1 * y0) / float(x0 - x1)
        return -n / m
    
    def targetFunction(self, x, desiredDistance):
        return self.meanDistance(x) - desiredDistance
    
    def meanDistance(self, x):
        mean = 0.0
        
        for i in self.grayPatterns:
            mean += abs(i - x)
        
        return mean / len(self.grayPatterns)
    
    def bin2gray(self, bits):
        print bits
        return bits[:1] + [i ^ ishift for i, ishift in zip(bits[:-1], bits[1:])]
 
    def gray2bin(self, bits):
        b = [bits[0]]
        for nextb in bits[1:]: b.append(b[-1] ^ nextb)
        return b

    def int2bin(self, n):
        if n:
            bits = []
            while n:
                n,remainder = divmod(n, 2)
                bits.insert(0, remainder)
            return bits
        else: return [0]
    
    def bin2int(self, bits):
        i = 0
        for bit in bits:
            i = i * 2 + bit
        return i

    def gray2int(self, bits):
        return self.bin2int(self.gray2bin(bits))
    
    def int2gray(self, n):
        return self.bin2gray(self.int2bin(n))

