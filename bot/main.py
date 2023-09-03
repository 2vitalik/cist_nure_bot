import shared_utils.api.telegram.telegram_utils as tg

import conf
from bot.utils.basic import basic_handler
from src.utils.tg import tg_send


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
        if self.chat_id != self.update.message.from_user.id:
            self.msg = self.send('🤷🏻‍♂️ Интерфейс индивидуального взаимодействия'
                                 ' пока не доступен')
