# --------------------------------- MAIN ----------------------------------

import config as cfg

from sheet_parser import SheetParser
from subscribe import Subscriber
from chat_bot import ChatBot, __bot
from bot_notifier import BotNotifier

# -------------------------------------------------------------------------

if __name__ == '__main__':
    # ? Создание экземпляра парсера
    # parser = SheetParser(
    # 	file_name=cfg.CREDENTIALS_FILE, 
    #     scopes=[cfg.GOOGLE_SHEETS_API, cfg.GOOGLE_DRIVE_API]
    # )

    # ? Загрузка данных из гугл-таблицы
    # data = parser.get(cfg.SPREAD_SHEET_ID)
    # SheetParser.save(data, cfg.SPREAD_SHEET_FILE)

    # ? Загрузка данных из файлов
    users = Subscriber.load(cfg.USERS_LIST_FILE)
    sheet = SheetParser.load(cfg.SPREAD_SHEET_FILE)

    # ? Создание уведомителя
    notifier = BotNotifier(__bot)

    # ? Запуск уведомителя
    notifier.start()

    # ? Создание и запуск чат-бота    
    chat_bot = ChatBot(users, sheet)
    chat_bot.start(__bot)

    # ? Остановка уведомителя
    notifier.stop()
    
# -------------------------------------------------------------------------