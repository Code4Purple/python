# File: 3_operators.py
# Topics: Comparison Operators, Logical Operators, Comparing Strings, F-Strings (Formatted String Literals)
# Python Version: 3.12.1

# Comparison Operators

print("\n Comparison Operators    \n")
x = 10
y = 5
print ("x =",x , "\ny =",y)
print("") # Blank Line

# Equal to
print("Is x = y  :", x == y)  # False

# Not equal to
print("Is x != y :", x != y)  # True

# Greater than
print("Is x > y  :", x > y)  # True

# Less than
print("Is x < y  :" ,x < y)  # False

# Greater than or equal to
print("Is x >= y :", x >= y)  # True

# Less than or equal to
print("Is x <= y :" , x <= y)  # False

# Logical Operators

print("\n Logical Operators \n")
x = True
y = False
print ("x =",x , "\ny =",y)
print("") # Blank Line

# Logical AND
print("Logical AND :", x and y)  # False

# Logical OR
print("Logical OR  :",x or y)  # True

# Logical NOT
print("Logical NOT :", not x)  # False
print("Logical NOT :", not y)  # True

# Comparing Strings
print("\n Comparing Strings \n")

string1 = "Hello"
string2 = "World"
#Showing Console the stored values  
print("String1 :", string1)
print("String2 :", string2)
print("") # Blank Line

# Equal to
print("Is string1 equal to string2                  :", string1 == string2)  # False

# Not equal to
print("Is string1 not equal to string2              :", string1 != string2)  # True

# Greater than
print("Is string1 greater than string2              :", string1 > string2)  # False

# Less than
print("Is string1 less than string2                 :", string1 < string2)  # True

# Greater than or equal to
print("Is string1 greater than or equal to string2  :", string1 >= string2)  # False

# Less than or equal to
print("Is string1 less than or equal to string2     :", string1 <= string2)  # True

print("") # Blank Line # Spacing the Console out to See the info better

#F-Strings (Formatted String Literals)
name = "Alice"
age = 25

# Using f-string to format the output
print(f"My name is {name} and I am {age} years old.")
