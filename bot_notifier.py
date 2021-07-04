# ------------------------------- SCHEDULE --------------------------------

import pandas as pd
import schedule as sch
import threading as thr
import time

from telebot import TeleBot
from subscribe import Role
from datetime import datetime, timedelta
from chat_bot import ChatBot

# -------------------------------------------------------------------------

class BotNotifier(object):	
	def __init__(self, bot: ChatBot):
		self.__is_working = True
		self.__users = bot.users()
		self.__sheet = bot.sheet()
  
	def start(self, bot: TeleBot):
		self.__bot = bot
		thread = thr.Thread(target=self.__schedule)
		thread.start()
		print('Расписание запущено!')

	def stop(self):
		self.__is_working = False
		print('Расписание остановлено!')
  
	def __schedule(self):
		sch.every(1).minutes.do(self.__notify)

		while self.__is_working:
			sch.run_pending()
			time.sleep(3)

	def __notify(self):
		groups = [u for u in self.__users if u.user_role == Role.GROUP]
       
		for user in self.__users:     
			if user.user_role == Role.TEACHER:
				data = self.__get_by_name(self.__sheet, user.user_name)
				is_equals, week = self.__next_week(data['Дата начала курса'])

				if data is not None and is_equals:
					text = self.__get_notification(week, data)
					self.__bot.send_message(user.chat_id, text, parse_mode='html')

					for group in groups:
						group_id = group.chat_id
						user_id = user.chat_id
      
						if self.__bot.get_chat_member(group_id, user_id) is not None:
							self.__bot.send_message(group_id, text,  parse_mode='html')

		print('Уведомления разосланы!')

	def __get_notification(self, week: int, data: pd.DataFrame):
		lesson = week % 4 if week % 4 > 0 else 4 
		module =  week // 4 if week % 4 == 0 else week // 4 + 1

		text = 'Добрый день, <b>' +  data['Преподаватель'] + '</b>!\n'
		text += '\nСпешу вас уведомить, что через неделю, \nа именно '
		text += self.__normalize_date(data['Дата начала курса'], week) + ', у '
		text += str(data['Поток курса']) + '-го потока\nкурса <i>"'
		text += data['Название курса']  + '"</i>\nпройдет ' +  str(lesson)
		text += '-e занятие ' + str(module) + '-го модуля.\n'
		text += '\nМесто и время проведения: \n' + data['Место проведения']
		text += ', c ' + data['Время проведения'].replace('-', ' до ')  + '.'
		return text
  
	def __get_by_name(self, df: pd.DataFrame, name: str):
		for i, row in df.iterrows():
			if row['Преподаватель'] == name:
				return row
		return None

	def __next_week(self, date: str):
		for week in range(12):
			dt = datetime.strptime(date, '%Y-%m-%d') + timedelta(weeks=week)
			dt_next = datetime.now() + timedelta(weeks=1)
			
			if dt.date() == dt_next.date():
				return (True, week+1)
		return (False, 0)

	def __normalize_date(self, date: str, number: int):
		dt = datetime.strptime(date, '%Y-%m-%d') + timedelta(weeks=number-1)
		return dt.strftime('%d.%m.%Y') + 'г.'

# -------------------------------------------------------------------------