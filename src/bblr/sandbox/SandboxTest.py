from bblr.generators.GeneratorTest import generateSample
from bblr.models.ModelTest import createModel

import tensorflow as tf
import numpy as np

def generateDataset(n):
    xs = []
    ys = []
    
    for i in xrange(n):
        x, y = generateSample()         # See GeneratorTest.py
        xs.append(x)
        ys.append(y)
    
    return xs, ys

# Setting some constants here.
INPUT_SIZE = 1
CLASSES_SIZE = 1

# Defining the model.
x = tf.placeholder(tf.float32, [None, INPUT_SIZE])
targetY = tf.placeholder(tf.float32, [None, CLASSES_SIZE])

# Create the datasets
trainingXs, trainingYs = generateDataset(100)
validationXs, validationYs = generateDataset(30)
testingXs, testingYs = generateDataset(30)

# Creating the model.
trainStep, accuracy = createModel()     # See ModelTest.py

# Initialize the variables.
init = tf.initialize_all_variables()

# Launch the graph.
session = tf.Session()
session.run(init)

bestAccuracy = None     # This is an array where [0] = training accuracy and [1] = validation accuracy.

for i in xrange(200):
    session.run(trainStep, feed_dict = {x: trainingXs, targetY: trainingYs})

    if i % 10 == 0:
        currentTrainingAccuracy = session.run(accuracy, feed_dict = {x: trainingXs, targetY: trainingYs})
        currentValidationAccuracy = session.run(accuracy, feed_dict = {x: validationXs, targetY: validationYs})

        if bestAccuracy == None or currentValidationAccuracy >= bestAccuracy[1]:
            # TODO: store the state of the network NOW.
            bestAccuracy = [currentTrainingAccuracy, currentValidationAccuracy]

        print 'Training step', i, '| Training accuracy', currentTrainingAccuracy, '| Validation accuracy', currentValidationAccuracy

print 'Best training accuracy:', bestAccuracy[0]
print 'Best validation accuracy:', bestAccuracy[1]

# TODO: load the state of the best network here and uncomment the following line.
# print 'Testing accuracy: ', session.run(accuracy, feed_dict = {x: testingXs, targetY: testingYs})
