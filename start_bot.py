import logging

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, \
    Dispatcher
from shared_utils.conf import conf as shared_conf

import conf
from bot.main import MainHandler
from bot.text import TextHandler
from src.utils.tg import tg_send


def enable_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s (%(name)s):  %(message)s'
    )


def add_handles(dispatcher: Dispatcher):
    handler = MainHandler()
    text_handler = TextHandler()

    dispatcher.add_handler(CommandHandler('send', handler.send_cmd))
    dispatcher.add_handler(CommandHandler('text', text_handler.text))
    dispatcher.add_handler(CommandHandler('vote', text_handler.vote))
    dispatcher.add_handler(MessageHandler(Filters.text, handler.default))
    # dispatcher.add_handler(CallbackQueryHandler(handler.process_callback))


def start_bot():
    shared_conf.slack_hooks = conf.slack_hooks

    enable_logging()
    tg_send(conf.telegram_admin, '💬 Starting the bot...')

    updater = Updater(token=conf.telegram_token)
    add_handles(updater.dispatcher)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    start_bot()
