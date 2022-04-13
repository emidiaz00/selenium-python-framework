from datetime import timedelta

from dateutil.tz import tz


def parse_date_time_from_utc_to_argentina_timezone(datetime):
    difference_hours = datetime.astimezone(tz.gettz('America/Argentina/Buenos_Aires')).utcoffset().total_seconds() / 60 / 60
    return datetime + timedelta(hours=difference_hours)
