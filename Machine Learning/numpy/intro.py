'''
    Numpy   - Numerical Python
    ndarray - n-dimensional array


'''

# numpy import statement
import numpy as np

# Basic Python List Code Example # without numpy
list1 = [1,2,3,4,5]
#print(list1)
#print(list1[0]) 


# Basic Numpy Array Code Example # with numpy
np1 = np.array([0,1,2,3,4,5,6,7,8,9])
print(np1)
print(np1.shape) # shape of the array

# Range Example
np2 = np.arange(10) # 0 to 9
print(np2)

# Step Example
np3 = np.arange(0, 10, 2) # 0 to 9 with step of 2
print(np3)

# Zeros Example
np4 = np.zeros(10) # 10 zeros
print(np4)

# Multidimensional Array Example
np5 = np.zeros((3, 4)) # 3 rows and 4 columns of zeros
print(np5)

# Full Example
np6 = np.full((10), 5) # 10 fives
print(np6)

# muiltidimensional array with full
np7 = np.full((3, 4), 6) # 3 rows and 4 columns of sixes
print(np7)

# Convert Python List to Numpy Array
list2 = [1,2,3,4,5]
np8 = np.array(list2) # convert list to numpy array
print(np8)