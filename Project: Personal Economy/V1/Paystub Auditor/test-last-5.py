import math

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

def annualPay(reg_pay_total):
    totalWeeks = 2080 # 40 hrs/week * 52 weeks
    hourly = reg_pay_total / 80 # 2 weeks 40 hour total
    annualIncome = hourly * totalWeeks 
    return annualIncome

def hourly_per_annual(annualPay):
    hourly_rate = (annualPay / 2080) 
    return hourly_rate

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

def evening_shift_earnings(quantity):
     multiple = 1
     rate = 0.70
     return calculate_pay(quantity, rate, multiple)

def night_shift_earnings(quantity):
     rate = 0.80
     multiple = 1
     time=finance_time_math(quantity)
     night = calculate_pay(time, rate, multiple)
     return cut_off(night)

def overtime_earnings(quantity,rate):
     multiple = 1.5
     time = finance_time_math(quantity)
     overtime = calculate_pay(time, rate, multiple)
     return cut_off(overtime)

def regular_earnings(quantity, rate):
     multiple = 1
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

    # test 1
    Reg_Pay_Amount = 2075.81
    Hourly_Wage = 25.947625
    Normal_TIme= 80
    OT_Time = 3.30
    OT_Pay_Amount = 136.22
    Night_Pay_Amount = 2.80
    Evening_Pay_Amount = 56.0
    Annual_Pay_Amount = global_variables("annual_salary")

    TestPassed = 0
    TestTotal = 6

    if(Annual_Pay_Amount == annualPay(Reg_Pay_Amount)):
        TestPassed = TestPassed + 1

    if(Hourly_Wage == hourly_per_annual(annualPay(Reg_Pay_Amount))):
        TestPassed = TestPassed + 1

    if(Reg_Pay_Amount == regular_earnings(Normal_TIme, hourly_per_annual(annualPay(Reg_Pay_Amount)))):
        TestPassed = TestPassed + 1
    
    if(OT_Pay_Amount == overtime_earnings(OT_Time,hourly_per_annual(annualPay(Reg_Pay_Amount)))):
        TestPassed = TestPassed + 1
    
    if(Night_Pay_Amount == night_shift_earnings(OT_Time)):
        TestPassed = TestPassed + 1

    if(Evening_Pay_Amount == evening_shift_earnings(80)):
        TestPassed = TestPassed + 1

    print(f"Test Passed {round_up(TestPassed/TestTotal) * 100}%")

if __name__ == "__main__":    main()  