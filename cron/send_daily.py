import up  # to go to root folder
import time
from datetime import datetime, timedelta

from shared_utils.conf import conf as shared_conf

import conf
from src.data.load import load_records
from src.msgs.prettify import prettify_time_slot
from src.utils.date import prettify_date
from src.utils.errors import errors
from src.utils.slack import slack_status
from src.utils.tg import tg_send


URL = 'https://cist.nure.ua/ias/app/tt/f?p=778:201:1393283551304514:::' \
      '201:P201_FIRST_DATE,P201_LAST_DATE,P201_GROUP,P201_POTOK:{},{},{},0:'


def get_url(group, date_from, days):
    date_to = date_from + timedelta(days=days - 1)

    group_id = conf.cist_ids[group]
    str_from = date_from.strftime('%d.%m.%Y')
    str_to = date_to.strftime('%d.%m.%Y')

    return URL.format(str_from, str_to, group_id)


def get_url_semester(group):
    group_id = conf.cist_ids[group]
    return URL.format(conf.date_from, conf.date_to, group_id)


@errors('send_daily')
def send_daily():
    def send_weekly():
        if not is_sunday:
            raise Exception('...')
        semester_start = datetime.strptime(conf.date_from, '%d.%m.%Y')
        # nonlocal now
        # now += timedelta(days=7)  # just for debugging...
        # n = (now - semester_start).days // 7 + 2
        # message = f'📆 <b>Розклад на {n}-й тиждень</b>\n\n'
        message = f'📆 Розклад на тиждень\n\n'
        for delta in range(1, 7):
            day = now + timedelta(days=delta)
            sub_message, has_items = pretty_day(day, in_week=True)
            message += f'{sub_message}\n'
        url_week = get_url(group, now + timedelta(days=1), 7)
        url_semester = get_url_semester(group)
        message += f'🌐 <b>cist</b> — <a href="{url_week}">week</a> & ' \
                   f'<a href="{url_semester}">semester</a>\n' \
                   f'#тиждень'
        tg_send(channel_id, '📁')
        tg_send(channel_id, message, pin=True)

    def pretty_day(day, in_week=False):
        day_key = day.strftime('%Y/%m/%d')
        day_prettify = prettify_date(day)
        if in_week:
            message = f'▪️ {day_prettify}\n'
        else:
            title = 'завтра'
            real_now = datetime.now()
            if now.month == real_now.month and now.day + 1 == real_now.day:
                title = 'сьогодні'
            message = f'📆 Розклад на {title}\n\n' \
                      f'▪️ {day_prettify}\n'
        has_items = False
        day_table = data[group][day_key]
        if day_table:
            for time_from in sorted(day_table):
                message += prettify_time_slot(day_table, group, time_from)
            has_items = True
        else:
            message += f'🔆 Схоже, занять немає\n'
        return message, has_items

    now = datetime.now()
    # now = datetime(2022, 2, 13)  # just for debug
    # now = datetime(2022, 8, 28)  # just for debug
    # now = datetime(2023, 2, 12)  # to emulate Sunday initial start
    # now = datetime(2023, 3, 19)  # to emulate Sunday initial start
    # now = datetime(2024, 9, 1)  # to emulate Sunday initial start
    is_sunday = now.weekday() == 6
    tomorrow = now + timedelta(days=1)
    data = load_records()
    for group, channel_id in conf.channels.items():
        if is_sunday:
            send_weekly()

        message, has_items = pretty_day(tomorrow)
        url_day = get_url(group, now + timedelta(days=1), 1)
        url_semester = get_url_semester(group)
        message += f'\n🌐 <b>cist</b> — <a href="{url_day}">day</a> & ' \
                   f'<a href="{url_semester}">semester</a>\n' \
                   f'#день'

        if has_items:
            tg_send(channel_id, '📝')
            tg_send(channel_id, f'{message}')
        else:
            slack_status(f'No items for {group}')  # todo
        time.sleep(1.5)


if __name__ == '__main__':
    print(datetime.now())

    shared_conf.slack_hooks = conf.slack_hooks
    send_daily()
