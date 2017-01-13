import argparse
import json
import re
from bblr.patterns.MainPatternGenerator import MainPatternGenerator
from bblr.models.ModelFactory import ModelFactory
from bblr.inputs.MainInputGenerator import MainInputGenerator

PATTERN_FORMAT_URL = 'https://github.com/juanlao7/bblr-hopfield-boltzmann/wiki/Pattern-data-set-properties-file-format'
MODELS_FORMAT_URL = 'https://github.com/juanlao7/bblr-hopfield-boltzmann/wiki/Pattern-data-set-properties-file-format'
INPUT_FORMAT_URL = 'https://github.com/juanlao7/bblr-hopfield-boltzmann/wiki/Input-data-set-properties-file-format'

PATTERN_ANALYSIS_LABELS = ['Pattern data set size', 'Dimension', 'Mean distance', 'Distance standard deviation', 'Relative mean distance', 'Relative distance standard deviation']
INPUT_ANALYSIS_LABELS = ['Input data set size', 'Dimension', 'Mean minimum distance', 'Minimum distance standard deviation', 'Relative mean minimum distance', 'Relative minimum distance standard deviation']

def loadJsonFile(path):
    with open(path) as handler:
        data = handler.read()
        data = re.sub(re.compile("/\*.*?\*/", re.DOTALL), '', data) # remove all occurrence streamed comments (/* COMMENT */)
        data = re.sub(re.compile("//.*?\n" ), '', data)             # remove all occurrence single line comments (// COMMENT\n)
        return json.loads(data)

def printAnalysis(analysis, labels, identation=0):
    for i in xrange(len(analysis)):
        print '\t' * identation, labels[i], ':', analysis[i]

if __name__ == '__main__':
    # Parsing arguments
    parser = argparse.ArgumentParser(prog='bblr-hopfield-boltzmann analyzer', description='Automatic script to obtain the final results of the project bblr-hopfield-boltzmann.')
    parser.add_argument('pattern_data_set_properties_file', help='Path to a file containing the combinations of pattern data set properties you want to test. See ' + PATTERN_FORMAT_URL)
    parser.add_argument('model_properties_file', help='Path to a file containing the combinations of model properties you want to test. See ' + MODELS_FORMAT_URL)
    parser.add_argument('input_data_set_properties_file', help='Path to a file containing the combinations of input data set properties you want to test. See ' + INPUT_FORMAT_URL)
    parser.add_argument('--seed', help='This random seed is added to the seed defined in the configuration files to obtain different results.', default=0, type=int)
    parser.add_argument('--just-analyze-patterns', action='store_true', help='Just create the random pattern data sets and analyze them. Do not do anything else.')
    parser.add_argument('--just-analyze-inputs', action='store_true', help='Just create the random pattern data sets, the random input data sets and analyze them. Do not do anything else.')
    arguments = parser.parse_args()
    
    # Loading preferences
    patternDataSetPropertiesCombinations = loadJsonFile(arguments.pattern_data_set_properties_file)
    modelPropertiesCombinations = loadJsonFile(arguments.model_properties_file)
    inputDataSetPropertiesCombinations = loadJsonFile(arguments.input_data_set_properties_file)
    
    # Main loop
    
    for patternDataSetProperties in patternDataSetPropertiesCombinations:
        print 'PATTERN:', patternDataSetProperties
        patternDataSetGenerator = MainPatternGenerator(patternDataSetProperties, arguments.seed)
        patternDataSet = patternDataSetGenerator.getPatterns()
        printAnalysis(patternDataSetGenerator.analyze(), PATTERN_ANALYSIS_LABELS, 1)
        print
        
        if not arguments.just_analyze_patterns:
            for modelProperties in modelPropertiesCombinations:
                print '\tMODEL:', modelProperties
                modelFactory = ModelFactory(modelProperties)
                model = modelFactory.buildModel()
                model.train(patternDataSet)
                
                for inputDataSetProperties in inputDataSetPropertiesCombinations:
                    print '\t\tINPUT:', inputDataSetProperties
                    inputDataSetGenerator = MainInputGenerator(inputDataSetProperties, patternDataSet, patternDataSetProperties, arguments.seed)
                    inputDataSet = inputDataSetGenerator.getInputs()
                    printAnalysis(inputDataSetGenerator.analyze(), INPUT_ANALYSIS_LABELS, 4)
                    
                    if not arguments.just_analyze_inputs:
                        testResults = model.test(inputDataSet)
