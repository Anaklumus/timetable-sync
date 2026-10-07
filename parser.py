import csv 

with open('timetable.csv', mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)