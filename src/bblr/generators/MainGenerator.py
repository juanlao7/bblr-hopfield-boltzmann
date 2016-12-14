import math

class MainGenerator(object):
    properties = None
    dataSetSize = 0
    
    def __init__(self, patternDataSetProperties):
        self.properties = patternDataSetProperties
        self.dataSetSize = patternDataSetProperties['dataSetSize']
        
        # Validating the configuration
        patternSize = self.properties['patternSize']
        scale = self.properties['scale']
        similitude = self.properties['similitude']
        
        self.assertInt('Data set size', self.dataSetSize, 1)
        self.assertInt('Pattern size', patternSize, 1)
        
        if scale != None:
            if scale['type'] == '1D':
                self.assertInt('Scale factor for 1D', scale['factor'], 1)
            elif scale['type'] == '2D':
                self.assertInt('Scale pattern width', scale['patternWidth'], 1)
                self.assertInt('Scale pattern height', scale['patternHeight'], 1)
                self.assertInt('Scale width factor', scale['widthFactor'], 1)
                self.assertInt('Scale height factor', scale['heightFactor'], 1)
                
                if scale['patternWidth'] * scale['patternHeight'] != patternSize:
                    raise Exception('Scale pattern width and pattern height do not fit with the given pattern size')
            else:
                raise Exception('Unknown scale type ' + scale['type'])
        
        if similitude != None:
            matches = similitude['matches']
            self.assertInt('Matches number', matches, 1)
            
            # TODO: implement the affectation grade
            
            if similitude['type'] in ['common 1s', 'common 0s']:
                # TODO: link to the explanation of this fact
                maxDataSetSize = patternSize - matches + 1 if patternSize - matches <= 1 else matches + 2
                
                if self.dataSetSize > maxDataSetSize:
                    raise Exception('Data set size cannot be greater than ' + maxDataSetSize + ' when similitude type is "' + similitude['type'] + '", patternSize is ' + patternSize + ' and matches is ' + matches)
            elif similitude['type'] == 'equal neighbors 1D':
                # TODO: check if dataSize overflows the limit of this constraint.
                self.assertInt('Equal neighbors 1D k', similitude['k'], 0)
                n = similitude['k'] / 2.0
                
                if int(n) != n:
                    raise Exception('Equal neighbors 1D k must be 2n, where n is an integer equal or greater than 0')
            elif similitude['type'] == 'equal neighbors 2D':
                # TODO: check if dataSize overflows the limit of this constraint.
                self.assertInt('Equal neighbors 2D pattern width', similitude['patternWidth'], 1)
                self.assertInt('Equal neighbors 2D pattern height', similitude['patternHeight'], 1)
                self.assertInt('Equal neighbors 2D k', similitude['k'], 0)
                n = (math.sqrt(similitude['k'] + 1) - 1) / 2.0
                
                if int(n) != n:
                    raise Exception('Equal neighbors 2D k must be (2n + 1)^2 - 1, where n is an integer equal or greater than 0')
                
                if similitude['patternWidth'] * similitude['patternHeight'] != patternSize:
                    raise Exception('Equal neighbors pattern width and pattern height do not fit with the given pattern size')
            else:
                raise Exception('Unknown similitude type "' + similitude['type'] + '"')
    
    # Public methods. A generator must implement these methods in order to use it in Main.py
    
    def hasNext(self):
        return self.dataSetSize > 0
    
    def next(self):
        if self.dataSetSize <= 0:
            return None
        
        self.dataSetSize -= 1
        return self.scale(self.generatePattern())
    
    # Private methods.
    
    def assertInt(self, name, value, minValue=None):
        if type(value) is not int:
            raise Exception(name + ' must be an integer')
        
        if min != None and value < min:
            raise Exception(name + ' must be equal or greater than ' + str(minValue))
    
    def generatePattern(self):
        # TODO: implement this
        return [4] * self.properties['patternSize']

    def scale(self, pattern):
        scale = self.properties['scale']
        
        if scale == None:
            return pattern
        
        if scale['type'] == '1D':
            return self.scaleImpl(pattern, scale['factor'])
        elif scale['type'] == '2D':
            patternWidth = scale['patternWidth']
            patternHeight = scale['patternHeight']
            pattern2D = [[pattern[i * patternWidth + j] for j in xrange(patternWidth)] for i in xrange(patternHeight)]
            
            pattern2D = map(lambda x: self.scaleImpl(x, scale['widthFactor']), pattern2D)
            pattern2D = self.scaleImpl(pattern2D, scale['heightFactor'])
            
            return [j for i in pattern2D for j in i]
    
    def scaleImpl(self, listOfItems, factor):
        return [j for i in listOfItems for j in [i] * factor]

