# ------------------------------- SCHEDULE --------------------------------

import pandas as pd
import schedule as sch
import time

from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from datetime import datetime, timedelta
from threading import Thread
from chat_bot import ChatBot


# -------------------------------------------------------------------------

class BotNotifier(object):
	def __init__(self, bot: TeleBot):
		self.__bot = bot
		self.__is_working = True

	def start(self):
		Thread(target=self.__schedule).start()
		print('\nРассылка уведомлений запущена!')

	def stop(self):
		self.__is_working = False
		print('Рассылка уведомлений остановлена!\n')		

	def __schedule(self):
		sch.every(10).minutes.do(self.__notify)

		while self.__is_working:
			sch.run_pending()
			time.sleep(3)

	def __notify(self):
		subs, groups, admins = self.__get_role_users()

		for user in subs:
			data = self.__get_by_name(ChatBot.sheet(), user.user_name)

			if data is not None:
				week = self.__next_week(data['Дата начала курса'])

				if week is not None:
					user_id = user.chat_id
					text = self.__get_user_notification(week, data)
					self.__bot.send_message(user_id, text, parse_mode='html')

					for group in groups:
						group_id = group.chat_id
						try:
							self.__bot.get_chat_member(group_id, user_id)
							self.__bot.send_message(group_id, text, parse_mode='html')
						except ApiTelegramException:
							continue

					for admin in admins:
						admin_id = admin.chat_id
						if admin_id != user_id:
							text = self.__get_admin_notification(week, data, admin.user_name)
							self.__bot.send_message(admin_id, text, parse_mode='html')
					
					print('Пользователь ' + user.user_name + ' уведомлен')
		print('Все уведомления разосланы!') 

# -------------------------------------------------------------------------

	def __get_user_notification(self, week: int, data: pd.DataFrame):
		text = self.__get_notification(week, data,  data['Преподаватель'])
		return self.__get_place_and_time(text, data)

	def __get_admin_notification(self, week: int, data: pd.DataFrame, admin_name: str):
		text = self.__get_notification(week, data, admin_name)
		text += '\nПреподаватель: ' + data['Преподаватель']
		return self.__get_place_and_time(text, data)

	def __get_place_and_time(self, text, data):
		text += '\nМесто и время проведения: \n' + data['Место проведения']
		text += ', c ' + data['Время проведения'].replace('-', ' до ') + '.'
		return text

	def __get_notification(self, week: int, data: pd.DataFrame, user_name: str):
		module, lesson = self.__get_module_lesson(week)
		
		text = 'Добрый день, <b>' +  user_name + '</b>!\n'
		text += '\nСпешу вас уведомить, что через неделю, а именно '
		text += self.__normalize_date(data['Дата начала курса'], week) + ', у '
		text += str(data['Поток курса']) + '-го потока курса <i>"'
		text += data['Название курса']  + '"</i> пройдет ' +  str(lesson)
		text += '-e занятие ' + str(module) + '-го модуля.\n'
		return text

	def __get_module_lesson(self, week):
		module =  week // 4 if week % 4 == 0 else week // 4 + 1
		lesson = week % 4 if week % 4 > 0 else 4     
		return (module, lesson)

	def __get_by_name(self, df: pd.DataFrame, name: str):
		for i, record in df.iterrows():
			if record['Преподаватель'] == name:
				return record
		return None

	def __next_week(self, date: str):
		for week in range(12):
			dt = datetime.strptime(date, '%Y-%m-%d') + timedelta(weeks=week)
			dt_next = datetime.now() + timedelta(weeks=1)
			
			if dt.date() == dt_next.date():
				return week + 1
		return None

	def __normalize_date(self, date: str, number: int):
		dt = datetime.strptime(date, '%Y-%m-%d') + timedelta(weeks=number-1)
		return dt.strftime('%d.%m.%Y') + 'г.'

	def __get_role_users(self):
		subs, groups, admins = [], [], []
		for user in ChatBot.users():
			if user.is_subscriber():
				subs.append(user)
			if user.is_admin():
				admins.append(user)
			if user.is_group():
				groups.append(user)
			
		return subs, groups, admins

# -------------------------------------------------------------------------