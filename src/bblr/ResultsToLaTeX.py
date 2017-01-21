import argparse
from Utils import Utils

PATTERN_DATA_SETS_PER_TABLE = 100

def getInterval(arrayOfDictionaries, key):
    # TODO: return "X+-Y"
    
    for element in arrayOfDictionaries:
        return element[key]

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
    
    for result in results:
        patternDataSet = schema.get(result['patternDataSetId'])
        
        if patternDataSet == None:
            patternDataSet = {}
            schema[result['patternDataSet']] = patternDataSet
        
        model = patternDataSet.get(result['modelId'])
        
        if model == None:
            model = {}
            patternDataSet[result['modelId']] = model 
        
        inputDataSet = model.get(result['inputDataSetId'])
        
        if inputDataSet == None:
            inputDataSet = []
            model[result['inputDataSetId']] = inputDataSet
        
        inputDataSet.append(result)
    
    # Creating index of items.
    patternDataSetIndex = {}
    
    for patternDataSetId in schema:
        patternDataSet = schema[patternDataSetId]
        patternDataSetResults = []
        
        for modelId in patternDataSet:
            model = patternDataSet[modelId]
            
            for inputDataSetId in model:
                inputDataSet = model[inputDataSetId]
                
                for result in inputDataSet:
                    patternDataSetResults.append(result)

        patternDataSetIndex['P' + patternDataSetId] = [
            ['Data set size', patternDataSetResults[0]['patternDataSetSize']],
            ['Pattern size', patternDataSetResults[0]['patternDimension']],
            ['Mean distance between two different patterns', getInterval(patternDataSetResults, 'patternsDistanceMean')],
            ['Standard deviation of distance between two different patterns', getInterval(patternDataSetResults, 'patternsDistanceStdev')],
        ]
