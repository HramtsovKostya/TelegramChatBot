# --------------------------------- MAIN ----------------------------------

import config as cnf
from chat_bot import ChatBot

from model.subscribe import Subscriber
from model.schedule import BotScheduler
from parse.sheet_parser import SheetParser

# -------------------------------------------------------------------------

if __name__ == '__main__':
    # ? Создание парсера
    # parser = SheetParser(
	# 	file_name=cnf.CREDENTIALS_FILE, 
    #     scopes=[cnf.GOOGLE_SHEETS_API, cnf.GOOGLE_DRIVE_API]
    # )

    # df = parser.get(cnf.SPREAD_SHEET_ID)
    # SheetParser.save(df, cnf.SPREAD_SHEET_FILE)
    
    # ? Создание расписания
    # scheduler = BotScheduler()
    # scheduler.start()
    
    # ? Запуск чат-бота
    ChatBot().start()
    
    # scheduler.stop()
    
# -------------------------------------------------------------------------