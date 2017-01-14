class Utils(object):
    @staticmethod
    def assertInt(name, value, minValue=None):
        if type(value) is not int:
            raise Exception(name + ' must be an integer')
        
        if minValue != None and value < minValue:
            raise Exception(name + ' must be equal or greater than ' + str(minValue))
        
    @staticmethod
    def assertFloat(name, value, minValue=None):
        if type(value) is not float and type(value) is not int:
            raise Exception(name + ' must be a floating-point number')
        
        if minValue != None and value < minValue:
            raise Exception(name + ' must be equal or greater than ' + str(minValue))
    
    @staticmethod
    def assertBoolean(name, value):
        if type(value) is not bool:
            raise Exception(name + ' must be boolean')

    @staticmethod
    def generateUniqueVector(randomGenerator, dimension, dataSet):
        while True:
            vector = tuple(Utils.randomBits(randomGenerator, dimension))
            
            if vector not in dataSet:
                return vector

    @staticmethod
    def randomBits(randomGenerator, size):
        return list(randomGenerator.random_integers(0, 1, size))
    
    @staticmethod
    def distance(a, b):
        d = 0
        
        for i, j in zip(a, b):
            if i != j:
                d += 1
        
        return d
    
    @staticmethod
    def minDistance(v, P):
        return min(Utils.distance(v, p) for p in P)
    
    @staticmethod
    def meanSquareError(y, target):
        error = 0.0
        n = len(y)
        
        for i in xrange(n):
            error += (target[i] - y[i])**2
        
        return error / n
    
    @staticmethod
    def generateDataSet(randomGenerator, dataSetSize, dimension, errorFunction, maxTries):
        maxCombinations = 2**dimension
        
        if dataSetSize > maxCombinations:
            raise Exception('You are trying to create more unique vectors (' + str(dataSetSize) + ') than possible combinations (' + str(maxCombinations) + ').')
        
        # Greedy algorithm, approximate solution
        dataSet = []
        
        for _ in xrange(dataSetSize):
            dataSet.append(Utils.generateUniqueVector(randomGenerator, dimension, dataSet))

        if errorFunction != None:
            bestError = errorFunction(dataSet)
            tries = 0
            
            while tries < maxTries and len(dataSet) < maxCombinations:
                candidate = Utils.generateUniqueVector(randomGenerator, dimension, dataSet)
                improved = False
                
                for vectorToDiscard in dataSet:
                    dataSetCopy = list(dataSet)
                    dataSetCopy.remove(vectorToDiscard)
                    dataSetCopy.append(candidate)
                    candidateError = errorFunction(dataSetCopy)
                    
                    if candidateError < bestError:
                        improved = True
                        dataSet = dataSetCopy
                        bestError = candidateError
                        break
                    
                if improved:
                    tries = 0
                else:
                    tries += 1
            
        return dataSet

    @staticmethod
    def transformDataSet(randomGenerator, dataSet, patternDataSetProperties):
        return map(lambda x: Utils.scale(Utils.addExtraBits(randomGenerator, list(x), patternDataSetProperties), patternDataSetProperties), dataSet)
    
    @staticmethod
    def addExtraBits(randomGenerator, vector, patternDataSetProperties):
        extraBits = patternDataSetProperties.get('extraBits')
        
        if extraBits == None:
            return vector
        
        if extraBits.get('values') in (0, 1):
            return vector + [extraBits.get('values')] * extraBits.get('number')
        
        return vector + Utils.randomBits(randomGenerator, extraBits.get('number'))

    @staticmethod
    def scale(vector, patternDataSetProperties):
        scale = patternDataSetProperties.get('scale')
        
        if scale == None:
            return vector
        
        if scale.get('type') == '1D':
            return Utils.scaleImpl(vector, scale.get('factor'))
        elif scale.get('type') == '2D':
            patternWidth = scale.get('patternWidth')
            patternHeight = scale.get('patternHeight')
            pattern2D = [[vector[i * patternWidth + j] for j in xrange(patternWidth)] for i in xrange(patternHeight)]
            
            pattern2D = map(lambda x: Utils.scaleImpl(x, scale.get('widthFactor')), pattern2D)
            pattern2D = Utils.scaleImpl(pattern2D, scale.get('heightFactor'))
            
            return [j for i in pattern2D for j in i]
    
    @staticmethod
    def scaleImpl(listOfItems, factor):
        return [j for i in listOfItems for j in [i] * factor]
