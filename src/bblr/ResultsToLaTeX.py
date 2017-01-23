import argparse
from Utils import Utils
import numpy

PATTERN_DATA_SETS_PER_MAIN_TABLE = 100
PATTERNS_TABLE_MAX_COLUMNS = 4
MODELS_TABLE_MAX_COLUMNS = 5
TRAINING_TABLE_MAX_COLUMNS = 3
TESTING_TABLE_MAX_COLUMNS = 4
DEFAULT_DECIMALS = 3

BLACKLIST_PATTERNS = sorted([])
BLACKLIST_MODELS = sorted([])
BLACKLIST_INPUTS = sorted([])

def getInterval(arrayOfDictionaries, key, decimals=DEFAULT_DECIMALS):
    values = map(lambda x: x[key], arrayOfDictionaries)
    mean = numberToString(numpy.mean(values), decimals)
    stdev = numberToString(numpy.std(values), decimals)
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

def parseKey(itemKey):
    return itemKey.replace('P_{0', 'P_{').replace('M_{0', 'M_{').replace('I_{0', 'I_{')

def generateIndexTable(indexTable, latexComment, caption, maxColumns=100000):
    print """
    % """ + latexComment + """
    
    \\section{""" + caption + """}

    \\begin{description}
    """
    
    numberOfProperties = len(indexTable[indexTable.keys()[0]])
    
    for propertyIndex in xrange(numberOfProperties):
        print '\\item [(' + str(propertyIndex + 1) + ')]', indexTable[indexTable.keys()[0]][propertyIndex][0] 

    print """
    \\end {description}
    """
        
    numberOfItems = len(indexTable)
    numberOfTables = len(range(0, numberOfItems, maxColumns))
    currentTableNumber = 1
    
    for i in xrange(0, numberOfItems, maxColumns):
        numberOfItemsInThisTable = min(i + maxColumns, numberOfItems) - i
        itemKeysOfThisTable = sorted(indexTable.keys())[i:i + numberOfItemsInThisTable]
        captionOfThisTable = caption if maxColumns > numberOfItems else caption + ' (' + str(currentTableNumber) + ' of ' + str(numberOfTables) + ')'
        currentTableNumber += 1 
        
        print """
        \\begin{table}[H]
        \\centering
        %\\label{my-label}
        \\begin{tabular}{c""" + ('c' * numberOfItemsInThisTable) + """}
        """
        
        for itemKey in itemKeysOfThisTable:
            print ' & ' + parseKey(itemKey),
        
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

