# File: 2_bmiCalculator.py
# Python Version: 3.12.1

# BMI Calculator Program 
# BMI = weight(kg) / height(m) ^ 2

print("\n----- BMI Calculator Program (World Wide)-----\n")
weight = float(input("Enter your weight in kgs    : "))
height = float(input("Enter your height in meters : "))

bmi = weight / height ** 2 # ** is the exponent operator

print("Your BMI is :", bmi)

print(" ") # Blank Line for console readability

# BMI Calculator Program (US)
print("\n----- BMI Calculator Program (US)-----\n")
# Coversion for kg to lbs
weight = weight * 2.205

# Coversion for meters to inches
height = height * 39.37

# BMI = weight(lbs) * 703 / height(in) ^ 2
bmi = weight * 703 / height ** 2

print("Your weight in lbs is    :", weight)
print("Your height in inches is :", height)
print("Your BMI is              :", bmi)

print(" ") # Blank Line for console readability