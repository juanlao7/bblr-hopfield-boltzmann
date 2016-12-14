import math

class MainGenerator(object):
    properties = None
    dataSetSize = 0
    
    def __init__(self, randomSeed, patternDataSetProperties):
        self.properties = patternDataSetProperties
        self.dataSetSize = patternDataSetProperties['dataSetSize']
        
        # Validating the configuration
        
        self.assertInt('Data set size', self.dataSetSize, 1)
        self.assertInt('Pattern size', self.properties['patternSize'], 1)
        
        if self.properties['scale'] != None:
            if self.properties['scale']['type'] == '1D':
                self.assertInt('Scale factor for 1D', self.properties['scale']['factor'], 1)
            elif self.properties['scale']['type'] == '2D':
                self.assertInt('Scale pattern width', self.properties['scale']['patternWidth'], 1)
                self.assertInt('Scale pattern height', self.properties['scale']['patternHeight'], 1)
                self.assertInt('Scale width factor', self.properties['scale']['widthFactor'], 1)
                self.assertInt('Scale height factor', self.properties['scale']['heightFactor'], 1)
                
                if self.properties['scale']['patternWidth'] * self.properties['scale']['patternHeight'] != self.properties['patternSize']:
                    raise Exception('Scale pattern width and pattern height do not fit with the given pattern size')
            else:
                raise Exception('Unknown scale type ' + self.properties['scale']['type'])
        
        if self.properties['similitude'] != None:
            self.assertInt('Matches number', self.properties['similitude']['matches'], 1)
            
            if self.properties['similitude']['type'] == 'equal neighbors 2D':
                self.assertInt('Equal neighbors 2D pattern width', self.properties['similitude']['patternWidth'], 1)
                self.assertInt('Equal neighbors 2D pattern height', self.properties['similitude']['patternHeight'], 1)
                self.assertInt('Equal neighbors 2D k', self.properties['similitude']['k'], 8)
                
                n = (math.sqrt(self.properties['similitude']['k'] + 1) - 1) / 2.0
                
                if int(n) != n:
                    raise Exception('Equal neighbors 2D k must be (2n + 1)^2 - 1, where n is an integer equal or greater than 1')
                
                if self.properties['similitude']['patternWidth'] * self.properties['similitude']['patternHeight'] != self.properties['patternSize']:
                    raise Exception('Equal neighbors pattern width and pattern height do not fit with the given pattern size')
            elif self.properties['similitude']['type'] not in ['common bits', 'common 1s', 'common 0s']:
                raise Exception('Unknown similitude type "' + self.properties['similitude']['type'] + '"')
    
    # Public methods. A generator must implement these methods in order to use it in Main.py
    
    def hasNext(self):
        return self.dataSetSize > 0
    
    def next(self):
        if self.dataSetSize <= 0:
            return None
        
        self.dataSetSize -= 1
        return self.scale(self.generatePattern())
    
    # Private methods.
    
    def assertInt(self, name, value, min=None):
        if type(value) is not int:
            raise Exception(name + ' must be an integer')
        
        if min != None and value < min:
            raise Exception(name + ' must be equal or greater than ' + str(min))
    
    def generatePattern(self):
        # TODO: implement this
        return [4] * self.properties['patternSize']

    def scale(self, pattern):
        if self.properties['scale'] == None:
            return pattern
        
        if self.properties['scale']['type'] == '1D':
            return self.scaleImpl(pattern, self.properties['scale']['factor'])
        elif self.properties['scale']['type'] == '2D':
            patternWidth = self.properties['scale']['patternWidth']
            patternHeight = self.properties['scale']['patternHeight']
            pattern2D = [[pattern[i * patternWidth + j] for j in xrange(patternWidth)] for i in xrange(patternHeight)]
            
            pattern2D = map(lambda x: self.scaleImpl(x, self.properties['scale']['widthFactor']), pattern2D)
            pattern2D = self.scaleImpl(pattern2D, self.properties['scale']['heightFactor'])
            
            return [j for i in pattern2D for j in i]
    
    def scaleImpl(self, listOfItems, factor):
        return [j for i in listOfItems for j in [i] * factor]

