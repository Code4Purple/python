import math



# Quantity = Hours Worked
# Type     = Hourly vs Salary
# Rate     = Hourly Rate
# Multiple = Overtime Multiplier (if applicable) Default is 1 for Regular Pay
# Amount   = Quantity * Rate * Multiple
# Time Math = minutes / 60 minutes per hour // if it equals 1 then add 1 to hours worked

def global_variables(option):
    # Golbal Variables For Pay Calculations
    if option == "annual_salary":
        return 53971.06
    elif option == "annual_hours":
        return 2080 # 40 hrs/week * 52 weeks
    elif option == "type":
        return "Hours"

def cut_off (value):
    value *= 100
    value = math.floor(value)
    value /= 100
    return value

def round_up(n, decimals=0):
    multiplier = 10**decimals
    return math.ceil(n * multiplier) / multiplier


def finance_time_math(time):
    hours = int(time)
    #print("Hours: {}".format(hours))
    minutes = (time - hours)
    #print("Minutes: {}".format(minutes))
    #print(round_up(minutes, 2))
    if minutes >= 0.6:
        hours += 1
        minutes = 0
    
    total_time = hours + ((minutes * 100 ) / 60)
    return round_up(total_time, 2)

def calculate_pay(quantity, rate, multiple):
    #truncated_pay = math.floor(quantity * rate * multiple)
    #return truncated_pay
    return quantity * rate * multiple

def evening_shift_earnings(quantity, rate, multiple):
     return calculate_pay(quantity, rate, multiple)

def night_shift_earnings(quantity, rate, multiple):
     time=finance_time_math(quantity)
     night = calculate_pay(time, rate, multiple)
     return cut_off(night)

def overtime_earnings(quantity, rate, multiple):
     time = finance_time_math(quantity)
     overtime = calculate_pay(time, rate, multiple)
     return cut_off(overtime)

def regular_earnings(quantity, rate, multiple):
     return calculate_pay(quantity, rate, multiple)

def Gross_Earnings(regular_pay, night_shift_pay, overtime_pay,evening_pay):
    return regular_pay + night_shift_pay + overtime_pay + evening_pay

def Pretax_Deductions(medical, vision):
    return medical + vision
    
def Employee_Tax_Deductions_Percentage(Gross_Earnings, Pretax_Deductions, Employee_Tax_Statement):
    tax_percentage = (Gross_Earnings - Pretax_Deductions) / Employee_Tax_Statement
    return tax_percentage

def Net_Pay(Gross_Earnings, Pretax_Deductions, tax):
    return Gross_Earnings - Pretax_Deductions - tax
    

def main():

    hourly_rate = global_variables("annual_salary") / global_variables("annual_hours")
    
    regular_pay = regular_earnings(80.0, hourly_rate,1)
    overtime_pay = overtime_earnings(3.30, hourly_rate, 1.5)
    night_shift_pay = night_shift_earnings(3.30, 0.80, 1)
    evening_pay = evening_shift_earnings(80.00, 0.70, 1)
    Gross_Income = Gross_Earnings(regular_pay, night_shift_pay, overtime_pay, evening_pay)
    Pretax = Pretax_Deductions(108.46, 2.03)
    Tax = Employee_Tax_Deductions_Percentage(Gross_Income, Pretax, 340.66)
    Net=Net_Pay(Gross_Income, Pretax, 340.66)

    if(hourly_rate == 25.947625):
        print("Test Passed Expected: 25.947625 Got: {}".format(hourly_rate))
    else:
        print("Test Failed Expected: 25.947625 Got: {}".format(hourly_rate))

    if(regular_pay == 2075.81):
        print("Test Passed Expected: 2075.81 Got: {}".format(regular_pay))
    else:
        print("Test Failed Expected: 2075.81 Got: {}".format(regular_pay))

    if(overtime_pay == 136.22): 
        print("Test Passed Expected: 136.22 Got: {}".format(overtime_pay))
    else:
        print("Test Failed Expected: 136.22 Got: {}".format(overtime_pay))

    if(night_shift_pay == 2.80):
        print("Test Passed Expected: 2.80 Got: {}".format(night_shift_pay))
    else:
        print("Test Failed Expected: 2.80 Got: {}".format(night_shift_pay))

    if(evening_pay == 56.00):       
        print("Test Passed Expected: 56.00 Got: {}".format(evening_pay))
    else:
        print("Test Failed Expected: 56.00 Got: {}".format(evening_pay))

    if(Gross_Income == 2270.83):
        print("Test Passed Expected: 2270.83 Got: {}".format(Gross_Income))
    else:
        print("Test Failed Expected: 2270.83 Got: {}".format(Gross_Income))
    
    if(Pretax == 110.49):
        print("Test Passed Expected: 110.49 Got: {}".format(Pretax))
    else:
        print("Test Failed Expected: 110.49 Got: {}".format(Pretax))

    if(Tax == 6.341630951682029):
        print("Test Passed Expected: 6.341630951682029 Got: {}".format(Tax))
    else:
        print("Test Failed Expected: 6.341630951682029 Got: {}".format(Tax))

    if(Net == 1819.68):
        print("Test Passed Expected: 1819.68 Got: {}".format(Net))
    else:
        print("Test Failed Expected: 1819.68 Got: {}".format(Net))

if __name__ == "__main__":    main()   
 