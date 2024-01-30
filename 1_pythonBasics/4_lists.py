# FIle: 4_lists.py
# Python Version: 3.12.1

# Lists
# Lists are a collection of items in a particular order.
# Lists are mutable, meaning they can be changed.
# Lists are defined by using square brackets [].
# Lists can contain any data type.

# Creating a list
print("\n----- Creating a list -----\n")
# Create a list of names
names = ["John", "Jane", "Jack", "Jill"]
print(names)

# Accessing elements in a list
print("\n----- Accessing elements in a list -----\n")
# Access the first element in the list
print(names[0])

# Access the last element in the list
print(names[-1])

# Access the second element in the list
print(names[1])

# Access the third element in the list
print(names[2])

# Access the fourth element in the list
print(names[3])

# Modifying elements in a list
print("\n----- Modifying elements in a list -----\n")
# Change the first element in the list
names[0] = "Johnathan"
print(names)

# Adding elements to a list
print("\n----- Adding elements to a list -----\n")
# Add an element to the end of the list
names.append("James")
print(names)

# Add an element to the beginning of the list
names.insert(0, "Jasmine")
print(names)

# Removing elements from a list
print("\n----- Removing elements from a list -----\n")
# Remove an element from the list
del names[0]
print(names)

# Remove an element from the list and store it in a variable
popped_name = names.pop()
print(names)
print(popped_name)

# Remove an element from the list at a specific index
names.pop(0)
print(names)

# Remove an element from the list by value
names.remove("Jack")
print(names)

# Sorting a list
print("\n----- Sorting a list -----\n")
# Sort a list in alphabetical order
names.sort()
print(names)

# Sort a list in reverse alphabetical order
names.sort(reverse=True)
print(names)

# Sort a list temporarily
print("\n----- Sort a list temporarily -----\n")
print("Here is the original list:")
print(names)

print("\nHere is the sorted list:")
print(sorted(names))

print("\nHere is the original list again:")
print(names)

# Printing a list in reverse order
print("\n----- Printing a list in reverse order -----\n")
names.reverse()
print(names)

# Finding the length of a list
print("\n----- Finding the length of a list -----\n")
print(len(names))

# Looping through a list
print("\n----- Looping through a list -----\n")
# Print each name in the list
for name in names:
    print(name)

# Print a message for each name in the list
for name in names:
    print(f"Hello {name}!")

# Print a message for each name in the list
for name in names:
    print(f"Hello {name}!")
    print(f"Welcome to the party {name}!")
print("Thank you all for coming!")

# Making a numerical list
print("\n----- Making a numerical list -----\n")
# Create a list of numbers from 1 to 10
numbers = list(range(1, 11))
print(numbers)

# Create a list of even numbers from 2 to 10
even_numbers = list(range(2, 11, 2))
print(even_numbers)

# Create a list of odd numbers from 1 to 10
odd_numbers = list(range(1, 11, 2))
print(odd_numbers)

# Create a list of squares from 1 to 10
squares = []
for number in numbers:
    squares.append(number ** 2)
print(squares)

# List comprehension
print("\n----- List comprehension -----\n")
# Create a list of squares from 1 to 10
squares = [number ** 2 for number in numbers]
print(squares)

# Slicing a list
print("\n----- Slicing a list -----\n")
# Print the first three elements in the list
print(names[0:3])

# Print the last three elements in the list
print(names[-3:])
print(names[2:])

# Copying a list
print("\n----- Copying a list -----\n")
# Copy a list
names_copy = names[:]
print(names_copy)

# In Operator
print("\n----- In Operator -----\n")
# Check if a name is in the list
print("John" in names)
print("Johnathan" in names)

# Not In Operator
print("\n----- Not In Operator -----\n")
# Check if a name is not in the list
print("John" not in names)
print("Johnathan" not in names)

# List Functions
print("\n----- List Functions -----\n")
# Find the minimum value in a list
print("The List : ", numbers)
print("Minium number of the List :" , min(numbers))
print("") # Blank Line for console readability

