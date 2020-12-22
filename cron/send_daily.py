import up  # to go to root folder
from datetime import datetime, timedelta

from shared_utils.conf import conf as shared_conf
from telegram import Bot, ParseMode

import conf
from src.data.load import load_data
from src.msgs.prettify import prettify_time_slot
from src.utils.date import prettify_date


def send_daily():
    def send_weekly():
        if not is_sunday:
            raise Exception('...')
        n = 18  # fixme
        message = f'📆 <b>Розклад на {n}-й тиждень</b>\n\n'
        for delta in range(1, 7):
            day = now + timedelta(days=delta)
            message += pretty_day(day, in_week=True) + '\n'
        message += '#тиждень'
        bot.send_message(channel_id, message, parse_mode=ParseMode.HTML)

    def pretty_day(day, in_week=False):
        day_key = day.strftime('%Y/%m/%d')
        day_prettify = prettify_date(day)
        if in_week:
            message = f'▪️ {day_prettify}\n'
        else:
            message = f'📆 Розклад на {day_prettify}\n\n'
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
    data = load_data()
    for group, channel_id in conf.channels.items():
        if is_sunday:
            send_weekly()
        message = pretty_day(tomorrow) + '\n#день'
        bot.send_message(channel_id, message, parse_mode=ParseMode.HTML)


if __name__ == '__main__':
    bot = Bot(conf.telegram_token)
    shared_conf.slack_hooks = conf.slack_hooks
    send_daily()
