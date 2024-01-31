# File : 5_conditionals.py
# Python Version: 3.12.1

# Conditionals

# Conditionals are used to check conditions and take actions based on the result.
name = "John"
age = 20

# if-else statements
print("\n----- if-else statements -----\n")
# if-else statements are used to check conditions and take actions based on the result.

for x in range(2): # For loop to run the code twice
    print("Making a decision based on a condition with this data:")
    print(f"Name: {name}")
    print(f"Age: {age}")

    print("\nIs the name John?")
    if name == "John":
        print(" Yes: Hello John!")
    else:
        print(" No: Hello Stranger!")

    print("\nIs the age 20?")
    if age == 20:
        print(" Yes: You are 20 years old!")
    else:    
        print(" No: You are not 20 years old!")

    name = "Jane"
    age = 21
    print("") # Print a new line for console readability

# Range of numbers
numbers = list(range(1, 11))
print(f"----- Making a list of numbers through the range of numbers ----- \n\nRange from 1 to 10 : {numbers}")

# for loop with a defined range already
print("\n----- for loop with a defined range already -----\n")
# Print each number in the list
for number in numbers:
    print(number)

# For loop through Dictionary
print("\n----- For loop through Dictionary -----\n")
# Create a dictionary
people =  {"John": 20, "Jane": 21, "Bob": 20, "Alice": 20}
for x in people:
    print(f"{x} is {people[x]} years old.")

# While Loop
print("\n----- While Loop -----\n")
loopCounter = 0
while loopCounter < 5:
    print(f"Loop Counter: {loopCounter}")
    loopCounter += 1

# Break and Continue
print("\n----- Break and Continue -----\n")
# Break
print("\n----- Break (Stops Data) -----\n")
# Print each number in the list
print("The data within the List : ", numbers)
for number in numbers:
    if number == 5:
        print("Stopping the loop at number 5")
        break
    print(number)

# Continue
print("\n----- Continue (Skips Data) -----\n")
# Print each number in the list
print("The data within the List : ", numbers)
for number in numbers:
    if number == 5:
        print("Skipping the number 5")
        continue
    print(number)

# Adding Data to a List with a Loop
print("\n----- Adding Data to a List with a Loop -----\n")
# Create a list of numbers from 1 to 10
numbers2 = []
print("The data within the list before the loop : ", numbers2)
print("Creating a list 1 to 20\n")
for number in range(1, 21):
    numbers2.append(number)
    print(f"Creating a data point for the list : {number}")

print("\nThe data within the list after the loop : ", numbers2)

print("") # Print a new line for console readability

# Using User Input as a way to put data into a list
print("\n----- Using User Input as a way to put data into a list -----\n")
# empty list
userInput = []
print("The data within the list before user data: ", userInput)
input = input("Enter a subject matter: ")
userInput.append(input)
print("The data within the list after user data: ", userInput)

# Creating a list of products
print("\n----- Creating a list of products -----\n")
# Emty list
products = []
print("The data within the list before the loop : ", products)
print("Creating a list of products")
print("")
# Loop to add products to the list
while True:
    products.append({"name": "Smartphone", "price": 1000, "description": "A device that can make calls and send messages."})
    products.append({"name": "Laptop", "price": 1500, "description": "A device that can be used to work on the go."})
    products.append({"name": "Tablet", "price": 800, "description": "A device that can be used to watch movies and play games."})
    print("The data within the list after the loop : \n", products)
    break

print("\n------ Products List Created -----\n")
for products in products:
    print(f"Product Name: {products['name']} ${products['price']}")
    print(f"Product Description: {products['description']}")
    print("")

print("") # Print a new line for console readability
