 # File: basicIdea.py

# 1 nuron with 4 inputs and 1 output with 1 bais
inputs = [1, 2, 3, 2.5]
weights = [0.2, 0.8, -0.5, 1.0]
bais = 2


outputs = inputs[0] * weights[0] + inputs[1] * weights[1] + inputs[2]*weights[2] + inputs[3]*weights[3] + bais
print(outputs)

# 3 nurons with 4 inputs and 3 output with 3 bais

# Still using the same inputs & wieghts from above with bais
weights2 = [0.5, -0.91, 0.26, -0.5]
weights3 = [-0.26, -0.27, 0.17, 0.87]

bais2 = 3
bais3 = 0.5