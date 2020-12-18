import re
from datetime import datetime, timedelta


def dt_text(value):
    m = re.match('(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\.\d{3}-(\d{2}):00',
                 value)
    if not m:
        return value

    dt_val, value_tz = m.groups()
    dt_val = datetime.strptime(dt_val, '%Y-%m-%dT%H:%M:%S')
    dt_val += timedelta(hours=int(value_tz) + 2)
    if dt_val.hour == 23 and dt_val.minute == dt_val.second == 0:
        dt_val += timedelta(hours=1)
    value = dt_val.strftime('%Y/%m/%d %H:%M:%S')

    remove_suffixes = [' 00:00:00']
    for suffix in remove_suffixes:
        if value.endswith(suffix):
            value = value[:-len(suffix)]

    remove_prefixes = ['1899/12/30 ']
    for prefix in remove_prefixes:
        if value.startswith(prefix):
            value = value[len(prefix):]

    return value
