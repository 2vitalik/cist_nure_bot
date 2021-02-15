import up  # to go to root folder
from datetime import datetime, timedelta

from shared_utils.conf import conf as shared_conf

import conf
from src.data.load import load_records
from src.msgs.prettify import prettify_time_slot
from src.utils.date import prettify_date
from src.utils.tg import tg_send


def send_daily():
    def send_weekly():
        if not is_sunday:
            raise Exception('...')
        n = 18  # fixme
        message = f'📆 <b>Розклад на тиждень</b>\n\n'  # todo: {n}-й
        for delta in range(1, 7):
            day = now + timedelta(days=delta)
            message += pretty_day(day, in_week=True) + '\n'
        message += '#тиждень'
        tg_send(channel_id, '📁')
        tg_send(channel_id, message)

    def pretty_day(day, in_week=False):
        day_key = day.strftime('%Y/%m/%d')
        day_prettify = prettify_date(day)
        if in_week:
            message = f'▪️ {day_prettify}\n'
        else:
            message = f'📆 Розклад на завтра\n\n' \
                      f'▪️ {day_prettify}\n'
        day_table = data[group][day_key]
        if day_table:
            for time_from in sorted(day_table):
                message += prettify_time_slot(day_table, time_from)
        else:
            message += f'🔆 Схоже, занять немає\n'
        return message

    now = datetime.now()
    is_sunday = now.weekday() == 6
    tomorrow = now + timedelta(days=1)
    data = load_records()
    for group, channel_id in conf.channels.items():
        if is_sunday:
            send_weekly()
        message = pretty_day(tomorrow) + '\n#день'
        tg_send(channel_id, '📝')
        tg_send(channel_id, message)


if __name__ == '__main__':
    shared_conf.slack_hooks = conf.slack_hooks
    send_daily()
