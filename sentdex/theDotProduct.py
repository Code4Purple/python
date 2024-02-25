# FIle : theDotProduct.py
# needed packages : numpy-1.26.4

import numpy as np

# 1 nuron with 4 inputs and 1 output with 1 bais
inputs = [1, 2, 3, 2.5]
weights = [0.2, 0.8, -0.5, 1.0]
bais = 2

output = np.dot(inputs, weights) + bais
print(output)

# 3 nurons with 4 inputs and 3 outputs with 3 baises
weights_v2 = [[0.2, 0.8, -0.5, 1.0],
              [0.5, -0.91, 0.26, -0.5],
              [-0.26, -0.27, 0.17, 0.87]]
bais2 = 3
bais3 = 0.5
baises = [bais,bais2,bais3]

outputs2 = np.dot(weights_v2, inputs) + baises
print(outputs2)