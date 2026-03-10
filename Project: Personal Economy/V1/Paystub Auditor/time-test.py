import math


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


time=finance_time_math(3.15) # should return 3.25

if time == 3.25:
    print("Test Passed Expected: 3.25 Got: {}".format(time))
else:
    print("Test Failed Expected: 3.25 Got: {}".format(time))

time=finance_time_math(3.30) # should return 3.5

if time == 3.50:
    print("Test Passed Expected: 3.5  Got: {}".format(time))
else:
    print("Test Failed Expected: 3.5  Got: {}".format(time))

time=finance_time_math(3.45) # should return 3.75

if time == 3.75:
    print("Test Passed Expected: 3.75 Got: {}".format(time))
else:
    print("Test Failed Expected: 3.75 Got: {}".format(time))