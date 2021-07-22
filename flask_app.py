# ------------------------------- FLASK-APP --------------------------------

import config as cfg

from flask import Flask
from flask import request

from telebot.apihelper import types as ts
from chat_bot import __bot, ChatBot
from subscribe import Subscriber
from sheet_parser import SheetParser
from bot_notifier import BotNotifier

# -------------------------------------------------------------------------

app = Flask(__name__)


@app.route("/", methods=['POST'])
def index():
    json_string = request.get_data().decode('utf-8')
    update = ts.Update.de_json(json_string)
    __bot.process_new_updates([update])
    return ''

# -------------------------------------------------------------------------

if __name__ == "__main__":

    # ? Загрузка данных из файлов
    users = Subscriber.load(cfg.USERS_LIST_FILE)
    sheet = SheetParser.load(cfg.SPREAD_SHEET_FILE)

    # ? Создание уведомителя
    notifier = BotNotifier(__bot)

    # ? Запуск уведомителя
    notifier.start()

    __bot.delete_webhook()
    __bot.set_webhook(cfg.WEBHOOK_URL)

    # ? Создание и запуск чат-бота    
    chat_bot = ChatBot(users, sheet)
    chat_bot.start(__bot)

    app.run()

    # ? Остановка уведомителя
    notifier.stop()

# -------------------------------------------------------------------------