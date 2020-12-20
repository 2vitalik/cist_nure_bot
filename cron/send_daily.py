from datetime import datetime, timedelta

from shared_utils.conf import conf as shared_conf
from telegram import Bot, ParseMode

import conf
from src.data.const import times
from src.data.load import load_data
from src.utils.date import prettify_date


def prettify_lesson(subject, kind, room):
    icons = {
        'лк': '💬',
        'пз': '💡',
        'лб': '⚙️',
    }
    icon = icons.get(kind, '❔')
    return f'{icon} ({kind}) <b>{subject}</b> → {room}'


def send_daily():
    def send_weekly():
        now = datetime.now()
        is_sunday = now.weekday() == 6
        if not is_sunday:
            raise Exception('...')
        n = 17  # fixme
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
                lessons = list(reversed(day_table[time_from]))
                number = times.get(time_from, '*️⃣')
                line = prettify_lesson(*lessons[0])
                message += f'{number} <code>{time_from[:5]}</code>: {line}\n'
                for lesson in lessons[1:]:
                    line = prettify_lesson(*lesson)
                    message += f'▫️<code>     </code>   {line}\n'
        else:
            message += f'🔆 Схоже занять немає\n'
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
