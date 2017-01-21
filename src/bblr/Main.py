import argparse
from bblr.patterns.MainPatternGenerator import MainPatternGenerator
from bblr.models.ModelFactory import ModelFactory
from bblr.inputs.MainInputGenerator import MainInputGenerator
from bblr.Utils import Utils
import json

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

    # Training results
    ['trainingEpochs', 'Training epochs'],
    
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
    ['iterationsMean', 'Iterations until equilibrium mean'],
    ['iterationsStdev', 'Iterations until equilibrium standard deviation'],
    ['successfulEquilibriums', 'Successful equilibriums'],
    ['unsuccessfulEquilibriums', 'Unsuccessful equilibriums'],
    ['spuriousEquilibriums', 'Spurious equilibriums']
]

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
    patternDataSetPropertiesCombinations = Utils.loadJsonFile(arguments.pattern_data_set_properties_file)
    modelPropertiesCombinations = Utils.loadJsonFile(arguments.model_properties_file)
    inputDataSetPropertiesCombinations = Utils.loadJsonFile(arguments.input_data_set_properties_file)
    
    # Main loop
    results = []
    patternDataSetId = 1
    
    for patternDataSetProperties in patternDataSetPropertiesCombinations:
        patternDataSetProperties['patternId'] = patternDataSetId
        patternDataSetId += 1
        
        print 'PATTERN:', patternDataSetProperties
        patternDataSetGenerator = MainPatternGenerator(patternDataSetProperties, arguments.seed)
        patternDataSet = patternDataSetGenerator.getPatterns()
        originalPatternDataSet = patternDataSetGenerator.getOriginalPatterns()
        
        patternDataSetAnalysis = patternDataSetGenerator.analyze()
        printAnalysis(patternDataSetAnalysis, 1)
        
        if not arguments.just_analyze_patterns:
            modelId = 1
            
            for modelProperties in modelPropertiesCombinations:
                modelProperties['modelId'] = modelId
                modelId += 1
                
                if not arguments.just_analyze_inputs:
                    print '\tMODEL:', modelProperties
                    modelFactory = ModelFactory(modelProperties, arguments.seed)
                    model = modelFactory.buildModel()
                    
                    trainingResults = model.train(patternDataSet)
                    printAnalysis(trainingResults, 2)

                    validationResults = model.test(patternDataSet, patternDataSet)
                    
                    validationResults = {
                        'successfullyStoredPatterns': validationResults['successfulEquilibriums'],
                        'unsuccessfullyStoredPatterns': validationResults['unsuccessfulEquilibriums']
                    }

                    printAnalysis(validationResults, 2)
                
                inputId = 1
                
                for inputDataSetProperties in inputDataSetPropertiesCombinations:
                    inputDataSetProperties['inputId'] = inputId
                    inputId += 1
                    
                    print '\t\tINPUT:', inputDataSetProperties
                    inputDataSetGenerator = MainInputGenerator(inputDataSetProperties, originalPatternDataSet, patternDataSet, patternDataSetProperties, arguments.seed)
                    inputDataSet = inputDataSetGenerator.getInputs()
                    
                    inputDataSetAnalysis = inputDataSetGenerator.analyze()
                    inputDataSetAnalysis['inputsPerPattern'] = inputDataSetProperties['inputsPerPattern']
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
