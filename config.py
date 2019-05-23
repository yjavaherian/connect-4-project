from NeuralNetwork import ValueEstimator


def init():
    global nn
    nn = ValueEstimator(3, 42, 50)
