# ------------------------------- SCHEDULE --------------------------------

import config as cfg
import pandas as pd
import schedule as sch
import time

from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from datetime import datetime, timedelta
from threading import Thread
from chat_bot import ChatBot
from sheet_parser import SheetParser

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
		sch.every(5).minutes.do(self.__notify)
		# sch.every().day.at('09:00').do(self.__notify)

		while self.__is_working:
			sch.run_pending()
			time.sleep(3)

	def __notify(self):  # sourcery no-metrics
		# ? Создание экземпляра парсера
		# parser = SheetParser(
		# 	file_name=cfg.CREDENTIALS_FILE, 
		# 	scopes=[cfg.GOOGLE_SHEETS_API, cfg.GOOGLE_DRIVE_API]
		# )

		# ? Загрузка данных из гугл-таблицы
		# data = parser.get(cfg.SPREAD_SHEET_ID)
		# SheetParser.save(data, cfg.SPREAD_SHEET_FILE)

		for user in self.__get_subs():
			data = self.__get_by_name(ChatBot.sheet(), user.user_name)

			if data is not None and data['Стадия курса'] == 'Идет':
				self.__notify_about_lessons(user, data)
				self.__notify_about_master_class(user, data) 
				print('Пользователь ' + user.user_name + ' уведомлен')

		print('Все уведомления разосланы!') 

	def __notify_about_lessons(self, user, data):
		week = self.__next_week(data['Дата начала курса'])

		if week is not None:
			text = self.__get_user_notification(week, data)
			self.__bot.send_message(user.chat_id, text, parse_mode='html')

			for g in self.__get_groups():
				try:
					self.__bot.get_chat_member(g.chat_id, user.chat_id)
					self.__bot.send_message(g.chat_id, text, parse_mode='html')
				except ApiTelegramException:
					continue

			for a in self.__get_admins():
				if a.chat_id != user.chat_id:
					text = self.__get_admin_notification(week, data, a.user_name)
					self.__bot.send_message(a.chat_id, text, parse_mode='html')

	def __notify_about_master_class(self, user, data):
		is_master_class = self.__is_master_class(data['Мастер-класс']) 

		if is_master_class:
			text = self.__get_user_mc_notification(data)
			self.__bot.send_message(user.chat_id, text, parse_mode='html')
			
			for g in self.__get_groups():
				try:
					self.__bot.get_chat_member(g.chat_id, user.chat_id)
					self.__bot.send_message(g.chat_id, text, parse_mode='html')
				except ApiTelegramException:
					continue

			for a in self.__get_admins():
				if a.chat_id != user.chat_id:
					text = self.__get_admin_mc_notification(data, a.user_name)
					self.__bot.send_message(a.chat_id, text, parse_mode='html')

# -------------------------------------------------------------------------

	def __get_user_notification(self, week: int, data):
		text = self.__get_notification(week, data,  data['Преподаватель'])
		return self.__get_place_and_time(text, data)

	def __get_user_mc_notification(self, data):
		text = self.__get_mc_notification(data, data['Преподаватель'])
		return self.__get_place_and_time(text, data)

	def __get_admin_notification(self, week: int, data, admin_name: str):
		text = self.__get_notification(week, data, admin_name)
		text += '\nПреподаватель: ' + data['Преподаватель']
		return self.__get_place_and_time(text, data)

	def __get_admin_mc_notification(self, data, admin_name: str):
		text = self.__get_mc_notification(data, admin_name)
		text += '\nПреподаватель: ' + data['Преподаватель']
		return self.__get_place_and_time(text, data)

	def __get_place_and_time(self, text, data):
		text += '\nМесто и время проведения: ' + data['Место проведения']
		text += ', c ' + data['Время проведения'].replace('-', ' до ') + '.'
		return text

	def __get_notification(self, week: int, data, user_name: str):
		module, lesson = self.__get_module_lesson(week)
		
		text = 'Добрый день, <b>' +  user_name + '</b>!\n'
		text += '\nСпешу вас уведомить, что через неделю, а именно '
		text += self.__normalize_date(data['Дата начала курса'], week) + ', у '
		text += str(data['Поток курса']) + '-го потока курса <i>"'
		text += data['Название курса']  + '"</i> пройдет ' +  str(lesson)
		text += '-e занятие ' + str(module) + '-го модуля.\n'
		return text

	def __get_mc_notification(self, data, user_name: str):
		text = 'Добрый день, <b>' +  user_name + '</b>!\n'
		text += '\nСпешу вас уведомить, что через неделю, а именно '
		text += self.__normalize_date(data['Мастер-класс'], 1) + ', у '
		text += str(data['Поток курса']) + '-го потока пройдет мастер-класс '
		text += 'по курсу <i>"' + data['Название курса']  + '"</i>.\n'
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
		if isinstance(date, str) and not date.isspace():
			dt_start = datetime.strptime(date, '%Y-%m-%d')
			dt_now = datetime.now()
			
			for week in range(12):
				dt = dt_start + timedelta(weeks=week)
				dt_next = dt_now + timedelta(weeks=1)
				
				if dt.date() == dt_next.date():
					return week + 1
		return None

	def __is_master_class(self, date: str):
		if isinstance(date, str) and not date.isspace():
			dt_mc = datetime.strptime(date, '%Y-%m-%d')
			dt_now = datetime.now()
			
			if dt_mc.date() <= dt_now.date():
				return None

			dt_next = dt_now + timedelta(weeks=1)
			return dt_mc.date() == dt_next.date()
		return False
  
	def __normalize_date(self, date: str, number: int):
		if not date.isspace():
			dt = datetime.strptime(date, '%Y-%m-%d')
			dt += timedelta(weeks=number-1)
			return dt.strftime('%d.%m.%Y') + 'г.'
		return None

	def __get_subs(self):
		return [u for u in ChatBot.users() if u.is_subscriber()]

	def __get_groups(self):
		return [u for u in ChatBot.users() if u.is_group()]

	def __get_admins(self):
		return [u for u in ChatBot.users() if u.is_admin()]
			
# -------------------------------------------------------------------------