from random import random

def generateSample():
    # This is just an example generator. Feel free to edit this code to have fun.
    x = random()
    y = 1 if x < 0 else 0
    return [x], [y]         # Sample inputs and outputs must be tensors. In this case, tensors of 1 dimension.
