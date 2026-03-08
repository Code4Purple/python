## Complete Neural Network Example

import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        """
        Initialize the neural network
        """
        # Initialize weights with small random values
        self.W1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros((1, hidden_size))
        
        self.W2 = np.random.randn(hidden_size, output_size) * 0.1
        self.b2 = np.zeros((1, output_size))
        
        print("Network initialized!")
        print(f"Input → Hidden weights shape: {self.W1.shape}")
        print(f"Hidden → Output weights shape: {self.W2.shape}")
    
    def relu(self, x):
        """ReLU activation function"""
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        """Derivative of ReLU for backpropagation"""
        return (x > 0).astype(float)
    
    def forward(self, X):
        """
        Forward propagation
        """
        # Store input for backpropagation
        self.X = X
        
        # Input → Hidden layer
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        print(f"\nForward pass:")
        print(f"Input shape: {X.shape}")
        print(f"z1 (before ReLU): {self.z1[0]}")
        print(f"a1 (after ReLU): {self.a1[0]}")
        
        # Hidden → Output layer
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.z2  # Linear output for regression
        print(f"z2 (output): {self.z2[0]}")
        
        return self.a2
    
    def mean_squared_error(self, predictions, targets):
        """Calculate MSE loss"""
        return np.mean((predictions - targets) ** 2)
    
    def backward(self, y, learning_rate=0.01):
        """
        Backward propagation
        """
        m = self.X.shape[0]  # number of samples
        
        print(f"\nBackward pass:")
        print(f"Target: {y[0][0]:.2f}, Prediction: {self.a2[0][0]:.2f}")
        
        # Output layer gradients
        dZ2 = self.a2 - y  # Derivative of MSE
        dW2 = np.dot(self.a1.T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m
        
        print(f"dW2 (gradient): {dW2.flatten()}")
        
        # Hidden layer gradients
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * self.relu_derivative(self.z1)
        dW1 = np.dot(self.X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m
        
        # Update weights and biases
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        
        print("Weights updated!")
    
    def train(self, X, y, epochs=1000, learning_rate=0.01):
        """
        Train the neural network
        """
        losses = []
        
        print("Starting training...")
        for epoch in range(epochs):
            # Forward pass
            predictions = self.forward(X)
            
            # Calculate loss
            loss = self.mean_squared_error(predictions, y)
            losses.append(loss)
            
            # Backward pass
            self.backward(y, learning_rate)
            
            # Print progress
            if epoch % 200 == 0:
                print(f"Epoch {epoch}, Loss: {loss:.6f}")
        
        return losses

# Create sample data: predict house prices
# Features: [size (sq ft), bedrooms]
X = np.array([
    [1000, 2],
    [1500, 3],
    [2000, 3],
    [2500, 4],
    [3000, 4],
    [3500, 5]
], dtype=float)

# Target: house prices (in thousands)
y = np.array([
    [200],
    [300],
    [400],
    [500],
    [600],
    [700]
], dtype=float)

# Normalize the data (important for training)
X_normalized = (X - np.mean(X, axis=0)) / np.std(X, axis=0)
y_normalized = (y - np.mean(y)) / np.std(y)

print("Data shapes:")
print(f"X shape: {X_normalized.shape}")
print(f"y shape: {y_normalized.shape}")
print(f"Sample data point: {X_normalized[0]}, target: {y_normalized[0]}")

# Create and train the network
print("\n" + "="*50)
nn = NeuralNetwork(input_size=2, hidden_size=4, output_size=1)

# Train the network
losses = nn.train(X_normalized, y_normalized, epochs=1000, learning_rate=0.1)

# Test the network
print("\n" + "="*50)
print("Testing the trained network:")
test_input = X_normalized[0:1]  # First sample
prediction = nn.forward(test_input)
print(f"Input: {X[0]} (original scale)")
print(f"Normalized input: {test_input[0]}")
print(f"Prediction (normalized): {prediction[0][0]:.4f}")
print(f"Actual (normalized): {y_normalized[0][0]:.4f}")

# Plot training progress
plt.figure(figsize=(10, 6))
plt.plot(losses)
plt.title('Training Loss Over Time')
plt.xlabel('Epoch')
plt.ylabel('Mean Squared Error')
plt.grid(True)
plt.show()

# Test on new data
print("\nTesting on new data:")
new_houses = np.array([
    [1200, 2],  # Should predict around 240k
    [2800, 4]   # Should predict around 560k
], dtype=float)

# Normalize new data using same parameters
new_houses_normalized = (new_houses - np.mean(X, axis=0)) / np.std(X, axis=0)

for i, house in enumerate(new_houses_normalized):
    pred = nn.forward(house.reshape(1, -1))
    print(f"House {i+1}: {new_houses[i]} sq ft, {int(new_houses[i][1])} bedrooms")
    print(f"  Predicted price (normalized): {pred[0][0]:.4f}")

'''
## Step-by-Step Breakdown:

### 1. **Data Preparation**
- House features: size and bedrooms
- Target: house prices
- Normalization to help training

### 2. **Network Architecture**
- Input: 2 features (size, bedrooms)
- Hidden: 4 neurons with ReLU activation
- Output: 1 neuron (price prediction)

### 3. **Forward Pass**
```
Input → Linear → ReLU → Linear → Output
```

### 4. **Training Process**
- Forward pass: make prediction
- Calculate loss: MSE between prediction and actual
- Backward pass: calculate gradients
- Update weights: move in direction that reduces loss

### 5. **Key Concepts Demonstrated**
- **Matrix operations** with NumPy
- **ReLU activation** and its derivative
- **Gradient descent** optimization
- **Batch processing** (multiple samples at once)

'''
