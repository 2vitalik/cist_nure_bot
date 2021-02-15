import up  # to go to root folder
from datetime import datetime, timedelta

from shared_utils.conf import conf as shared_conf
from telegram import Bot, ParseMode

import conf
from src.msgs.prettify import prettify_time_slot
from src.data.load import load_records


def send_lesson():
    now = datetime.now() + timedelta(minutes=5)
    day_key = now.strftime('%Y/%m/%d')
    time_key = now.strftime('%H:%M:00')

    data = load_records()
    for group, channel_id in conf.channels.items():
        day_table = data[group][day_key]
        if time_key in day_table:
            message = prettify_time_slot(day_table, time_key)
            bot.send_message(channel_id, message, parse_mode=ParseMode.HTML)


if __name__ == '__main__':
    bot = Bot(conf.telegram_token)
    shared_conf.slack_hooks = conf.slack_hooks
    send_lesson()
