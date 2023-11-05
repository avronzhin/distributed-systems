import datetime


def get_timestamp_from_date(date_input):
    return int(datetime.datetime.fromisoformat(date_input.isoformat()).timestamp())


def get_date_from_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)