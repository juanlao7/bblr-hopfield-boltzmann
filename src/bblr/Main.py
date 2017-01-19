import argparse
import json
import re
from bblr.patterns.MainPatternGenerator import MainPatternGenerator
from bblr.models.ModelFactory import ModelFactory
from bblr.inputs.MainInputGenerator import MainInputGenerator

PATTERN_FORMAT_URL = 'https://github.com/juanlao7/bblr-hopfield-boltzmann/wiki/Pattern-data-set-properties-file-format'
MODELS_FORMAT_URL = 'https://github.com/juanlao7/bblr-hopfield-boltzmann/wiki/Pattern-data-set-properties-file-format'
INPUT_FORMAT_URL = 'https://github.com/juanlao7/bblr-hopfield-boltzmann/wiki/Input-data-set-properties-file-format'

ANALYSIS_LABELS = [
    # Pattern data set analysis
    ['patternDataSetSize', 'Pattern data set size'],
    ['patternDimension', 'Pattern dimension'],
    ['patternsDistanceMean', 'Distance between patterns mean'],
    ['patternsDistanceStdev', 'Distance between patterns standard deviation'],
    
    # Model properties
    ['model', 'Model'],
    ['trainingRule', 'Training rule'],
    ['hiddenNeurons', 'Number of hidden neurons'],
    ['learningRate', 'Learning rate'],
    ['weightDecay', 'Weight decay'],
    ['momentum', 'Momentum'],
    ['batchSize', 'Batch size'],
    
    # Validation results
    ['successfullyStoredPatterns', 'Number of stored patterns'],
    ['unsuccessfullyStoredPatterns', 'Number of not stored patterns'],
    
    # Input data set analysis
    ['inputDataSetSize', 'Input data set size'],
    ['inputDimension', 'Input vector dimension'],
    ['inputMinimumDistanceMean', 'Minimum distance of inputs to patterns mean'],
    ['inputMinimumDistanceStdev', 'Minimum distance of inputs to patterns standard deviation'],
    
    # Test results
    ['timeMean', 'CPU time mean'],
    ['timeStdev', 'CPU time standard deviation'],
    ['iterationsMean', 'Iterations mean'],
    ['iterationsStdev', 'Iterations standard deviation'],
    ['successfulEquilibriums', 'Successful equilibriums'],
    ['unsuccessfulEquilibriums', 'Unsuccessful equilibriums'],
    ['spuriousEquilibriums', 'Spurious equilibriums']
]

def loadJsonFile(path):
    with open(path) as handler:
        data = handler.read()
        data = re.sub(re.compile("/\*.*?\*/", re.DOTALL), '', data) # remove all occurrence streamed comments (/* COMMENT */)
        data = re.sub(re.compile("//.*?\n" ), '', data)             # remove all occurrence single line comments (// COMMENT\n)
        return json.loads(data)

def printAnalysis(analysis, identation=0):
    for key, label in ANALYSIS_LABELS:
        if key in analysis:
            print '\t' * identation, label, ':', analysis[key] 
    
    print

if __name__ == '__main__':
    # Parsing arguments
    parser = argparse.ArgumentParser(prog='bblr-hopfield-boltzmann analyzer', description='Automatic script to obtain the final results of the project bblr-hopfield-boltzmann.')
    parser.add_argument('pattern_data_set_properties_file', help='Path to a file containing the combinations of pattern data set properties you want to test. See ' + PATTERN_FORMAT_URL)
    parser.add_argument('model_properties_file', help='Path to a file containing the combinations of model properties you want to test. See ' + MODELS_FORMAT_URL)
    parser.add_argument('input_data_set_properties_file', help='Path to a file containing the combinations of input data set properties you want to test. See ' + INPUT_FORMAT_URL)
    parser.add_argument('--seed', help='This random seed is added to the seed defined in the configuration files to obtain different results.', default=0, type=int)
    parser.add_argument('--just-analyze-patterns', action='store_true', help='Just create the random pattern data sets and analyze them. Do not do anything else.')
    parser.add_argument('--just-analyze-inputs', action='store_true', help='Just create the random pattern data sets, the random input data sets and analyze them. Do not do anything else.')
    parser.add_argument('--out', dest='results_file', help='Store the results as a JSON file.')
    arguments = parser.parse_args()
    
    # Loading preferences
    patternDataSetPropertiesCombinations = loadJsonFile(arguments.pattern_data_set_properties_file)
    modelPropertiesCombinations = loadJsonFile(arguments.model_properties_file)
    inputDataSetPropertiesCombinations = loadJsonFile(arguments.input_data_set_properties_file)
    
    # Main loop
    results = []
    
    for patternDataSetProperties in patternDataSetPropertiesCombinations:
        print 'PATTERN:', patternDataSetProperties
        patternDataSetGenerator = MainPatternGenerator(patternDataSetProperties, arguments.seed)
        patternDataSet = patternDataSetGenerator.getPatterns()
        originalPatternDataSet = patternDataSetGenerator.getOriginalPatterns()
        
        patternDataSetAnalysis = patternDataSetGenerator.analyze()
        printAnalysis(patternDataSetAnalysis, 1)
        
        if not arguments.just_analyze_patterns:
            for modelProperties in modelPropertiesCombinations:
                print '\tMODEL:', modelProperties
                modelFactory = ModelFactory(modelProperties, arguments.seed)
                model = modelFactory.buildModel()
                
                trainingResults = model.train(patternDataSet)
                validationResults = model.test(patternDataSet, patternDataSet)
                
                validationResults = {
                    'successfullyStoredPatterns': validationResults['successfulEquilibriums'],
                    'unsuccessfullyStoredPatterns': validationResults['unsuccessfulEquilibriums']
                }
                
                for inputDataSetProperties in inputDataSetPropertiesCombinations:
                    print '\t\tINPUT:', inputDataSetProperties
                    inputDataSetGenerator = MainInputGenerator(inputDataSetProperties, originalPatternDataSet, patternDataSetProperties, arguments.seed)
                    inputDataSet = inputDataSetGenerator.getInputs()
                    
                    inputDataSetAnalysis = inputDataSetGenerator.analyze()
                    printAnalysis(inputDataSetAnalysis, 3)
                    
                    if not arguments.just_analyze_inputs:
                        testResults = model.test(inputDataSet, patternDataSet)
                        
                        print '\t\t\tRESULT:'
                        printAnalysis(testResults, 3)
                        
                        result = {}
                        result.update(patternDataSetAnalysis)
                        result.update(modelProperties)
                        result.update(trainingResults)
                        result.update(validationResults)
                        result.update(inputDataSetAnalysis)
                        result.update(testResults)
                        
                        results.append(result)
    
    if arguments.results_file:
        handler = open(arguments.results_file, 'w')
        handler.write(json.dumps(results, indent=4, sort_keys=True))
        handler.close()
