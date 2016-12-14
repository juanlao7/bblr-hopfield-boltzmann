import argparse
import json
import re

def loadJsonFile(path):
    with open(path) as handler:
        data = handler.read()
        data = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,data) # remove all occurance streamed comments (/*COMMENT */) from string
        data = re.sub(re.compile("//.*?\n" ) ,"" ,data)             # remove all occurance singleline comments (//COMMENT\n ) from string
        return json.loads(data)

def generatePatternDataSet(patternDataSetPropertiesCombination):
    raise 'Not implemented yet'

def generateModel(modelPropertiesCombination):
    raise 'Not implemented yet'

if __name__ == '__main__':
    # Parsing arguments
    parser = argparse.ArgumentParser(prog='bblr-hopfield-boltzmann analyzer', description='Automatic script to obtain the final results of the project bblr-hopfield-boltzmann.', epilog='*1: The format for this file is specified here: <URL>')
    parser.add_argument('model_properties_file', help='Path to a file containing the combinations of model properties you want to test (*1)')
    parser.add_argument('pattern_data_set_properties_file', help='Path to a file containing the combinations of pattern data set properties you want to test (*1)')
    arguments = parser.parse_args()
    
    # Loading preferences
    modelPropertiesCombinations = loadJsonFile(arguments.model_properties_file)
    patternDataSetPropertiesCombinations = loadJsonFile(arguments.pattern_data_set_properties_file)
    
    # Main loop
    
    for patternDataSetPropertiesCombination in patternDataSetPropertiesCombinations:
        patternDataSet = generatePatternDataSet(patternDataSetPropertiesCombination)
        
        for modelPropertiesCombination in modelPropertiesCombinations:
            model = generateModel(modelPropertiesCombination)
            model.train(patternDataSet)
            #result = model.test(inputDataSet)
            #result.add(other things such as the training cost)
            #print result
