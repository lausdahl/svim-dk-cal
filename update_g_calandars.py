from __future__ import print_function

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from icalendar import Calendar
import json

from google.oauth2 import service_account


def main():
    with open('rosy-spring-359619-475b02205702.json') as source:
        info = json.load(source)

    creds = service_account.Credentials.from_service_account_info(info)

    sync_cal_to_ics('cnc7r2d4qfhp0qhu5js17l91bc@group.calendar.google.com', 'swimming_meet_odder.ics', creds,
                    full_refresh=False)
    sync_cal_to_ics('jhpu1liovjefu5mbj5ui4uj8j4@group.calendar.google.com', 'swimming_meet_jylland.ics', creds,
                    full_refresh=False)
    sync_cal_to_ics('ui9jr9vao6nacsckiss2ri1g50@group.calendar.google.com', 'swimming_meet.ics', creds,
                    full_refresh=False)


def sync_cal_to_ics(calender_id, ics_file_path, creds, full_refresh=False):
    try:
        print("Updating cal: '%s' source: '%s'" % (calender_id, ics_file_path))
        service = build('calendar', 'v3', credentials=creds)

        cal_overview=service.calendars().get(calendarId=calender_id).execute()
        print("Updating cal: '%s' source: '%s'" % (cal_overview['summary'], ics_file_path))

        cal_event_mapping = generate_inserts(ics_file_path)

        up_to_date_cal_events = []

        def process_events(events):
            for event in events:

                if full_refresh:
                    print("Event '%s' - '%s' - '%s' -- deleting" % (event['id'], event['summary'], event['start']))
                    service.events().delete(calendarId=calender_id, eventId=event['id']).execute()
                else:
                    if 'start' in event and 'date' in event['start'] and datetime.strptime(event['start']['date'],
                                                                                           '%Y-%m-%d') > datetime.today() - timedelta(
                        days=31 * 3):

                        if cal_event_hash(event) in cal_event_mapping:
                            # print('Up to date -- skipping')
                            up_to_date_cal_events.append(cal_event_hash(event))
                        else:
                            print("Event changed '%s' -- deleting" % event['id'])
                            service.events().delete(calendarId=calender_id, eventId=event['id']).execute()

        ret = service.events().list(calendarId=calender_id,
                                    singleEvents=True,
                                    orderBy='startTime').execute()

        process_events(ret.get('items', []))
        while 'nextPageToken' in ret:
            print("Additional pages, fetching next")
            ret = service.events().list(calendarId=calender_id,
                                        singleEvents=True,
                                        orderBy='startTime',
                                        pageToken=ret['nextPageToken']).execute()
            process_events(ret.get('items', []))

        for k, event in cal_event_mapping.items():
            if k in up_to_date_cal_events:
                continue

            try:
                print("Event '%s' -- inserting" % event['summary'])
                service.events().insert(calendarId=calender_id,
                                        body=event).execute()
            except HttpError as e:
                print(e)
                print(event)
    except HttpError as error:
        print('An error occurred: %s' % error)


def generate_inserts(ics_file_path):
    cal_event_mapping = dict()

    g = open(ics_file_path, 'rb')
    gcal = Calendar.from_ical(g.read())
    for component in gcal.walk():
        if component.name == "VEVENT":
            if datetime.strptime(str(component.get('dtstart').dt), '%Y-%m-%d').year < datetime.today().year:
                print('Skipping year' + str(component.get('dtstart').dt))
                continue

            end = datetime.strptime(str(component.get('dtend').dt), '%Y-%m-%d')
            end = end + timedelta(days=1)

            body = {
                "summary": component.get('summary'),
                "description": component.get('description'),
                "start": {"date": str(component.get('dtstart').dt)},
                "end": {"date": end.strftime('%Y-%m-%d')},
                "location": component.get('location')}

            cal_event_mapping.update({cal_event_hash(body): body})
    g.close()
    return cal_event_mapping


def cal_event_hash(body):
    keys = ['start', 'end', 'location', 'description', 'summary']
    return hash("".join([str(body[k]) for k in keys]))


if __name__ == '__main__':
    main()
