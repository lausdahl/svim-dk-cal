from __future__ import print_function

import datetime
import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
from multiprocessing import Pool


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    sync_cal_to_ics('jhpu1liovjefu5mbj5ui4uj8j4@group.calendar.google.com', 'swimming_meet_jylland.ics', creds)
    sync_cal_to_ics('ui9jr9vao6nacsckiss2ri1g50@group.calendar.google.com', 'swimming_meet.ics', creds)
    sync_cal_to_ics('cnc7r2d4qfhp0qhu5js17l91bc @ group.calendar.google.com', 'swimming_meet_odder.ics', creds)



def remove_event(v):
    event, calender_id, service=v
    print('Deleting: %s' % event['id'])
    service.events().delete(calendarId=calender_id,
                            eventId=event['id']).execute()
    return None

def sync_cal_to_ics(calender_id, ics_file_path, creds):
    try:
        service = build('calendar', 'v3', credentials=creds)
        # service.calendars().clear(calendarId='ui9jr9vao6nacsckiss2ri1g50@group.calendar.google.com').execute()

        # all_events=service.events().list(calendarId=calender_id,
        #                                    singleEvents=True,
        #                                    orderBy='startTime').execute().get('items', [])

        for event in service.events().list(calendarId=calender_id,
                                           singleEvents=True,
                                           orderBy='startTime').execute().get('items', []):
            print('Deleting: %s' % event['id'])
            service.events().delete(calendarId=calender_id,
                                    eventId=event['id']).execute()




        # pool = Pool(1)
        # print(pool.map(remove_event, [ (event,calender_id,service) for event in all_events]))
        # pool.join()

        print('inserting')
        from icalendar import Calendar, Event
        from datetime import datetime,timedelta
        from pytz import UTC  # timezone

        g = open(ics_file_path, 'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                print(component.get('summary'))
                # print(component.get('dtstart').dt)
                # print(component.get('dtend').dt)
                # print(component.get('dtstamp'))
                if datetime.strptime(str(component.get('dtstart').dt), '%Y-%m-%d').year < datetime.today().year:
                    print ('Skipping year'+str(component.get('dtstart').dt))
                    continue

                end =datetime.strptime(str(component.get('dtend').dt), '%Y-%m-%d')
                end =end + timedelta(days=1)
                service.events().insert(calendarId=calender_id,
                                        body={
                                            "summary": component.get('summary'),
                                            "description": component.get('description'),
                                            "start": {"date": str(component.get('dtstart').dt)},
                                            "end": {"date": end.strftime('%Y-%m-%d')},
                                            "location": component.get('location')}
                                        ).execute()
        g.close()

        # print('listing')
        # # Call the Calendar API
        # now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # print('Getting the upcoming 10 events')
        # events_result = service.events().list(calendarId='ui9jr9vao6nacsckiss2ri1g50@group.calendar.google.com',
        #                                       timeMin=now,
        #                                       maxResults=10, singleEvents=True,
        #                                       orderBy='startTime').execute()
        # events = events_result.get('items', [])
        #
        # if not events:
        #     print('No upcoming events found.')
        # return
        #
        # # Prints the start and name of the next 10 events
        # for event in events:
        #     start = event['start'].get('dateTime', event['start'].get('date'))
        #     print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
