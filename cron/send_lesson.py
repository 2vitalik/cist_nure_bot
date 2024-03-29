import time

import up  # to go to root folder
from datetime import datetime, timedelta

from shared_utils.conf import conf as shared_conf

import conf
from src.msgs.prettify import prettify_time_slot
from src.data.load import load_records
from src.utils.errors import errors
from src.utils.tg import tg_send


@errors('send_lesson')
def send_lesson():
    now = datetime.now() + timedelta(minutes=5)
    day_key = now.strftime('%Y/%m/%d')
    time_key = now.strftime('%H:%M:00')

    data = load_records()
    for group, channel_id in conf.channels.items():
        day_table = data[group][day_key]
        if time_key in day_table:
            message = prettify_time_slot(day_table, group, time_key, alarm=True)
            tg_send(channel_id, message)
            time.sleep(1)


if __name__ == '__main__':
    shared_conf.slack_hooks = conf.slack_hooks
    send_lesson()
