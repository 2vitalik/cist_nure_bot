import up  # to go to root folder
from datetime import datetime

import conf

import requests


def send_webhook():
    webhook_url = conf.google_chat_webhook
    message = {
        "text": '🖐️ Напишіть "+" в ланцюжку 🙂'
    }
    response = requests.post(webhook_url, json=message)
    if response.status_code == 200:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{now}: Повідомлення успішно відправлено!")
    else:
        print(f"Помилка: {response.status_code}, {response.text}")


if __name__ == '__main__':
    send_webhook()
