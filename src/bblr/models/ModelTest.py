import tensorflow as tf

def createModel(x, targetY):
    # Setting some constants here.
    INPUT_SIZE = x.get_shape().dims[1].__int__()
    CLASSES_SIZE = targetY.get_shape().dims[1].__int__()
    HIDDEN_LAYER_1_SIZE = 5
    HIDDEN_LAYER_2_SIZE = 3
    
    # Defining the model.
    weights1 = tf.Variable(tf.random_uniform([INPUT_SIZE, HIDDEN_LAYER_1_SIZE], -1.0, 1.0))
    biases1 = tf.Variable(tf.ones([HIDDEN_LAYER_1_SIZE]))
    
    weights2 = tf.Variable(tf.random_uniform([HIDDEN_LAYER_1_SIZE, HIDDEN_LAYER_2_SIZE], -1.0, 1.0))
    biases2 = tf.Variable(tf.ones([HIDDEN_LAYER_2_SIZE]))
    
    weights3 = tf.Variable(tf.random_uniform([HIDDEN_LAYER_2_SIZE, CLASSES_SIZE], -1.0, 1.0))
    biases3 = tf.Variable(tf.ones([CLASSES_SIZE]))
    
    hiddenLayer1 = tf.nn.relu(tf.matmul(x, weights1) + biases1)
    hiddenLayer2 = tf.nn.relu(tf.matmul(hiddenLayer1, weights2) + biases2)
    
    y = tf.nn.sigmoid(tf.matmul(hiddenLayer2, weights3) + biases3)
    
    # Defining the train step.
    error = tf.nn.l2_loss(y - targetY)
    trainStep = tf.train.GradientDescentOptimizer(0.01).minimize(error)
    
    
    # Defining the accuracy.
    success = tf.less(y - targetY, 0.1)     # We consider a success if the difference between the result and the target is less than 0.1
    accuracy = tf.reduce_mean(tf.cast(success, tf.float32))
    
    return x, targetY, trainStep, accuracy
