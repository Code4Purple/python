# File: 1_interestCalculator.py
# Python Version: 3.12.1


# Interest Calculator Program
print("\n----- Interest Calculator Program -----\n")

principal = float(input("Enter the principal amount : "))
years = int(input("Enter the number of years : "))
rate = float(input("Enter the rate of interest : "))
interest = principal * years * rate / 100

print("Interest Amount = ", interest)
print("Total Amount = ", principal + interest)

print(f"The interest amount is {interest} for {years} years and the total amount is {principal + interest}.")


print(" ") # Blank Line for console readability

