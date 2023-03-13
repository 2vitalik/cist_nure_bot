from datetime import datetime

from pytz import timezone


def convert_date(date_str):  # todo: move to coda-docs?
    date_str = date_str[:-3] + date_str[-2:]
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z'). \
        astimezone(timezone('Europe/Kiev'))


def prettify_date(date):
    months = [
        '',
        'січня',
        'лютого',
        'березня',
        'квітня',
        'травня',
        'червня',
        'липня',
        'серпня',
        'вересня',
        'жовтня',
        'листопада',
        'грудня',
    ]
    month = months[date.month]

    weekdays = [
        'понеділок',
        'вівторок',
        'середа',
        'четвер',
        "п'ятниця",
        'субота',
        'неділя',
    ]
    weekday = weekdays[date.weekday()]
    return f'<b>{date.day} {month}</b> ({weekday})'
