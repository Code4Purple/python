import numpy as np
import nnfs
from nnfs.datasets import spiral_data

nnfs.init()

class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.rand(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

class ActivationReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

class ActivationSoftMax:
    def forward(self, inputs):
        expValues = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = expValues / np.sum(expValues, axis=1, keepdims=True)
        self.output = probabilities

X,y = spiral_data(samples=100, classes=3)

densel = LayerDense(2,3)
activation1 = ActivationReLU()
densel2 = LayerDense(3,3)
activation2 = ActivationSoftMax()

densel.forward(X)
activation1.forward(densel.output)
densel2.forward(activation1.output)
activation2.forward(densel2.output)

print(activation2.output[:5])

