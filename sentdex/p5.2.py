import numpy as np

np.random.seed(0)

X = [
    [1, 2, 3, 2.5],
    [2.0, 5.0, -1.0, 2.0],
    [-1.5,2.7,3.3,-0.8]
    ]

class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.rand(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

layer1 = LayerDense(4, 5)  # Adjust the number of inputs to match the dimensions of the input data
layer1.forward(X)

class ActivationReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

layer1 = LayerDense(4,5)
layer1.forward(X)
print(layer1.output)
print()

activation1 = ActivationReLU()
activation1.forward(layer1.output)
print(activation1.output)