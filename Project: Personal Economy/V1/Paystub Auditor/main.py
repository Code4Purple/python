import math



# Quantity = Hours Worked
# Type     = Hourly vs Salary
# Rate     = Hourly Rate
# Multiple = Overtime Multiplier (if applicable) Default is 1 for Regular Pay
# Amount   = Quantity * Rate * Multiple
# Time Math = minutes / 60 minutes per hour // if it equals 1 then add 1 to hours worked

def calculate_pay(quantity, rate, multiple):
    #truncated_pay = math.floor(quantity * rate * multiple)
    #return truncated_pay
    return quantity * rate * multiple

def hours(time):
    hours = int(time)
    minutes = time - hours
    if minutes >= 0.60:
        hours += 1
    return hours

def evening_shift_earnings(quantity, rate, multiple):
     return calculate_pay(quantity, rate, multiple)

def night_shift_earnings(quantity, rate, multiple):
     return calculate_pay(quantity, rate, multiple)

def overtime_earnings(quantity, rate, multiple):
     return calculate_pay(quantity, rate, multiple)

def regular_earnings(quantity, rate, multiple):
     return calculate_pay(quantity, rate, multiple)

def main():
    # Example usage
    annual_salary = 53971.06
    annual_hours = 2080 # 40 hrs/week * 52 weeks

    hours_worked = 80
    hourly_rate = annual_salary / annual_hours
    overtime_multiplier = 1.5

    regular_pay = regular_earnings(hours_worked, hourly_rate, 1)

    hours_worked = 3.30
    overtime_pay = overtime_earnings( hourly_rate, overtime_multiplier)

    
   
    print( "Over Time: Quantity: {} Rate: {} Multiple: {} Amount: {}".format(5, hourly_rate, overtime_multiplier, overtime_pay(5, hourly_rate, overtime_multiplier)))
    print("Regular Pay: Quantity: {} Rate: {} Multiple: {} Amount: {}".format(hours_worked, hourly_rate, 1, regular_pay))

if __name__ == "__main__":    main()
    


    