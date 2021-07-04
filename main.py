# --------------------------------- MAIN ----------------------------------

import config as cnf
from chat_bot import bot, users, sheet

from model.subscribe import Subscriber
from model.schedule import BotScheduler
from parse.sheet_parser import SheetParser

# -------------------------------------------------------------------------

if __name__ == '__main__':
    # parser = SheetParser(
	# 	file_name=cnf.CREDENTIALS_FILE, 
    #     scopes=[cnf.GOOGLE_SHEETS_API, cnf.GOOGLE_DRIVE_API]
    # )

    # df = parser.get(cnf.SPREAD_SHEET_ID)
    # SheetParser.save(df, cnf.SPREAD_SHEET_FILE)
    
    # scheduler = BotScheduler()
    # scheduler.start()
    
    users = Subscriber.load(cnf.USERS_LIST_FILE)
    sheet = SheetParser.load(cnf.SPREAD_SHEET_FILE)
    
    print("Бот успешно запущен!")
    bot.polling(none_stop=True, timeout=20)
    print("Бот остановлен!")
    
    # scheduler.stop()
    
# -------------------------------------------------------------------------