def getIdAfterBlacklist(itemId, blackList):
    if itemId in blackList:
        return None
    
    newItemId = itemId
    
    for blackListedId in blackList:
        if blackListedId > itemId:
            break
        
        newItemId -= 1
    
    return newItemId

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
    patternDataSetResultDictionary = {}
    modelResultDictionary = {}
    inputDataSetResultDictionary = {}
    trainingAndValidationResultDictionary = {}
    testingResultDictionary = {}
    
    for result in results:
        # Managing the black list.
        result['patternDataSetId'] = getIdAfterBlacklist(result['patternDataSetId'], BLACKLIST_PATTERNS)
        result['modelId'] = getIdAfterBlacklist(result['modelId'], BLACKLIST_MODELS)
        result['inputDataSetId'] = getIdAfterBlacklist(result['inputDataSetId'], BLACKLIST_INPUTS)
        
        if None in (result['patternDataSetId'], result['modelId'], result['inputDataSetId']):
            continue

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
        patternDataSetIndexTable['$P_{' + str(patternDataSetId).zfill(2) + '}$'] = [
            ['Data set size', patternDataSetResults[0]['patternDataSetSize']],
            ['Pattern size', patternDataSetResults[0]['patternDimension']],
            ['Mean distance $\mu_{P_i}$ between two random different patterns', getInterval(patternDataSetResults, 'patternsDistanceMean')],
            ['Standard deviation of distance $\sigma_{P_i}$ between two random different patterns', getInterval(patternDataSetResults, 'patternsDistanceStdev')],
        ]

    for modelId, modelResults in modelResultDictionary.iteritems():
        if modelResults[0]['model'] == 'hopfield':
            modelInfo = [
                ['Model', 'Hopfield'],
                ['Learning rule', modelResults[0]['trainingRule'].capitalize()],
                ['Number of hidden neurons', ''],
                ['Learning rate', ''],
                #['Weight decay', ''],
                #['Momentum. By Hinton\'s recommendation[CITA], the training starts with a momentum of 0.5. Once the large initial progress in the reduction of the reconstruction error has settled down to gentle progress after 5 epochs, the momentum is increased to 0.9', ''],
                ['Patterns per batch', '']
            ]
        else:
            modelInfo = [
                ['Model', 'RBM'],
                ['Learning rule.', 'CD'],
                ['Number of hidden neurons.', modelResults[0]['hiddenNeurons']],
                ['Learning rate.', modelResults[0]['learningRate']],
                #['Weight decay.', modelResults[0]['weightDecay']],
                #['Momentum. By Hinton\'s recommendation[CITA], the training starts with a momentum of 0.5. Once the large initial progress in the reduction of the reconstruction error has settled down to gentle progress after 5 epochs, the momentum is increased to 0.9', 'no' if not modelResults[0]['momentum'] else 'yes'],
                ['Patterns per batch', modelResults[0]['batchSize']]
            ]
    
        modelIndexTable['$M_{' + str(modelId).zfill(2) + '}$'] = modelInfo
    
    for inputDataSetId, inputDataSetResults in inputDataSetResultDictionary.iteritems():
        for i in inputDataSetResults:
            i.update({'ratioInputMinimumDistanceMean': i['inputMinimumDistanceMean'] / float(i['patternsDistanceMean'])})
        
        inputDataSetIndexTable['$I_{' + str(inputDataSetId).zfill(2) + '}$'] = [
            ['Number of inputs per each pattern of the pattern data set', inputDataSetResults[0]['inputsPerPattern']],
            ['Mean minimum distance between a random input $v$ and the closest pattern to $v$, expressed as a proportion of the mean distance between 2 random patterns of the pattern data set', getInterval(inputDataSetResults, 'ratioInputMinimumDistanceMean')]
        ]

    for key, trainingAndValidationResults in trainingAndValidationResultDictionary.iteritems():
        for i in trainingAndValidationResults:
            i.update({'ratioStoredPatterns': i['successfullyStoredPatterns'] / float(i['patternDataSetSize'])})
        
        trainingInfo = [
            #['Successfully stored patterns', getInterval(trainingAndValidationResults, 'successfullyStoredPatterns')],
            #['Unsuccessfully stored patterns', getInterval(trainingAndValidationResults, 'unsuccessfullyStoredPatterns')],
            ['Ratio of stored patterns, proportional to the number of training patterns', getInterval(trainingAndValidationResults, 'ratioStoredPatterns')]
        ]
        
        if trainingAndValidationResults[0]['model'] == 'restricted-boltzmann':
            trainingInfo += [
                ['Training epochs', getInterval(trainingAndValidationResults, 'trainingEpochs', 1)]                
            ]
        else:
            trainingInfo += [
                ['Training epochs', '']                
            ]
        
        patternDataSetId, modelId = key.split(':')
        trainingAndValidationIndexTable['$\\{P_{' + patternDataSetId.zfill(2) + '},M_{' + modelId.zfill(2) + '}\\}$'] = trainingInfo
    
    for key, testingResults in testingResultDictionary.iteritems():
        for i in testingResults:
            i.update({'ratioSuccessfulEquilibriums': i['successfulEquilibriums'] / float(i['inputDataSetSize'])})
        
        patternDataSetId, modelId, inputDataSetId = key.split(':')
        
        testingIndexTable['$\\{P_{' + patternDataSetId.zfill(2) + '},M_{' + modelId.zfill(2) + '},I_{' + inputDataSetId.zfill(2) + '}\\}$'] = [
            #['Successful recalls', getInterval(testingResults, 'successfulEquilibriums')],
            #['Unsuccessful recalls', getInterval(testingResults, 'unsuccessfulEquilibriums')],
            #['Spurious pattern recalls', getInterval(testingResults, 'spuriousEquilibriums')],
            ['Ratio of successful recalls, proportional to the number of test inputs', getInterval(testingResults, 'ratioSuccessfulEquilibriums')],
            ['Mean CPU time (ms) per recall', getInterval(testingResults, 'timeMean', 1)],
            #['Standard deviation of CPU time per recall', getInterval(testingResults, 'timeStdev')]
        ]
    
    numberOfPatterns = len(patternDataSetResultDictionary)
    numberOfInputs = len(inputDataSetResultDictionary)
    numberOfModels = len(modelResultDictionary)
    
    # Generating LaTeX code of the main table.
    
    print """
    \\documentclass[12pt]{article}
    \\usepackage{float}
    \\begin{document}
    """
    
    if False:
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
                print ' & \\multicolumn{' + str(numberOfInputs) + '}{c|}{\\textbf{$P_{' + str(patternDataSetId) + '}$}}',
            
            print ' \\\\ \\cline{2-' + str(numberOfPatternsInThisTable * numberOfInputs + 1) + '}'
            
            for _ in xrange(numberOfPatternsInThisTable):
                for inputDataSetId in xrange(1, numberOfInputs + 1):
                    print ' & $I_{' + str(inputDataSetId) + '}$',
            
            print ' \\\\ \\hline'
            
            for modelId in xrange(1, numberOfModels + 1):
                print '\\multicolumn{1}{|c|}{\\textbf{$M_{' + str(modelId) + '}$}}',
                
                for patternDataSetId in xrange(i + 1, i + numberOfPatternsInThisTable + 1):
                    for inputDataSetId in xrange(1, numberOfInputs + 1):
                        print ' & $\\{P_{' + str(patternDataSetId) + '},M_{' + str(modelId) + '},I_{' + str(inputDataSetId) + '}\\}$'
                
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
    generateIndexTable(patternDataSetIndexTable, 'PATTERN DATA SETS TABLE', 'Analyzed pattern data sets', PATTERNS_TABLE_MAX_COLUMNS)
    generateIndexTable(modelIndexTable, 'MODELS TABLE', 'Analyzed models', MODELS_TABLE_MAX_COLUMNS)
    generateIndexTable(inputDataSetIndexTable, 'INPUT DATA SETS TABLE', 'Tested inputs')
    generateIndexTable(trainingAndValidationIndexTable, 'TRAININGS AND VALIDATIONS TABLE', 'Obtained training results', TRAINING_TABLE_MAX_COLUMNS)
    generateIndexTable(testingIndexTable, 'TESTING TABLE', 'Obtained testing results', TESTING_TABLE_MAX_COLUMNS)
    
    print """
    \\end{document}
    """
    