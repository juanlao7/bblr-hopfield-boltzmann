import argparse
import json
import re
from bblr.generators.MainGenerator import MainGenerator
from bblr.models.ModelFactory import ModelFactory
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
    print 'Data set size:', n
    dimension = len(dataSet[0])
    print 'Pattern size:', dimension
    mean = 0.0
    k = 0
    
    for i in xrange(n):
        for j in xrange(i + 1, n):
            d = distance(dataSet[i], dataSet[j])
            mean += d
            k += 1
    
    mean /= k 
    print 'Mean distance:', mean

    variance = 0.0

    for i in xrange(n):
        for j in xrange(i + 1, n):
            d = distance(dataSet[i], dataSet[j])
            variance += (d - mean)**2

    variance /= k
    stdev = math.sqrt(variance)
    print 'Distance standard deviation:', stdev
    print 'Relative mean distance:', mean / dimension
    print 'Relative distance standard deviation:', stdev / dimension
    print '-------'

def generateModel(modelPropertiesCombination):
    raise 'Not implemented yet'

if __name__ == '__main__':
    # Parsing arguments
    parser = argparse.ArgumentParser(prog='bblr-hopfield-boltzmann analyzer', description='Automatic script to obtain the final results of the project bblr-hopfield-boltzmann.')
    parser.add_argument('pattern_data_set_properties_file', help='Path to a file containing the combinations of pattern data set properties you want to test. See ' + PATTERN_FORMAT_URL)
    parser.add_argument('model_properties_file', help='Path to a file containing the combinations of model properties you want to test. See ' + MODELS_FORMAT_URL)
    parser.add_argument('--just-analyze', action='store_true', help='Just create the random pattern data sets and analyze them. Do not create or train the models.')
    arguments = parser.parse_args()
    
    # Loading preferences
    modelPropertiesCombinations = loadJsonFile(arguments.model_properties_file)
    patternDataSetPropertiesCombinations = loadJsonFile(arguments.pattern_data_set_properties_file)
    
    # Main loop
    
    for patternDataSetPropertiesCombination in patternDataSetPropertiesCombinations:
        patternDataSetGenerator = MainGenerator(patternDataSetPropertiesCombination)
        patternDataSet = patternDataSetGenerator.getPatterns()
        
        if arguments.just_analyze:
            analyze(patternDataSet)
        else:
            for modelPropertiesCombination in modelPropertiesCombinations:
                modelFactory = ModelFactory(modelPropertiesCombination)
                model = modelFactory.buildModel()
                model.train(patternDataSet)
                #result = model.test(inputDataSet)
                #result.add(other things such as the training cost)
                #print result
        
            raise 'die!'
