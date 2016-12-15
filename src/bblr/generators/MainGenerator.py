import math

class MainGenerator(object):
    properties = None
    dataSetSize = 0
    
    def __init__(self, patternDataSetProperties):
        self.properties = patternDataSetProperties
        self.dataSetSize = patternDataSetProperties['dataSetSize']
        
        # Validating the configuration
        patternSize = self.properties['patternSize']
        extraBits = self.properties['extraBits']
        constraint = self.properties['constraint']
        scale = self.properties['scale']
        
        self.assertInt('Data set size', self.dataSetSize, 1)
        self.assertInt('Pattern size', patternSize, 1)
        
        if extraBits != None:
            self.assertInt('Number of extra bits', extraBits['number'], 1)
            
            if extraBits['values'] not in (0, 1, 'random'):
                raise Exception('Extra bits values must be 0, 1 or "random"')
        
        if constraint != None:
            self.assertFloat('Average distance', constraint['average'], 0)
            self.assertFloat('Standard deviation', constraint['stdev'], 0)
        
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
        
    def assertFloat(self, name, value, minValue=None):
        if type(value) is not float:
            raise Exception(name + ' must be a floating-point number')
        
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

