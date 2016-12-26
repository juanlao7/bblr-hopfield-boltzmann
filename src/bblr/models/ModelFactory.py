class ModelFactory(object):
    def __init__(self, properties):
        self.properties = properties
    
    def buildModel(self):
        modelName = self.properties.get('model')
        modelClassName = ''.join(map(lambda x: x.capitalize(), modelName.split('-'))) + 'Model'
        modelModule = __import__(modelClassName, globals(), locals())
        modelClass = getattr(modelModule, modelClassName)
        return modelClass(self.properties)