# Find the maximum value in a list
print("The List : ", numbers)
print("Maximum number of the List :" , max(numbers))
print("") # Blank Line for console readability

# Find the sum of all values in a list
print("The List : ", numbers)
print("Sum of all numbers of the List :" , sum(numbers))
print("") # Blank Line for console readability

# List Insert Function
print("\n----- List Insert Function -----\n")
# Insert a new element in the list
print("The List : ", numbers)
numbers.insert(2, 11)
print("The List after inserting 11 at index 2 : ", numbers)

# List Append Function
print("\n----- List Append Function -----\n")
# Append a new element in the list
print("The List : ", numbers)
numbers.append(12)
print("The List after appending 12 : ", numbers)

# List Append Function
print("\n----- List Append Function -----\n")
# Append a new element in the list
print("The List : ", numbers)
numbers.append(12)
print("The List after appending 12 : ", numbers)

# List Remove Function
print("\n----- List Remove Function -----\n")
# Remove a element in the list
print("The List : ", numbers)
numbers.remove(12)
print("The List after removing 12 : ", numbers)

# Adding Lists
print("\n----- Adding Lists -----\n")
# Add two lists
print("The List(1) : ", numbers)
print("The List(2) : ", even_numbers)
print("The List(1) + The List(2) : ", numbers + even_numbers)
print("") # Blank Line for console readability

# Multiplying Lists
print("\n----- Multiplying Lists -----\n")
# Multiply a list
print("The List : ", numbers)
print("The List * 2 : ", numbers * 2)
print("") # Blank Line for console readability

# Nested Lists
print("\n----- Nested Lists -----\n")
# Create a nested list
print("The List : ", numbers)
nested_list = [numbers, even_numbers]
print("The Nested List : ", nested_list)
print("") # Blank Line for console readability

# Tuples
print("\n----- Tuples -----\n") 
# Tuples are immutable lists
# Tuples are defined by using parentheses ()
# Tuples can contain any data type.

# Creating a tuple
print("\n----- Creating a tuple -----\n")
# Create a tuple of names
names_tuple = ("John", "Jane", "Jack", "Jill")
print(names_tuple)
print("") # Blank Line for console readability

# Accessing elements in a tuple
print("\n----- Accessing elements in a tuple -----\n")
# Access the first element in the tuple
print(names_tuple[0])
print("") # Blank Line for console readability

# Creating Empty Lists
print("\n----- Creating Empty Lists -----\n")
# Create an empty list
empty_list = []
print(empty_list)
print("") # Blank Line for console readability

# Searching Lists
print("\n----- Searching Lists -----\n")
# Search a list
print("The List : ", numbers)
print("The index of 5 in the list : ", numbers.index(5))

# Dictionaries
print("\n----- Dictionaries -----\n")
# Dictionaries are a collection of key-value pairs.
# Dictionaries are mutable, meaning they can be changed.
# Dictionaries are defined by using curly braces {}.
# Dictionaries can contain any data type.

# Creating a dictionary
print("\n----- Creating a dictionary -----\n")
# Create a dictionary of names
names_dict = {"John": 1, "Jane": 2, "Jack": 3, "Jill": 4}
print(names_dict)
print("") # Blank Line for console readability

# Accessing elements in a dictionary
print("\n----- Accessing elements in a dictionary -----\n")
# Access the first element in the dictionary
print(names_dict["John"])
print("") # Blank Line for console readability

# Modifying elements in a dictionary
print("\n----- Modifying elements in a dictionary -----\n")
# Change the first element in the dictionary
names_dict["John"] = 5
print(names_dict)
print("") # Blank Line for console readability

# Adding elements to a dictionary
print("\n----- Adding elements to a dictionary -----\n")
# Add an element to the dictionary
names_dict["James"] = 6
print(names_dict)
print("") # Blank Line for console readability

# Set list of keys
print("\n----- Set list of keys -----\n")
# Set a list of keys    
print(names_dict.keys())
print("") # Blank Line for console readability

# Set list of values
print("\n----- Set list of values -----\n")
# Set a list of values
print(names_dict.values())
print("") # Blank Line for console readability



#print() # Blank Line for console readability