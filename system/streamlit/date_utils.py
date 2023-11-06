import datetime


def get_timestamp_from_date(date_input: datetime.date):
    return int(datetime.datetime.fromisoformat(date_input.isoformat()).timestamp())


def get_date_from_timestamp(timestamp: int | float):
    return datetime.datetime.fromtimestamp(timestamp)


def split_by_days(start_date: datetime.date, end_date: datetime.date):
    days = list()
    day = start_date
    while day < end_date:
        days.append(day)
        day = day + datetime.timedelta(days=1)
    return days


def split_day_by_interval(day: datetime.date, interval_hours: int):
    interval_timestamp = interval_hours * 60 * 60
    next_day = day + datetime.timedelta(days=1)
    next_day_timestamp = get_timestamp_from_date(next_day)
    day_timestamp = get_timestamp_from_date(day)
    day_timestamps = list()
    while day_timestamp < next_day_timestamp:
        day_timestamps.append(day_timestamp)
        day_timestamp = day_timestamp + interval_timestamp
    return day_timestamps, interval_timestamp
