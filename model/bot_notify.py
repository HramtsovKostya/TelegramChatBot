# -------------------------------------------------------------------------

import config as cnf
import schedule as sch
import threading as thr
import time

from os import path

# ------------------------------- NOTIFIER --------------------------------

class BotNotifier(object):	
	def __init__(self, bot):
		self.__bot = bot
		self.__is_working = True

	def __notify(self):
		print('Уведомления разосланы!')

	def __schedule(self):
		sch.every(3).minutes.do(self.__notify)

		while self.__is_working:
			sch.run_pending()
			time.sleep(1)

	def start(self):
		thread = thr.Thread(target=self.__schedule)
		thread.start()
		print('Расписание запущено!')

	def stop(self):
		self.__is_working = False
		print('Расписание остановлено!')

# -------------------------------------------------------------------------