import shared_utils.api.telegram.telegram_utils as tg

import conf
from bot.utils.basic import basic_handler
from src.utils.tg import tg_send


class TextHandler:
    context = None
    bot = None
    update = None
    chat_id = None
    input = None
    msg = None

    def send(self, message, keyboard=None, buttons=None):
        return tg.send(self.bot, self.chat_id, message,
                       keyboard=keyboard, buttons=buttons)

    def get_chats(self, options):
        options = options.strip()
        if options[0] != '[' or options[-1] != ']':
            return
        options = options[1:-1]

        chats = []
        slugs = options.split(', ')
        for slug in slugs:
            if '-' in slug:
                chats.append(f'ПЗПІ-{slug}')

            groups_count = {
                '19': 11,
                '20': 10,
                '21': 11,
                '22': 10,
            }
            if slug in groups_count:
                chats.extend([
                    f'ПЗПІ-{slug}-{num}'
                    for num in range(1, groups_count[slug] + 1)
                ])
        return chats

    @basic_handler
    def text(self):
        if self.chat_id != conf.telegram_admin:
            self.msg = self.send('🤷🏻‍♂️ Потрібен адмінський доступ')
            return

        data = self.input.replace('/text', '')
        options, text = data.split('\n', maxsplit=1)
        chats = self.get_chats(options)
        if not chats:
            self.send('⚠️ Помилка в параметрах')
            return

        for group, chat_id in conf.channels.items():
            if group in chats:
                print(group)
                tg_send(chat_id, text)
        self.send('✔️ Текст відправлено')

    @basic_handler
    def vote(self):
        if self.chat_id != conf.telegram_admin:
            self.msg = self.send('🤷🏻‍♂️ Потрібен адмінський доступ')
            return

        data = self.input.replace('/vote', '')
        options, question, *answers = data.split('\n')

        is_anonymous = True
        # if 'a+' in options:
        #     is_anonymous = True
        #     options = options.replace('a+', '')
        # elif 'a-' in options:
        #     options = options.replace('a-', '')

        allows_multiple = False
        if 'm+' in options:
            allows_multiple = True
            options = options.replace('m+', '')
        elif 'm-' in options:
            options = options.replace('m-', '')

        chats = self.get_chats(options)
        if not chats:
            self.send('⚠️ Помилка в параметрах')
            return

        for group, chat_id in conf.channels.items():
            if group in chats:
                print(group)
                self.bot.send_poll(chat_id, question, answers,
                                   is_anonymous=is_anonymous,
                                   allows_multiple_answers=allows_multiple)
        self.send('✔️ Опитування відправлено')

    @basic_handler
    def default(self):
        if self.update.message.chat_id != self.update.message.from_user.id:
            return
        self.msg = self.send('🤷🏻‍♂️ Інтерфейс взаємодії з ботом поки що '
                             'не реалізован')
