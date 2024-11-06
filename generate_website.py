import os
from datetime import date, datetime
from typing import Iterable
import itertools

#import pandas as pd
import jinja2
import yaml

from constants import (DIR_TEMPLATES, DIR_PUBLIC, DIR_DATA,
                       COL_CONF_TYPE,
                       MAP_CONF_TYPE,
                      )

FORMATTER_DATE = lambda x: date.strftime(x, "%B %d, %Y")

def load_data():
    yml_files = [x for x in os.listdir(DIR_DATA) if x.endswith(".yml")]
    data = []
    for _file in yml_files:
        print(_file)
        _file_path = os.path.join(DIR_DATA, _file)
        with open(_file_path, 'r') as yml_file:
            data.extend(yaml.safe_load(yml_file))
    return data

def create_conference_table(conf_list: Iterable, year: int=date.today().year):
    week_data = {k+1: [] for k in range(52)}
    deadline_data = {k+1: [] for k in range(52)}
    for conference in conf_list:
        #conference["type"] = MAP_CONF_TYPE.get(conference.get("type", "Unknown"), "unknown")
        conference['type'] = conference.get("type", "unknown")
        dates = conference.get("dates")
        if dates is None:# or len(dates) != 2:
            continue
        for _conf_dates in dates:
            _start_date, _end_date = _conf_dates
            if _start_date.year != year:
                continue
            start_week = _start_date.isocalendar()[1]
            week_data[start_week].append(conference)
            end_week = _end_date.isocalendar()[1]
            if end_week != start_week:
                week_data[end_week].append(conference)
        deadlines = conference.get("deadline")
        if deadlines is None:
            continue
        for deadline in deadlines:
            deadline_iso = deadline.isocalendar()
            deadline_sort_year = deadline_iso.year
            if deadline_sort_year != year:
                continue
            deadline_week = deadline_iso.week
            deadline_data[deadline_week].append(conference)
    return week_data, deadline_data

def week_days_format(week: int, year=date.today().year, format="%b %d"):
    first_day = date.fromisocalendar(year, week, 1)
    last_day = date.fromisocalendar(year, week, 7)
    _text = "{} &ndash; {}".format(first_day.strftime(format),
                                   last_day.strftime(format))
    return _text

def main():
    data = load_data()
    #print(week_data)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(DIR_TEMPLATES))
    env.filters['weekdates'] = week_days_format
    #template = env.get_template("index.html")
    template = env.get_template("weeks.html")

    today = date.today()
    now = datetime.now()
    timestamp = today.strftime("%B %d, %Y")

    import icalendar
    cal = icalendar.Calendar()
    cal.add("prodid", "-//Conference Calendar//Conference Calendar//EN")
    cal.add("version", "2.0")
    cal_deadline = icalendar.Calendar()
    cal_deadline.add("prodid", "-//Conference Deadlines//Conference Calendar//EN")
    cal_deadline.add("version", "2.0")
    for conference in data:
        for start_date, end_date in conference.get("dates", []):
            event = icalendar.Event()
            uid = "{:%Y%m%d}{:%Y%m%d}-{}".format(start_date, end_date,
                                                conference["abbreviation"])
            event.add("uid", uid)
            event.add("dtstamp", now)
            event.add("summary", conference['name'])
            event.add("dtstart", start_date)
            event.add("dtend", end_date)
            cal.add_component(event)
        for deadline in conference.get("deadline", []):
            event = icalendar.Event()
            uid = "{:%Y%m%d}-{}".format(deadline, conference["abbreviation"])
            event.add("uid", uid)
            event.add("dtstamp", now)
            #event.add("summary", conference['name'])
            event.add("summary", f"Deadline: {conference['abbreviation']}")
            event.add("dtstart", deadline)
            cal_deadline.add_component(event)
    with open(os.path.join(DIR_PUBLIC, "conferences.ics"), "wb") as ics_file:
        ics_file.write(cal.to_ical())
    with open(os.path.join(DIR_PUBLIC, "deadlines.ics"), "wb") as ics_file:
        ics_file.write(cal_deadline.to_ical())


    week_data = {}
    deadline_data = {}
    for year in [today.year, today.year+1]:
        _week_data, _deadline_data = create_conference_table(data, year)
        week_data[year] = _week_data
        deadline_data[year] = _deadline_data
    datasets = [("Conference Dates", "index.html", week_data),
                ("Submission Deadlines", "deadlines.html", deadline_data),
                ]
    for _title, _html_file, _data in datasets:
        content = template.render(conferences=data,
                                  conf_data=_data,
                                  title=_title,
                                  timestamp=timestamp,
                                  today=today)
        out_path = os.path.join(DIR_PUBLIC, _html_file)
        with open(out_path, 'w') as html_file:
            html_file.write(content)

if __name__ == "__main__":
    results = main()
