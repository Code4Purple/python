# File: 1_operations.py
# Topics: Arithmetic Operations, Modulus Operators, String & Using Escape Sequence, Concatenation of Strings
# Python Version: 3.12.1

# Arithmetic Operations

print("             Arithmetic Operations            ")
# Addition
x = 5
y = 3
print("Addition of          :", x," & ",y," = ", x + y)

# Subtraction 
x = 5
y = 3
print("Subtraction of       :", x," & ",y," = ", x - y)

# Multiplication
x = 5
y = 3
print("Multiplication of    :", x," & ",y," = ", x * y)

# Division
x = 12
y = 3
print("Division of          :", x," & ",y," = ", x / y)

print(" ") # Blank Line

# Modulus Operators
print(  "             Modulus Operators            ")
# Modulus
x = 12
y = 3
print("Modulus of           :", x," & ",y," = ", x % y)

# Exponentiation
x = 2
y = 3
print("Exponentiation of    :", x," & ",y," = ", x ** y)

#Square Root
x = 16
print("Square Root of       :", x," = ", x ** 0.5)

print(" ") # Blank Line

# String & Using Escape Sequence
print("             String & Using Escape Sequence            ")
# String
x = "Hello"
y = "World"
print("String               :", x," ",y)

# Escape Sequences
x = "Hello \n World"  # Newline
print("Newline          :", x)

x = "Hello \t World"  # Tab
print("Tab              :", x)

x = "Hello \b World"  # Backspace
print("Backspace        :", x)

x = "Hello \r World"  # Carriage Return
print("Carriage Return  :", x)

x = "Hello \f World"  # Form Feed
print("Form Feed        :", x)

x = "Hello \a World"  # Bell
print("Bell             :", x)

x = "Hello \\ World"  # Backslash
print("Backslash        :", x)

x = "Hello \' World"  # Single Quote
print("Single Quote     :", x)

x = "Hello \" World"  # Double Quote
print("Double Quote     :", x)

x = "Hello \ World"  # Invalid escape sequence
print("Invalid Escape   :", x)

print(" ") # Blank Line

# Concatenation of Strings
print("             Concatenation of Strings            ")

x = "Hello"
y = "World"
print("Concatenation of Strings :", x + " " + y)
