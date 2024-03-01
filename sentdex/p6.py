
layer_outputs = [4.8, 1.21, 2.385]

E = 2.71828182846 # Euler's number

exp_values = []

for output in layer_outputs:
    exp_values.append(E ** output)

print()
print(exp_values)

norm_base = sum(exp_values)
norm_values = []

for value in exp_values:
    norm_values.append(value / norm_base)

print()
print(norm_values)
print()
print(sum(norm_values))