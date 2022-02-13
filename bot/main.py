import shared_utils.api.telegram.telegram_utils as tg

import conf
from src.utils.tg import tg_send


def basic_handler(func):
    def wrapper(self, update, context):
        self.context = context
        self.bot = context.bot
        self.update = update
        self.chat_id = update.message.chat_id
        self.input = update.message.text.strip()
        return func(self)
    return wrapper


class MainHandler:
    context = None
    bot = None
    update = None
    chat_id = None
    input = None
    msg = None

    def send(self, message, keyboard=None, buttons=None):
        return tg.send(self.bot, self.chat_id, message,
                       keyboard=keyboard, buttons=buttons)

    @basic_handler
    def send_cmd(self):
        if self.chat_id != conf.telegram_admin:
            self.msg = self.send('🤷🏻‍♂️ Команда доступна только админу :)')
            return

        text = self.input.replace('/send', '')
        for group, channel_id in conf.channels.items():
            tg_send(channel_id, text)
        self.send('✔️ Сообщение отправлено')

    @basic_handler
    def default(self):
        self.msg = self.send('🤷🏻‍♂️ Интерфейс индивидуального взаимодействия'
                             ' пока не доступен')
