import shared_utils.api.telegram.telegram_utils as tg


def basic_handler(func):
    def wrapper(self, update, context):
        self.bot = context.bot
        self.update = update
        self.chat_id = update.message.chat_id
        self.input = update.message.text.strip()
        return func(self)
    return wrapper


class MainHandler:
    bot = None
    update = None
    chat_id = None
    input = None
    msg = None

    def send(self, message, keyboard=None, buttons=None):
        return tg.send(self.bot, self.chat_id, message,
                       keyboard=keyboard, buttons=buttons)

    @basic_handler
    def default(self):
        self.msg = self.send('🤷🏻‍♂️ Интерфейс индивидуального взаимодействия'
                             ' пока не доступен')
