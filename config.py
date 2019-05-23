from NeuralNetwork import ValueEstimator

global nn

def init():
    global nn
    nn = ValueEstimator(3, 42, 50)
