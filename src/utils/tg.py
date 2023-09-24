import time

from telegram import Bot, ParseMode
from telegram.error import TimedOut, RetryAfter, NetworkError

import conf
from src.utils.slack import slack_error

bot = Bot(conf.telegram_token)


def add_quote(text):
    return text.replace('\n', '\n> ')


def tg_send(chat_id, text, pin=False):
    try:
        msg = bot.send_message(chat_id, text,
                         parse_mode=ParseMode.HTML,
                         disable_web_page_preview=True)
        if pin:
            bot.pin_chat_message(chat_id, msg.message_id, True)
    except (TimedOut, RetryAfter, NetworkError) as e:
        message = (f'`tg_send`  *{type(e).__name__}*: {str(e)}\n\n'
                   f'Pause for 1 minute...\n\n'
                   f'>chat_id: {chat_id}\n\n'
                   f'>{add_quote(text)}')
        slack_error(message)
        tg_send(conf.telegram_admin, message)
        time.sleep(60)
        return tg_send(chat_id, text)
