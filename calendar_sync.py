import os.path
import datetime 
import hashlib 

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError 

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


DAYS = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
    "Friday": 4, "Saturday": 5, "Sunday": 6,
}


def first_occurrence(start_date, day_name):
    """First date on or after start_date that falls on day_name."""
    offset = (DAYS[day_name] - start_date.weekday()) % 7
    return start_date + datetime.timedelta(days=offset)


def make_event_id(session):
    key = f"{session.course}|{session.day}|{session.start_time}|{session.end_time}"
    return hashlib.sha1(key.encode()).hexdigest()


def create_recurring_event(service, session, first_date, until_date):
    first_class = first_occurrence(first_date, session.day).isoformat()
    until = until_date.strftime("%Y%m%d") + "T235959Z"

    event = {
        "summary": session.course,
        "location": session.room,
        "id": make_event_id(session),
        "start": {
            "dateTime": f"{first_class}T{session.start_time}:00",
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": f"{first_class}T{session.end_time}:00",
            "timeZone": "Asia/Kolkata",
        },
        "recurrence": [f"RRULE:FREQ=WEEKLY;UNTIL={until}"],
    }
    try:
        return service.events().insert(calendarId="primary", body=event).execute()
    except HttpError as error:
        if error.resp.status == 409:
            return None
        raise


if __name__ == "__main__":
    from parser import sessions

    service = get_service()
    start = datetime.date(2026, 10, 12)
    end = datetime.date(2026, 11, 20)

    for session in sessions:
        created = create_recurring_event(service, session, start, end)
        if created is None:
            print(f"Skipped (already exists): {session.course} {session.day}")
        else:
            print(f"Created: {session.course} {session.day}")