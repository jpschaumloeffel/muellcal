from datetime import datetime, timedelta
from icalendar import Calendar, Event

year = 2023
bezirk = "3A1"

local_tzinfo = datetime.now().astimezone().tzinfo

calendar_data = {
    'Restmüll': "4 18 1 15 1 15 29 13 26 10 24 7 21 5 19 2 16 30 13 27 11 25 8 22 6 20",
    'Gelber Sack': "4 1 1 29 26 24 21 19 16 13 11 8 6",
    'Papiertonne': "25 23 22 19 17 14 12 9 6 5 2 29 28",
    'Biotonne': "11 25 8 23 8 22 5 19 4 17 1 14 28 12 26 9 23 6 20 5 18 2 15 29 13 28",
}


def generate_ics():
    cal = Calendar()

    for calname, days in calendar_data.items():
        parsed_days = [int(x) for x in days.split(" ")]

        dates = []

        month = 1
        last_day = None
        for day in parsed_days:
            if last_day is not None and last_day >= day:
                month += 1
            dates.append(datetime(year, month, day, tzinfo=local_tzinfo).date())
            last_day = day

        for d in dates:
            event = Event()
            event['uid'] = f'muellkalender2023-{calname.encode("ascii", errors="ignore").decode()}-{d.year}{d.month}{d.day}'
            event.add('summary', calname)
            event.add('description', f"Bezirk {bezirk}")
            event.add('dtstart', d)
            event.add('dtend', d + timedelta(days=1))
            cal.add_component(event)

    return cal.to_ical()


if __name__ == '__main__':
    with open(f"muellcal_{year}.ics", "wb") as f:
        f.write(generate_ics())
