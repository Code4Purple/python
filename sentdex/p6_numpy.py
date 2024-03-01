import numpy as np

layer_outputs = [4.8, 1.21, 2.385]

E = 2.71828182846 # Euler's number

exp_values = np.exp(layer_outputs)
norm_values = exp_values / np.sum(exp_values)

print("Numpy Version of SoftMax")
print(norm_values)
print(sum(norm_values))
print()

# The numpy version is much more concise and easier to read.
# input -> exponentiation -> normalization -> output
# also called : input -> softmax -> output

# Batch Version of this code    
print("Batch Version of SoftMax")
layer_outputs2 = [[4.8, 1.21, 2.385],
                  [8.9, -1.81, 0.2],
                  [1.41, 1.051, 0.026]]

exp_values2 = np.exp(layer_outputs2)
print(exp_values2)
print()
norm_values2 = exp_values2 / np.sum(exp_values2, axis=1, keepdims=True)
print(norm_values2)