from itertools import combinations 

def has_conflict(session1, session2):
    if session1.day != session2.day:
        return False
    return session1.start_time < session2.end_time and session2.start_time < session1.end_time

def find_conflicts(sessions):
    conflicts = []
    for s1, s2 in combinations(sessions, 2):
        if has_conflict(s1, s2):
            conflicts.append((s1, s2))
    return conflicts