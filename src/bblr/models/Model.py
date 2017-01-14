class Model(object):
    def test(self, inputDataSet, patternDataSet):
        return {
            'timeMean': 1,
            'timeStdev': 1,
            'iterationsMean': 1,
            'iterationsStdev': 1,
            'successfulEquilibriums': 1,
            'unsuccessfulEquilibriums': 1,
            'spuriousEquilibriums': 1,
            'relativeSuccessfulEquilibriums': 0.5,
            'relativeUnsuccessfulEquilibriums': 0.5
        }
