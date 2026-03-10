import math



# Quantity = Hours Worked
# Type     = Hourly vs Salary
# Rate     = Hourly Rate
# Multiple = Overtime Multiplier (if applicable) Default is 1 for Regular Pay
# Amount   = Quantity * Rate * Multiple
# Time Math = minutes / 60 minutes per hour // if it equals 1 then add 1 to hours worked

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
     return calculate_pay(time, rate, multiple)

def overtime_earnings(quantity, rate, multiple):
     time = finance_time_math(quantity)
     return calculate_pay(time, rate, multiple)

def regular_earnings(quantity, rate, multiple):
     return calculate_pay(quantity, rate, multiple)

def main():
    # Golbal Variables For Pay Calculations
    annual_salary = 53971.06
    annual_hours = 2080 # 40 hrs/week * 52 weeks

    # Regular Pay Calculation
    hours_worked = 80
    hourly_rate = annual_salary / annual_hours
    regular_pay = regular_earnings(hours_worked, hourly_rate, 1)

    # Overtime Pay Calculation
    overtime_multiplier = 1.5
    overtime_rate = hourly_rate
    overtime_quantity = 3.30
    overtime_pay = cut_off(overtime_earnings(overtime_quantity, overtime_rate, overtime_multiplier))

    # Night Shift Pay Calculation
    night_shift_rate = 0.80
    night_shift_quantity = 3.30
    night_shift_multiplier = 1
    night_shift_pay = cut_off(night_shift_earnings(night_shift_quantity, night_shift_rate, night_shift_multiplier))

    # Evening Shift Pay Calculation
    evening_shift_rate = 0.70
    evening_shift_quantity = hours_worked
    evening_shift_multiplier = 1
    evening_shift_pay = cut_off(evening_shift_earnings(evening_shift_quantity, evening_shift_rate, evening_shift_multiplier))

    print("Evening Shift Earnings: Quantity: {}  Rate: {}   Multiple: {}   Amount: {}".format(finance_time_math(evening_shift_quantity), round_up(evening_shift_rate, 2), evening_shift_multiplier, evening_shift_pay))
    print("Night Shift Earnings  : Quantity: {}  Rate: {}    Multiple: {}   Amount: {}".format(finance_time_math(night_shift_quantity), round_up(night_shift_rate, 2), night_shift_multiplier, night_shift_pay))
    print("Overtime Earnings     : Quantity: {}  Rate: {}  Multiple: {} Amount: {}".format(finance_time_math(overtime_quantity), round_up(hourly_rate, 2), overtime_multiplier, overtime_pay))
    print("Regular Pay           : Quantity: {}  Rate: {}  Multiple: {}   Amount: {}".format(hours_worked, round_up(hourly_rate, 2), 1, regular_pay))

if __name__ == "__main__":    main()
    


    