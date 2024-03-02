import numpy as np

# 3 sample data for inputs
inputs = [[1, 2, 3, 2.5],
          [2.0, 5.0, -1.0, 2.0],
          [-1.5, 2.7, 3.3, -0.8]]  # Fixed the missing comma in the third row

weights = [[0.2, 0.8, -0.5, 1.0],
           [0.5, -0.91, 0.26, -0.5],
           [-0.26, -0.27, 0.17, 0.87]]

biases = [2, 3, 0.5]

inputs = np.array(inputs)  # Convert inputs to a NumPy array
weights = np.array(weights)  # Convert weights to a NumPy array

# layer 1 
layer1Outputs = np.dot(inputs, weights.T) + biases  # Transpose weights before the dot product

# layer 2
weights2 = [[0.1, -0.14, 0.5],
            [-0.5, 0.12, -0.33],
            [-0.44, 0.73, -0.13]]

biases2 = [-1 , 2 , -0.5]

weight2 = np.array(weights2).T  # Convert weights2 to a NumPy array

layer2Outputs = np.dot(layer1Outputs, weights2) + biases2 

print(layer2Outputs)
