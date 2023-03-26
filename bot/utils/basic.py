def basic_handler(func):
    def wrapper(self, update, context):
        self.context = context
        self.bot = context.bot
        self.update = update
        self.chat_id = update.message.chat_id
        self.input = update.message.text.strip()
        return func(self)
    return wrapper
