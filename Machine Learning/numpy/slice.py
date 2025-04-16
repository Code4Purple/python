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

