import argparse
from Utils import Utils
import numpy

PATTERN_DATA_SETS_PER_MAIN_TABLE = 100
PATTERNS_TABLE_MAX_COLUMNS = 7
MODELS_TABLE_MAX_COLUMNS = 6
TRAINING_TABLE_MAX_COLUMNS = 6
TESTING_TABLE_MAX_COLUMNS = 5
DEFAULT_MAX_DECIMALS = 3

BLACKLIST_PATTERNS = sorted([])
BLACKLIST_MODELS = sorted([4, 6, 7])
BLACKLIST_INPUTS = sorted([])

def getRawInterval(arrayOfDictionaries, key):
    values = map(lambda x: x[key], arrayOfDictionaries)
    mean = numpy.mean(values)
    stdev = numpy.std(values)
    return mean, stdev

def getInterval(arrayOfDictionaries, key, maxDecimals=DEFAULT_MAX_DECIMALS, decimals=None):
    mean, stdev = getRawInterval(arrayOfDictionaries, key)
    mean = numberToString(mean, maxDecimals, decimals)
    meanDecimals = max(0, mean[::-1].find('.'))
    return '$' + mean + '\\pm' + numberToString(stdev, decimals=meanDecimals) + '$'

def numberToString(number, maxDecimals=DEFAULT_MAX_DECIMALS, decimals=None):
    if decimals != None:
        return ('%.' + str(decimals) + 'f') % number

    powerOfTen = 10 ** maxDecimals
    
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
    """
    
    numberOfProperties = len(indexTable[indexTable.keys()[0]])
    propertiesDefinition = []
    i = 1;
    
    for propertyIndex in xrange(numberOfProperties):
        propertyDefinition = indexTable[indexTable.keys()[0]][propertyIndex][0]

        if not propertyDefinition.startswith('$'):
            propertiesDefinition.append('\\item [(' + str(i) + ')] ' + propertyDefinition)
            i += 1
    
    numberOfItems = len(indexTable)
    numberOfTables = len(range(0, numberOfItems, maxColumns))
    currentTableNumber = 1
    
    for i in xrange(0, numberOfItems, maxColumns):
        numberOfItemsInThisTable = min(i + maxColumns, numberOfItems) - i
        itemKeysOfThisTable = sorted(indexTable.keys())[i:i + numberOfItemsInThisTable]
        captionOfThisTable = caption if maxColumns >= numberOfItems else caption + ' (' + str(currentTableNumber) + ' of ' + str(numberOfTables) + ')'
        currentTableNumber += 1 
        
        print """
        \\begin{table}[H]
        \\centering
        %\\label{my-label}
        \\def\\arraystretch{1.5}
        %\\resizebox{\\textwidth}{!}{%
        \\begin{tabular}{c""" + ('c' * numberOfItemsInThisTable) + """}
        """
        
        for itemKey in itemKeysOfThisTable:
            print ' & ' + parseKey(itemKey),
        
        print ' \\\\ \\cline{2-' + str(numberOfItemsInThisTable + 1) + '}'
        i = 1
        
        for propertyIndex in xrange(numberOfProperties):
            propertyDefinition = indexTable[indexTable.keys()[0]][propertyIndex][0]

            if propertyDefinition.startswith('$'):
                print propertyDefinition,
            else:
                print '(' + str(i) + ')',
                i += 1
            
            for itemKey in itemKeysOfThisTable:
                print ' &', indexTable[itemKey][propertyIndex][1],
            
            if propertyIndex != numberOfProperties - 1:
                print '\\\\'
        
        print """
        \\end{tabular}
        %\\end{tabular}}
        \\caption{""" + captionOfThisTable + """}
        \\end{table}
        """

    if len(propertiesDefinition) > 0:
        print """
        \\begin{description}
        """ + '\r\n'.join(propertiesDefinition) + """
        \\end {description}
        """

def generateCrossTable(crossTable, resultKey, latexComment, caption, fontSize="footnotesize"):
    numberOfColumns = len(crossTable[crossTable.keys()[0]])

    print """
    % """ + latexComment + """

    \\begin{table}[H]
    \\centering
    %\\label{my-label}
    \\def\\arraystretch{1.5}
    %\\resizebox{\\textwidth}{!}{%
    \\""" + fontSize + """
    \\begin{tabular}{c""" + ('c' * numberOfColumns) + """}
    """

    for columnLabel in sorted(crossTable[crossTable.keys()[0]]):
        print ' &', parseKey(columnLabel),

    print '\\\\ \\cline{2-' + str(numberOfColumns + 1) + '}'

    for rowLabel in sorted(crossTable):
        print parseKey(rowLabel),

        for columnLabel in sorted(crossTable[rowLabel]):
            print ' &', crossTable[rowLabel][columnLabel][resultKey],

        print '\\\\'

    print """
    \\end{tabular}
    %\\end{tabular}}
    \\caption{""" + caption + """}
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
    #trainingAndValidationIndexTable = {}
    #testingIndexTable = {}

    for patternDataSetId, patternDataSetResults in patternDataSetResultDictionary.iteritems():
        mean = '$' + numberToString(getRawInterval(patternDataSetResults, 'patternsDistanceMean')[0] / float(patternDataSetResults[0]['patternDimension']), decimals=2) + '$'
        stdev = '$' + numberToString(getRawInterval(patternDataSetResults, 'patternsDistanceStdev')[0] / float(patternDataSetResults[0]['patternDimension']), decimals=2) + '$'

        patternDataSetIndexTable['$P_{' + str(patternDataSetId).zfill(2) + '}$'] = [
            ['$\\left|P_i\\right|$', patternDataSetResults[0]['patternDataSetSize']],
            ['$n$', patternDataSetResults[0]['patternDimension']],
            ['$\\frac{\\mu_{P_i}}{n}$', mean],
            ['$\\frac{\\sigma_{P_i}}{n}$', stdev]
            #['Mean distance $\mu_{P_i}$ between two random different patterns', getInterval(patternDataSetResults, 'patternsDistanceMean')],
            #['Standard deviation of distance $\sigma_{P_i}$ between two random different patterns', getInterval(patternDataSetResults, 'patternsDistanceStdev')],
        ]

    for modelId, modelResults in modelResultDictionary.iteritems():
        if modelResults[0]['model'] == 'hopfield':
            modelInfo = [
                ['Model', 'Hopfield'],
                ['Learning rule', modelResults[0]['trainingRule'].capitalize()],
                ['Number of hidden neurons', '\\textcolor{gray}{n/a}'],
                #['Learning rate', '\\textcolor{gray}{n/a}'],
                #['Weight decay', ''],
                #['Momentum. By Hinton\'s recommendation[CITA], the training starts with a momentum of 0.5. Once the large initial progress in the reduction of the reconstruction error has settled down to gentle progress after 5 epochs, the momentum is increased to 0.9', ''],
                ['Number of patterns per training batch', '\\textcolor{gray}{n/a}']
            ]
        else:
            modelInfo = [
                ['Model', 'RBM'],
                ['Learning rule', 'CD'],
                ['Number of hidden neurons', modelResults[0]['hiddenNeurons']],
                #['Learning rate', modelResults[0]['learningRate']],
                #['Weight decay', modelResults[0]['weightDecay']],
                #['Momentum. By Hinton\'s recommendation[CITA], the training starts with a momentum of 0.5. Once the large initial progress in the reduction of the reconstruction error has settled down to gentle progress after 5 epochs, the momentum is increased to 0.9', 'no' if not modelResults[0]['momentum'] else 'yes'],
                ['Patterns per batch', modelResults[0]['batchSize']]
            ]
    
        modelIndexTable['$M_{' + str(modelId).zfill(2) + '}$'] = modelInfo
    
    for inputDataSetId, inputDataSetResults in inputDataSetResultDictionary.iteritems():
        for i in inputDataSetResults:
            i.update({'ratioInputMinimumDistanceMean': i['inputMinimumDistanceMean'] / float(i['patternsDistanceMean'])})
        
        inputDataSetIndexTable['$I_{' + str(inputDataSetId).zfill(2) + '}$'] = [
            ['Number of generated inputs per each pattern of the pattern data set, $\\frac{\\left|I_i\\right|}{\\left|P_j\\right|}$', inputDataSetResults[0]['inputsPerPattern']],
            ['$\\frac{\\mu_{I_i}}{\\mu_{P_j}}$', getInterval(inputDataSetResults, 'ratioInputMinimumDistanceMean')]
        ]

    """
    for key, trainingAndValidationResults in trainingAndValidationResultDictionary.iteritems():
        for i in trainingAndValidationResults:
            i.update({'ratioStoredPatterns': i['successfullyStoredPatterns'] / float(i['patternDataSetSize'])})
        
        trainingInfo = [
            #['Successfully stored patterns', getInterval(trainingAndValidationResults, 'successfullyStoredPatterns')],
            #['Unsuccessfully stored patterns', getInterval(trainingAndValidationResults, 'unsuccessfullyStoredPatterns')],
            ['Number of stored patterns, proportional to $\\left|P_i\\right|$', getInterval(trainingAndValidationResults, 'ratioStoredPatterns', decimals=2)]
        ]
        
        if trainingAndValidationResults[0]['model'] == 'restricted-boltzmann':
            trainingInfo += [
                ['Training epochs', getInterval(trainingAndValidationResults, 'trainingEpochs', 0)]
            ]
        else:
            trainingInfo += [
                ['Training epochs', '\\textcolor{gray}{n/a}']                
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
            #['Mean CPU time (ms) per recall', getInterval(testingResults, 'timeMean', 1)],
            #['Standard deviation of CPU time per recall', getInterval(testingResults, 'timeStdev')]
        ]
    """

    trainingAndValidationCrossTable = {}
    testingCrossTables = {}

    for key, trainingAndValidationResults in trainingAndValidationResultDictionary.iteritems():
        for i in trainingAndValidationResults:
            i.update({'ratioStoredPatterns': i['successfullyStoredPatterns'] / float(i['patternDataSetSize'])})

        patternDataSetId, modelId = key.split(':')
        row = getObject(trainingAndValidationCrossTable, '$P_{' + patternDataSetId.zfill(2) + '}$', {})

        row['$M_{' + modelId.zfill(2) + '}$'] = {
            'ratioStoredPatterns': getInterval(trainingAndValidationResults, 'ratioStoredPatterns', decimals=2),
            'trainingEpochs': '\\textcolor{gray}{n/a}' if trainingAndValidationResults[0]['model'] == 'hopfield' else getInterval(trainingAndValidationResults, 'trainingEpochs', 0)
        }

    for key, testingResults in testingResultDictionary.iteritems():
        for i in testingResults:
            i.update({'ratioSuccessfulEquilibriums': i['successfulEquilibriums'] / float(i['inputDataSetSize'])})
        
        patternDataSetId, modelId, inputDataSetId = key.split(':')
        testingCrossTable = getObject(testingCrossTables, '$P_{' + patternDataSetId.zfill(2) + '}$', {})
        row = getObject(testingCrossTable, '$M_{' + modelId.zfill(2) + '}$', {})
        
        row['$I_{' + inputDataSetId.zfill(2) + '}$'] = {
            'ratioSuccessfulEquilibriums': getInterval(testingResults, 'ratioSuccessfulEquilibriums', decimals=3)
        }
    
    numberOfPatterns = len(patternDataSetResultDictionary)
    numberOfInputs = len(inputDataSetResultDictionary)
    numberOfModels = len(modelResultDictionary)
    
    # Generating LaTeX code of the main table.
    
    print """
    \\documentclass[12pt]{article}
    \\usepackage{float}
    \\usepackage{xcolor}
    \\usepackage{graphicx}
    \\usepackage[justification=centering]{caption}
    \usepackage[toc,page]{appendix}
    \\begin{document}
    
    \\begin{appendices}
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
    print '\\section{Annalyzed Pattern Data Sets}'
    generateIndexTable(patternDataSetIndexTable, 'PATTERN DATA SETS TABLE', 'Analyzed pattern data sets', PATTERNS_TABLE_MAX_COLUMNS)

    print '\\section{Analyzed Models}'
    generateIndexTable(modelIndexTable, 'MODELS TABLE', 'Analyzed models', MODELS_TABLE_MAX_COLUMNS)

    print '\\section{Tested Input Data Sets}'
    generateIndexTable(inputDataSetIndexTable, 'INPUT DATA SETS TABLE', 'Randomly generated and tested input data sets')

    print '\\section{Training and Validation Results}'
    #generateIndexTable(trainingAndValidationIndexTable, 'TRAININGS AND VALIDATIONS TABLE', 'Results of training model $M_i$ with pattern data set $P_j$', TRAINING_TABLE_MAX_COLUMNS)
    generateCrossTable(trainingAndValidationCrossTable, 'trainingEpochs', 'TRAINING EPOCHS TABLE', 'Number of epochs needed to train model $M_i$ with pattern data set $P_j$', "scriptsize")
    generateCrossTable(trainingAndValidationCrossTable, 'ratioStoredPatterns', 'TRAINING STORED PATTERNS TABLE', 'Number of stored patterns, proportional to $\\left|P_i\\right|$')

    print '\\section{Testing Results}'
    #generateIndexTable(testingIndexTable, 'TESTING TABLE', 'Results of testing input data set $I_i$ with model $M_j$, previously trained with pattern data set $P_k$', TESTING_TABLE_MAX_COLUMNS)

    for patternDataSetId, testingCrossTable in sorted(testingCrossTables.iteritems()):
        print '\\subsection{Testing Results for Pattern Data Set ' + parseKey(patternDataSetId) + '}'
        generateCrossTable(testingCrossTable, 'ratioSuccessfulEquilibriums', 'TESTING TABLE', 'Number of successful recalls when input data set $I_i$ is given to model $M_j$, trained with pattern data set ' + parseKey(patternDataSetId) + ', proportional to $\\left|I_i\\right|$')
    
    print """
    \\end{appendices}
    \\end{document}
    """
    