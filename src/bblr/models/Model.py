import time
import numpy
from bblr.Utils import Utils

class Model(object):
    def test(self, inputDataSet, patternDataSet):
        times = []
        allIterations = []
        successfulEquilibriums = 0
        unsuccessfulEquilibriums = 0
        spuriousEquilibriums = 0
        
        for inputVector in inputDataSet:
            associatedPattern = self.findNearestPattern(inputVector, patternDataSet)
            
            time = self.getTime()
            output, iterations = self.input(inputVector)
            time = self.getTime() - time
            
            allIterations.append(iterations)
            times.append(time)
            
            if tuple(associatedPattern) == tuple(output):
                successfulEquilibriums += 1
            else:
                unsuccessfulEquilibriums += 1
                
                if self.isSpurious(associatedPattern, output):
                    spuriousEquilibriums += 1
        
        return {
            'timeMean': numpy.mean(times),
            'timeStdev': numpy.std(times),
            'iterationsMean': numpy.mean(allIterations),
            'iterationsStdev': numpy.std(allIterations),
            'successfulEquilibriums': successfulEquilibriums,
            'unsuccessfulEquilibriums': unsuccessfulEquilibriums,
            'spuriousEquilibriums': spuriousEquilibriums
        }

    def getTime(self):
        return int(round(time.time() * 1000))
    
    def findNearestPattern(self, inputVector, patternDataSet):
        minD = None
        minPattern = None
        
        for pattern in patternDataSet:
            d = Utils.distance(inputVector, pattern)
            
            if minD == None or d < minD:
                minD = d
                minPattern = pattern
    
        return minPattern
    
    def isSpurious(self, vector1, vector2):
        for i, j in zip(vector1, vector2):
            if i == j:
                return False
        
        return True
    