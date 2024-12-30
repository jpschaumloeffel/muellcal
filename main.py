from datetime import datetime, timedelta

from icalendar import Calendar, Event

year = 2025
bezirk = "3A1"

local_tzinfo = datetime.now().astimezone().tzinfo

# this is a really lazy way to input repeating events
# - just list the days component of all events
# - separate events in different months by commas
# - make sure to have 12 months max
calendar_data_2023 = {
    'Restmüll': "4 18, 1 15, 1 15 29, 13 26, 10 24, 7 21, 5 19, 2 16 30, 13 27, 11 25, 8 22, 6 20",
    'Gelber Sack': "4, 1, 1 29, 26, 24, 21, 19, 16, 13, 11, 8, 6",
    'Papiertonne': "25, 23, 22, 19, 17, 14, 12, 9, 6, 5, 2 29, 28",
    'Biotonne': "11 25, 8 23, 8 22, 5 19, 4 17, 1 14 28, 12 26, 9 23, 6 20, 5 18, 2 15 29, 13 28",
}

calendar_data_2024 = {
    'Restmüll': "4 17 31, 15 28, 13 27, 10 24, 8 23, 5 19, 3 17 31, 14 28, 11 25, 9 23, 6 20, 4 18",
    'Gelber Sack': "4 31, 28, 26, 24, 23, 19, 17, 14, 11, 9, 6, 4",
    'Papiertonne': "24, 21, 20, 17, 15, 12, 10, 7, 4, 2 30, 27, 24",
    'Biotonne': "10 24, 7 21, 6 20, 4 17, 2 15 29, 12 26, 10 24, 7 21, 4 18, 2 16 30, 13 27, 11 24",
}

calendar_data = {
    'Restmüll': "2 15 29, 12 26, 12 26, 9 24, 7 21, 4 18, 2 16 30, 13 27, 10 24, 8 22, 5 19, 3 17 31",
    'Gelber Sack': "2 29, 26, 26, 24, 21, 18, 16, 13, 10, 8, 5, 3 31",
    'Papiertonne': "22, 19, 19, 16, 14, 12, 9, 6, 3, 1 29, 26, 23",
    'Biotonne': "8 22, 5 19, 6 19, 2 16 30, 14 28, 12 25, 9 23, 6 20, 3 17, 1 15 29, 12 26, 10 23",
}


def generate_ics():
    cal = Calendar()

    for calname, caldata in calendar_data.items():
        monthly_days = [x.strip() for x in caldata.split(",")]

        if len(monthly_days) != 12:
            print(f"warning: data for {calname} contains events in {len(monthly_days)} months, probably wrong")

        for month, month_days in enumerate(monthly_days):
            for day in [int(x) for x in month_days.split(" ")]:
                if (month + 1) < 1 or (month + 1) > 12:
                    pass
                d = datetime(year, month + 1, day, tzinfo=local_tzinfo).date()

                event = Event()
                ascii_calname = calname.encode("ascii", errors="ignore").decode()
                event['uid'] = f'muellkalender2024-{ascii_calname}-{d.year}{d.month:02}{d.day:02}'
                event.add('summary', calname)
                event.add('description', f"Bezirk {bezirk}")
                event.add('dtstart', d)
                event.add('dtend', d + timedelta(days=1))
                cal.add_component(event)

    return cal.to_ical()


if __name__ == '__main__':
    with open(f"muellcal_{year}.ics", "wb") as f:
        f.write(generate_ics())
