# --------------------------------- MAIN ----------------------------------

from chat_bot import ChatBot, __bot
from bot_notifier import BotNotifier

# -------------------------------------------------------------------------

if __name__ == '__main__':
    # ? Создание парсера
    # parser = SheetParser(
	# 	file_name=cnf.CREDENTIALS_FILE, 
    #     scopes=[cnf.GOOGLE_SHEETS_API, cnf.GOOGLE_DRIVE_API]
    # )

    # ? Загрузка данных из гугл-таблицы
    # data = parser.get(cnf.SPREAD_SHEET_ID)
    # SheetParser.save(data, cnf.SPREAD_SHEET_FILE)
    
    # ? Создание чат-бота
    chat_bot = ChatBot()

    # ? Создание уведомителя
    notifier = BotNotifier(chat_bot)
    
    # ? Запуск уведомителя
    notifier.start(__bot)
    
    # ? Запуск чат-бота    
    chat_bot.start(__bot)
    
    # ? Остановка уведомителя
    notifier.stop()
    
# -------------------------------------------------------------------------