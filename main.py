# --------------------------------- MAIN ----------------------------------

import config as cnf
from chat_bot import bot

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
    
    print("Бот успешно запущен!")
    bot.polling(none_stop=True, timeout=20)
    print("Бот остановлен!")
    
    # scheduler.stop()
    
# -------------------------------------------------------------------------