class Utils(object):
    @staticmethod
    def assertInt(name, value, minValue=None):
        if type(value) is not int:
            raise Exception(name + ' must be an integer')
        
        if minValue != None and value < minValue:
            raise Exception(name + ' must be equal or greater than ' + str(minValue))
        
    @staticmethod
    def assertFloat(name, value, minValue=None):
        if type(value) is not float and type(value) is not int:
            raise Exception(name + ' must be a floating-point number')
        
        if minValue != None and value < minValue:
            raise Exception(name + ' must be equal or greater than ' + str(minValue))
    