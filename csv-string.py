# csv string
import names
import random
from datetime import timedelta, datetime

def random_date(start, end):
    '''
    reference: https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    '''
    delta = end - start
    int_delta = (delta.days*24*60*60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)
    
employee_info = [] #EID, FirstName, LastName, username, password

for i in range(1, 101):
    fname = names.get_first_name()
    lname = names.get_last_name()
    employee_info.append([
        "{0:0=4d}".format(i),
        fname,
        lname,
        (fname+lname).lower(),
        fname[0:2] + str(i) + lname[0:2] + "!"
    ])
    #print(employee_info[i-1])
    
#print(employee_info[99])

payroll = [] #EID, contract_type(hour, month), hour_count, unit_pay, total_pay
for i in employee_info:
    hour_count = random.randrange(130, 181)
    if hour_count <= 150:
        hour_count = random.randrange(50, 80)
        contract_type = "hour"
        unit_pay = random.randrange(17, 27, 3)
        total_pay = hour_count*unit_pay
    else:
        contract_type = "month"
        unit_pay = random.randrange(1500, 3300, 150)
        total_pay = unit_pay
    payroll.append([
        i[0],
        contract_type,
        hour_count,
        unit_pay,
        total_pay
    ])
#print(payroll)

schedule = [] # EID, mon, tue, wed, thu, fri, sat, sun (boolean to indicate yes or no)
week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
day_count = 0
for i in payroll:
    data = [i[0], False, False, False, False, False, False, False]
    if contract_type == "hour":
        day_count = random.randrange(3, 6) #find total day that the employee has to work in one week
    elif contract_type == "month":
        day_count = 5
    working = random.sample(week, day_count) #find the days that employee has too work in a week
    #for i in working:
    if "mon" in working:
        data[1] = True
    if "tue" in working:
        data[2] = True
    if "wed" in working:
        data[3] = True
    if "thu" in working:
        data[4] = True  
    if "fri" in working:
        data[5] = True
    if "sat" in working:
        data[6] = True
    if "sun" in working:
        data[7] = True 
    #print(data)
    schedule.append(data)
#print(schedule)
            


training = [] # EID, training_name(basic operation, human resource, database management), completion_date
d1 = datetime.strptime('18/9/2012 1:30 PM', '%d/%m/%Y %I:%M %p')
d2 = datetime.strptime('14/9/2023 4:50 AM', '%d/%m/%Y %I:%M %p')
#print(random_date(d1, d2))
for i in employee_info:
    training_name = random.randrange(1, 4)
    if training_name == 1:
        training_name = "Basic Operation"
    elif training_name == 2:
        training_name = "Human Resources"
    elif training_name == 3:
        training_name = "Database Management"
    completion_date = random_date(d1, d2)
    #print(completion_date)
    training.append([
        i[0],
        training_name,
        completion_date
    ])
#print(training)

'''
string.lower()
https://www.programiz.com/python-programming/methods/string/lower

string format - convert number into x digits string eg 5 -> 05
https://stackoverflow.com/questions/3505831/in-python-how-do-i-convert-a-single-digit-number-into-a-double-digits-string

string format official documentation
https://docs.python.org/3/library/string.html#string-formatting

name module
https://pypi.org/project/names/


random functions to generate integers
https://pynative.com/python-random-randrange/

datetime random
https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates

csv reference
https://www.scaler.com/topics/how-to-create-a-csv-file-in-python/

random sampling
https://note.nkmk.me/en/python-random-choice-sample-choices/
'''