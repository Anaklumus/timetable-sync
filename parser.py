from models import ClassSession

import csv 

sessions = []

with open('timetable.csv', mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        session = ClassSession(
            course=row['course'],
            day=row['day'],
            start_time=row['start_time'],
            end_time=row['end_time'],
            room=row['room']
        )
        sessions.append(session)

for s in sessions:
    print(f"{s.course} on {s.day} {s.start_time}-{s.end_time}")