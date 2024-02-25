 # File: basicIdea.py

# 1 nuron with 4 inputs and 1 output with 1 bais
inputs = [1, 2, 3, 2.5]
weights = [0.2, 0.8, -0.5, 1.0]
bais = 2


outputs = inputs[0]*weights[0] + inputs[1]*weights[1] + inputs[2]*weights[2] + inputs[3]*weights[3] + bais
print(outputs)

# 3 nurons with 4 inputs and 3 outputs with 3 baises
# Still using the same inputs, wieghts, and bais

# inputs = [1, 2, 3, 2.5]

# weights1 = [0.2, 0.8, -0.5, 1.0]
weights2 = [0.5, -0.91, 0.26, -0.5]
weights3 = [-0.26, -0.27, 0.17, 0.87]

# bais1 = 2
bais2 = 3
bais3 = 0.5

outputs2 = [inputs[0]*weights[0] + inputs[1]*weights[1] + inputs[2]*weights[2] + inputs[3]*weights[3] + bais,
            inputs[0]*weights2[0] + inputs[1]*weights2[1] + inputs[2]*weights2[2] + inputs[3]*weights2[3] + bais2,
            inputs[0]*weights3[0] + inputs[1]*weights3[1] + inputs[2]*weights3[2] + inputs[3]*weights3[3] + bais3]

print(outputs2)

# Cleaning and Dynamic Version of the above code
# inputs = [1, 2, 3, 2.5]
weights_v2 = [[0.2, 0.8, -0.5, 1.0],
              [0.5, -0.91, 0.26, -0.5],
              [-0.26, -0.27, 0.17, 0.87]]

baises = [bais,bais2,bais3]

layer_outputs = []
for neuron_weights, neuron_bais in zip(weights_v2, baises):
    neuron_output = 0
    for n_input, weight in zip(inputs, neuron_weights):
        neuron_output += n_input*weight
    neuron_output += neuron_bais
    layer_outputs.append(neuron_output)

print(layer_outputs)