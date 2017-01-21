import argparse
from Utils import Utils

PATTERN_DATA_SETS_PER_TABLE = 100

def getInterval(arrayOfDictionaries, key):
    # TODO: return "X+-Y"
    
    for element in arrayOfDictionaries:
        return element[key]

def getObject(parent, key, defaultObject):
    if key in parent:
        return parent[key]
    
    parent[key] = defaultObject
    return parent[key]

if __name__ == '__main__':
    # Parsing arguments
    parser = argparse.ArgumentParser(prog='bblr-hopfield-boltzmann results to LaTeX script', description='Automatic script to convert the results of the project bblr-hopfield-boltzmann into LaTeX.')
    parser.add_argument('result_files', nargs='+', help='List of result JSON files.')
    arguments = parser.parse_args()

    # Loading results.
    results = []
    
    for resultFile in arguments.result_files:
        results += Utils.loadJsonFile(resultFile)
    
    # Organizing results.
    schema = {}
    patternDataSetResultDictionary = {}
    modelResultDictionary = {}
    inputDataSetResultDictionary = {}
    trainingAndValidationResultDictionary = {}
    testingResultDictionary = {}
    
    for result in results:
        # Schema.
        patternDataSet = getObject(schema, result['patternDataSetId'], {})
        model = getObject(patternDataSet, result['modelId'], {})
        inputDataSet = getObject(model, result['inputDataSetId'], [])
        inputDataSet.append(result)
        
        # Index tables.
        getObject(patternDataSetResultDictionary, result['patternDataSetId'], []).append(result)
        getObject(modelResultDictionary, result['modelId'], []).append(result)
        getObject(inputDataSetResultDictionary, result['inputDataSetId'], []).append(result)
        getObject(trainingAndValidationResultDictionary, str(result['patternDataSetId']) + ':' + str(result['modelId']), []).append(result)
        getObject(testingResultDictionary, str(result['patternDataSetId']) + ':' + str(result['modelId']) + ':' + str(result['inputDataSetId']), []).append(result)
    
    patternDataSetIndex = {}
    modelIndex = {}
    inputDataSetIndex = {}
    trainingAndValidationIndex = {}
    testingIndex = {}

    for patternDataSetId, patternDataSetResults in patternDataSetResultDictionary.iteritems():
        patternDataSetIndex['P' + str(patternDataSetId)] = [
            ['Data set size', patternDataSetResults[0]['patternDataSetSize']],
            ['Pattern size', patternDataSetResults[0]['patternDimension']],
            ['Mean distance between two different patterns', getInterval(patternDataSetResults, 'patternsDistanceMean')],
            ['Standard deviation of distance between two different patterns', getInterval(patternDataSetResults, 'patternsDistanceStdev')],
        ]

    for modelId, modelResults in modelResultDictionary.iteritems():
        if modelResults[0]['model'] == 'hopfield':
            modelInfo = [
                ['Model', 'Hopfield'],
                ['Learning rule', modelResults[0]['trainingRule'].capitalize()]
            ]
        else:
            modelInfo = [
                ['Model', 'Restricted Boltzmann Machine'],
                ['Number of hidden neurons', modelResults[0]['hiddenNeurons']],
                ['Learning rate', modelResults[0]['learningRate']],
                ['Weight decay', modelResults[0]['weightDecay']],
                ['Momentum', 1.0 if not modelResults[0]['momentum'] else '0.5 for the first 5 epochs, 0.9 after'],
                ['Patterns per batch', modelResults[0]['batchSize']]
            ]
    
        modelIndex['M' + str(modelId)] = modelInfo
    
    for inputDataSetId, inputDataSetResults in inputDataSetResultDictionary.iteritems():
        inputDataSetIndex['I' + str(inputDataSetId)] = [
            ['Data set size', inputDataSetResults[0]['inputDataSetSize']],
            ['Inputs per pattern', inputDataSetResults[0]['inputsPerPattern']],
            ['Mean minimum distance between an input and a pattern', getInterval(inputDataSetResults, 'inputMinimumDistanceMean')],
            ['Standard deviation of minimum distance between an input and a pattern', getInterval(inputDataSetResults, 'inputMinimumDistanceStdev')]
        ]

    for key, trainingAndValidationResults in trainingAndValidationResultDictionary.iteritems():
        patternDataSetId, modelId = key.split(':')
        
        trainingInfo = [
            ['Successfully stored patterns', getInterval(trainingAndValidationResults, 'successfullyStoredPatterns')],
            ['Unsuccessfully stored patterns', getInterval(trainingAndValidationResults, 'unsuccessfullyStoredPatterns')]
            # TODO CPU time
        ]
        
        if trainingAndValidationResults[0]['model'] == 'restricted-boltzmann-machine':
            trainingInfo += [
                ['Training epochs', getInterval(trainingAndValidationResults, 'trainingEpochs')]                
            ]
        
        trainingAndValidationIndex['Training M' + modelId + ' with P' + patternDataSetId] = trainingInfo
    
    for key, testingResults in testingResultDictionary.iteritems():
        patternDataSetId, modelId, inputDataSetId = key.split(':')
        
        testingIndex['Testing I' + inputDataSetId + ' in M' + modelId + ' trained with P' + patternDataSetId] = [
            # Take care, these properties assume that all input data set sizes are equal.
            ['Successful equilibriums', getInterval(testingResults, 'successfulEquilibriums')],
            ['Unsuccessful equilibriums', getInterval(testingResults, 'unsuccessfulEquilibriums')],
            ['Spurious pattern recalls', getInterval(testingResults, 'spuriousEquilibriums')],          # TODO decide if we want to put this property only in hopfield
            ['Mean CPU time per recall', getInterval(testingResults, 'timeMean')],
            ['Standard deviation of CPU time per recall', getInterval(testingResults, 'timeStdev')]
        ]
    
    # Generating LaTeX code
    numberOfPatterns = len(patternDataSetResultDictionary)
    numberOfInputs = len(inputDataSetResultDictionary)
    numberOfModels = len(modelResultDictionary)
    
    print """
    \\begin{table}[]
    \\centering
    \\label{my-label}
    \\begin{tabular}{c|""" + ((('c' * numberOfInputs) + '|') * numberOfPatterns) + """}
    \\cline{2-""" + str(numberOfPatterns * numberOfInputs + 1) + """} 
    """
    
    for patternDataSetId, models in sorted(schema.iteritems()):
        print ' & \\multicolumn{' + str(numberOfInputs) + '}{c|}{\\textbf{P' + str(patternDataSetId) + '}}',
    
    print ' \\\\ \\cline{2-' + str(numberOfPatterns * numberOfInputs + 1) + '}'
    
    for _ in xrange(numberOfPatterns):
        for inputDataSetId in inputDataSetResultDictionary:
            print ' & I' + str(inputDataSetId),
    
    print ' \\\\ \\hline'
    
    resultId = 1
    
    for modelId in xrange(1, numberOfModels + 1):
        print '\\multicolumn{1}{|c|}{\\textbf{M' + str(modelId) + '}}',        
        
        for patternDataSetId in xrange(1, numberOfPatterns + 1):
            for inputDataSetId in xrange(1, numberOfInputs + 1):
                print ' & R' + str(resultId),
                resultId += 1
        
        if modelId == numberOfModels:
            print '\\\\  \\hline'
        else:
            print '\\\\ '
    
    print """
    \\end{tabular}
    \\caption{My caption}
    \\end{table}
    """
