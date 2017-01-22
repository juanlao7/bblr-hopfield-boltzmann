import argparse
from Utils import Utils
import numpy

PATTERN_DATA_SETS_PER_MAIN_TABLE = 100
TESTING_TABLE_MAX_COLUMNS = 5
DEFAULT_DECIMALS = 3

def getInterval(arrayOfDictionaries, key):
    values = map(lambda x: x[key], arrayOfDictionaries)
    mean = numberToString(numpy.mean(values))
    stdev = numberToString(numpy.std(values))
        
    if stdev == '0':
        return mean
    
    return mean + '$\\pm$' + stdev

def numberToString(number, decimals=DEFAULT_DECIMALS):
    powerOfTen = 10 ** decimals
    
    number = round(number * powerOfTen) / powerOfTen
    
    if number == int(number):
        return str(int(number))
    
    return str(number)

def getObject(parent, key, defaultObject):
    if key in parent:
        return parent[key]
    
    parent[key] = defaultObject
    return parent[key]

def generateIndexTable(indexTable, latexComment, caption, maxColumns=100000):
    print """
    % """ + latexComment + """
    
    """
        
    numberOfItems = len(indexTable)
    numberOfProperties = len(indexTable[indexTable.keys()[0]])
    numberOfTables = len(range(0, numberOfItems, maxColumns))
    currentTableNumber = 1
    
    for i in xrange(0, numberOfItems, maxColumns):
        numberOfItemsInThisTable = min(i + maxColumns, numberOfItems) - i
        itemKeysOfThisTable = sorted(indexTable.keys())[i:i + numberOfItemsInThisTable]
        captionOfThisTable = caption if maxColumns > numberOfItems else caption + ' (' + str(currentTableNumber) + ' of ' + str(numberOfTables) + ')'
        currentTableNumber += 1 
        
        print """
        \\begin{table}[]
        \\centering
        \\label{my-label}
        \\begin{tabular}{c""" + ('c' * numberOfItemsInThisTable) + """}
        """
        
        for itemKey in itemKeysOfThisTable:
            print ' & ' + itemKey,
        
        print ' \\\\ \\cline{2-' + str(numberOfItemsInThisTable + 1) + '}'
        
        for propertyIndex in xrange(numberOfProperties):
            print '(' + str(propertyIndex + 1) + ')',
            
            for itemKey in itemKeysOfThisTable:
                print ' &', indexTable[itemKey][propertyIndex][1],
            
            if propertyIndex != numberOfProperties - 1:
                print '\\\\'
        
        print """
        \\end{tabular}
        \\caption{""" + captionOfThisTable + """}
        \\end{table}
        """
    
    print """
    \\begin{description}
    """
    
    for propertyIndex in xrange(numberOfProperties):
        print '\\item [(' + str(propertyIndex + 1) + ')]', indexTable[indexTable.keys()[0]][propertyIndex][0] 

    print """
    \\end {description}
    """

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
    
    patternDataSetIndexTable = {}
    modelIndexTable = {}
    inputDataSetIndexTable = {}
    trainingAndValidationIndexTable = {}
    testingIndexTable = {}

    for patternDataSetId, patternDataSetResults in patternDataSetResultDictionary.iteritems():
        patternDataSetIndexTable['P' + str(patternDataSetId)] = [
            ['Data set size', patternDataSetResults[0]['patternDataSetSize']],
            ['Pattern size', patternDataSetResults[0]['patternDimension']],
            ['Mean distance between two different patterns', getInterval(patternDataSetResults, 'patternsDistanceMean')],
            ['Standard deviation of distance between two different patterns', getInterval(patternDataSetResults, 'patternsDistanceStdev')],
        ]

    for modelId, modelResults in modelResultDictionary.iteritems():
        if modelResults[0]['model'] == 'hopfield':
            modelInfo = [
                ['Model', 'Hopfield'],
                ['Learning rule', modelResults[0]['trainingRule'].capitalize()],
                ['Number of hidden neurons', ''],
                ['Learning rate', ''],
                ['Weight decay', ''],
                ['Momentum', ''],
                ['Patterns per batch', '']
            ]
        else:
            modelInfo = [
                ['Model', 'RBM'],
                ['Learning rule', 'CD'],
                ['Number of hidden neurons', modelResults[0]['hiddenNeurons']],
                ['Learning rate', modelResults[0]['learningRate']],
                ['Weight decay', modelResults[0]['weightDecay']],
                ['Momentum', 1.0 if not modelResults[0]['momentum'] else 'recommended'],
                ['Patterns per batch', modelResults[0]['batchSize']]
            ]
    
        modelIndexTable['M' + str(modelId)] = modelInfo
    
    for inputDataSetId, inputDataSetResults in inputDataSetResultDictionary.iteritems():
        inputDataSetIndexTable['I' + str(inputDataSetId)] = [
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
        
        if trainingAndValidationResults[0]['model'] == 'restricted-boltzmann':
            trainingInfo += [
                ['Training epochs', getInterval(trainingAndValidationResults, 'trainingEpochs')]                
            ]
        else:
            trainingInfo += [
                ['Training epochs', '']                
            ]
        
        trainingAndValidationIndexTable['\\{P' + patternDataSetId + ',M' + modelId + '\\}'] = trainingInfo
    
    for key, testingResults in testingResultDictionary.iteritems():
        patternDataSetId, modelId, inputDataSetId = key.split(':')
        
        testingIndexTable['\\{P' + patternDataSetId + ',M' + modelId + ',I' + inputDataSetId + '\\}'] = [
            # Take care, these properties assume that all input data set sizes are equal.
            ['Successful recalls', getInterval(testingResults, 'successfulEquilibriums')],
            ['Unsuccessful recalls', getInterval(testingResults, 'unsuccessfulEquilibriums')],
            ['Spurious pattern recalls', getInterval(testingResults, 'spuriousEquilibriums')],          # TODO decide if we want to put this property only in hopfield
            ['Mean CPU time per recall', getInterval(testingResults, 'timeMean')],
            ['Standard deviation of CPU time per recall', getInterval(testingResults, 'timeStdev')]
        ]
    
    numberOfPatterns = len(patternDataSetResultDictionary)
    numberOfInputs = len(inputDataSetResultDictionary)
    numberOfModels = len(modelResultDictionary)
    
    # Generating LaTeX code of the main table.
    
    print """
    % MAIN TABLES
    """
    
    for i in xrange(0, numberOfPatterns, PATTERN_DATA_SETS_PER_MAIN_TABLE):
        numberOfPatternsInThisTable = min(i + PATTERN_DATA_SETS_PER_MAIN_TABLE, numberOfPatterns) - i
        
        print """
        \\begin{table}[]
        \\centering
        \\label{my-label}
        \\begin{tabular}{c|""" + ((('c' * numberOfInputs) + '|') * numberOfPatternsInThisTable) + """}
        \\cline{2-""" + str(numberOfPatternsInThisTable * numberOfInputs + 1) + """} 
        """
        
        for patternDataSetId in xrange(i + 1, i + numberOfPatternsInThisTable + 1):
            print ' & \\multicolumn{' + str(numberOfInputs) + '}{c|}{\\textbf{P' + str(patternDataSetId) + '}}',
        
        print ' \\\\ \\cline{2-' + str(numberOfPatternsInThisTable * numberOfInputs + 1) + '}'
        
        for _ in xrange(numberOfPatternsInThisTable):
            for inputDataSetId in xrange(1, numberOfInputs + 1):
                print ' & I' + str(inputDataSetId),
        
        print ' \\\\ \\hline'
        
        for modelId in xrange(1, numberOfModels + 1):
            print '\\multicolumn{1}{|c|}{\\textbf{M' + str(modelId) + '}}',
            
            for patternDataSetId in xrange(i + 1, i + numberOfPatternsInThisTable + 1):
                for inputDataSetId in xrange(1, numberOfInputs + 1):
                    print ' & \\{P' + str(patternDataSetId) + ',M' + str(modelId) + ',I' + str(inputDataSetId) + '\\}'
            
            if modelId == numberOfModels:
                print '\\\\  \\hline'
            else:
                print '\\\\ '
        
        print """
        \\end{tabular}
        \\caption{My caption}
        \\end{table}
        """
    
    # Generating LaTeX code of index tables.
    generateIndexTable(patternDataSetIndexTable, 'PATTERN DATA SETS TABLE', 'Analyzed pattern data sets')
    generateIndexTable(modelIndexTable, 'MODELS TABLE', 'Analyzed models')
    generateIndexTable(inputDataSetIndexTable, 'INPUT DATA SETS TABLE', 'Tested inputs')
    generateIndexTable(trainingAndValidationIndexTable, 'TRAININGS AND VALIDATIONS TABLE', 'Obtained training results')
    generateIndexTable(testingIndexTable, 'TESTING TABLE', 'Obtained testing results', TESTING_TABLE_MAX_COLUMNS)
    