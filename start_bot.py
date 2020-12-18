import logging

from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters
from shared_utils.conf import conf as shared_conf

import conf
from bot.main import MainHandler


def start_bot():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s (%(name)s):  %(message)s'
    )
    shared_conf.slack_hooks = conf.slack_hooks

    bot = Bot(conf.telegram_token)
    bot.send_message(chat_id=conf.telegram_admin, text='💬 Starting the bot...')

    handler = MainHandler()

    updater = Updater(token=conf.telegram_token)
    dispatcher = updater.dispatcher
    # dispatcher.add_handler(CommandHandler('buttons', handler.process_buttons,
    #                                       pass_args=False))
    dispatcher.add_handler(MessageHandler(Filters.text, handler.default))
    # dispatcher.add_handler(CallbackQueryHandler(handler.process_callback))

    updater.start_polling()
    print('Bot has successfully started.')
    updater.idle()
    print('Bot has finished.')


if __name__ == '__main__':
    start_bot()
