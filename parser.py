import csv

from models import ClassSession


def load_sessions(path):
    sessions = []
    with open(path, mode="r", newline="") as file:
        for row in csv.DictReader(file):
            sessions.append(ClassSession(
                course=row["course"],
                day=row["day"],
                start_time=row["start_time"],
                end_time=row["end_time"],
                room=row["room"],
            ))
    return sessions