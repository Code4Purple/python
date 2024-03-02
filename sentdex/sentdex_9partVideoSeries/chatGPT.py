import numpy as np

# Define array1, array2, and array3
array1 = np.array([[1, 2],
                   [3, 4]])
array2 = np.array([[5, 6],
                   [7, 8]])
array3 = np.array([9, 10, 7]).shape

# Compute the dot product of array1 and array2, then add array3
output = np.dot(array1, array2.T) + array3

print("Output Array:")
print(output)
