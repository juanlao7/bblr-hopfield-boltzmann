from bblr.Utils import Utils

class RestrictedBoltzmannModel(object):
    def __init__(self, properties):
        self.hiddenNeurons = properties.get('hiddenNeurons')
        self.learningRate = properties.get('learningRate')
        self.weightDecay = properties.get('weightDecay')
        self.momentum = properties.get('momentum')
        self.batchSize = properties.get('batchSize')
        
        # Validating the configuration.
        Utils.assertInt('Hidden neurons', self.hiddenNeurons, 0)    # TODO: should we do this proportional to the pattern dimension?
        Utils.assertFloat('Learning rate', self.learningRate, 0)
        Utils.assertFloat('Weight decay', self.weightDecay, 0)
        Utils.assertFloat('Momentum', self.momentum, 0)
        Utils.assertInt('Batch size', self.batchSize, 0)

    def train(self, patternDataSet):
        self.patternSize = len(patternDataSet[0])
