import numpy as np

# Slicing Numpy Arrays
np1 = np.array([0,1,2,3,4,5,6,7,8,9])

# Return 2,3,4,5
np2 = np1[2:6] # 2 to 5
print(np2)

# Return from something till the end of the array?
np3 = np1[2:] # 2 to end
print(np3)

# Return Negative Slices
np4 = np1[-3:] # last 3 elements
print(np4)


# Steps
np5 = np1[0:5]
np6 = np1[0:5:2]
print(np5)
print(np6)

# Steps on the entire array
np7 = np1[::2] # every 2nd element
print(np7)


# Create a 2D numpy array
np8 = np.array([[1,2,3,4],[5,6,7,8]])

# Pull out a single item (row 1, column 2)
np9 = np8[1,2] # 7
print(np9)

# slice a 2d array
np10 = np8[0:2, 1:3] # 2nd and 3rd column of both rows
print(np10)