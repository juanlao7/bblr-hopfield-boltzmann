import argparse
import json
import re
from bblr.generators.MainGenerator import MainGenerator
from math import factorial
import random
import math

PATTERN_FORMAT_URL = 'https://github.com/juanlao7/bblr-hopfield-boltzmann/wiki/Pattern-data-set-properties-file-format'
MODELS_FORMAT_URL = 'https://github.com/juanlao7/bblr-hopfield-boltzmann/wiki/Pattern-data-set-properties-file-format'

def loadJsonFile(path):
    with open(path) as handler:
        data = handler.read()
        data = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,data) # remove all occurance streamed comments (/*COMMENT */) from string
        data = re.sub(re.compile("//.*?\n" ) ,"" ,data)             # remove all occurance singleline comments (//COMMENT\n ) from string
        return json.loads(data)

def distance(a, b):
    d = 0
    
    for i in xrange(len(a)):
        if a[i] != b[i]:
            d += 1
    
    return d 

def analyze(dataSet):
    n = len(dataSet)
    print 'Size:', n
    dimension = len(dataSet[0])
    print 'Dimension:', dimension
    mean = 0.0
    k = 0
    
    for i in xrange(n):
        for j in xrange(i + 1, n):
            d = distance(dataSet[i], dataSet[j])
            mean += d
            k += 1
    
    mean /= k 
    print 'Mean:', mean

    variance = 0.0

    for i in xrange(n):
        for j in xrange(i + 1, n):
            d = distance(dataSet[i], dataSet[j])
            variance += (d - mean)**2

    variance /= k
    stdev = math.sqrt(variance)
    print 'Stdev:', stdev
    print 'Relative mean:', mean / dimension
    print 'Relative stdev:', stdev / dimension
    print '-------'

def generateModel(modelPropertiesCombination):
    raise 'Not implemented yet'

if __name__ == '__main__':
    # Parsing arguments
    parser = argparse.ArgumentParser(prog='bblr-hopfield-boltzmann analyzer', description='Automatic script to obtain the final results of the project bblr-hopfield-boltzmann.')
    parser.add_argument('pattern_data_set_properties_file', help='Path to a file containing the combinations of pattern data set properties you want to test. See ' + PATTERN_FORMAT_URL)
    parser.add_argument('model_properties_file', help='Path to a file containing the combinations of model properties you want to test. See ' + MODELS_FORMAT_URL)
    arguments = parser.parse_args()
    
    # Loading preferences
    modelPropertiesCombinations = loadJsonFile(arguments.model_properties_file)
    patternDataSetPropertiesCombinations = loadJsonFile(arguments.pattern_data_set_properties_file)
    
    # Main loop
    
    for patternDataSetPropertiesCombination in patternDataSetPropertiesCombinations:
        patternDataSetGenerator = MainGenerator(patternDataSetPropertiesCombination)
        patterns = patternDataSetGenerator.getPatterns()
        analyze(patterns)
        
        if False:
            for modelPropertiesCombination in modelPropertiesCombinations:
                model = generateModel(modelPropertiesCombination)
                model.train(patternDataSetGenerator)
                #result = model.test(inputDataSet)
                #result.add(other things such as the training cost)
                #print result
