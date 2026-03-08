import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import numpy as np

# 1. Generate data using NumPy
# Create an array of 100 equally spaced numbers between 0 and 2*pi
x = np.linspace(0, 2 * np.pi, 100)
# Calculate the sine of each value in x
y = np.sin(x)

# 2. Create the plot using Matplotlib's pyplot module
plt.figure(figsize=(8, 5)) # Optional: adjusts figure size
plt.plot(x, y, color='blue', linestyle='-') # Plot the data

# 3. Add labels and a title for clarity
plt.title("Sine Wave using Matplotlib and NumPy")
plt.xlabel("X values (radians)")
plt.ylabel("Sine of X")
plt.grid(True) # Optional: adds a grid for better readability

# 4. Display the plot
plt.show()
