# ------------------------------- SCHEDULE --------------------------------

import pandas as pd
import schedule as sch
import threading as thr
import time

from datetime import datetime, timedelta

# -------------------------------------------------------------------------

class BotScheduler(object):	
	def __init__(self, data: pd.DataFrame):
		self.__is_working = True
		self.__data_frame = data
  
	def start(self):
		thread = thr.Thread(target=self.__schedule)
		thread.start()
		print('Расписание запущено!')

	def stop(self):
		self.__is_working = False
		print('Расписание остановлено!')
  
	def __schedule(self):
		name = 'Храмцов Константин'
		sch.every(1).minutes.do(self.__notify, name)

		while self.__is_working:
			sch.run_pending()
			time.sleep(3)

	def __notify(self, name: str):     
		text = 'На сегодня уведомлений нет!'
  
		data = self.__get_by_name(self.__data_frame, name)
		is_equals, week = self.__next_week(data['Дата начала курса'])

		if data != None and is_equals:
			text = self.__get_notification(week, data)
			
		print(text)

	def __get_notification(self, week: int, data: pd.DataFrame):
		lesson = week % 4 if week % 4 > 0 else 4 
		module =  week // 4 if week % 4 == 0 else week // 4 + 1

		text = 'Добрый день, ' +  data['Преподаватель'] + '! '
		text += 'Спешу вас уведомить, что через неделю, а именно '
		text += self.__normalize_date(data['Дата начала курса'], week) + ', у '
		text += str(data['Поток курса']) + '-го потока курса "'
		text += data['Название курса']  + '" пройдет ' +  str(lesson)
		text += '-e занятие ' + str(module) + '-го модуля. '
		text += 'Место и время проведения: ' + data['Место проведения']
		text += ', c ' + data['Время проведения'].replace('-', ' до ')  + '.'
		
		return text
  
	def __get_by_name(self, df: pd.DataFrame, name: str):
		for i, row in df.iterrows():
			if row['Преподаватель'] == name:
				return row
		return None

	def __next_week(self, date: str):
		is_equals = (False, 0)
		
		for week in range(12):
			dt = datetime.strptime(date, '%Y-%m-%d') + timedelta(weeks=week)
			dt_next = datetime.now() + timedelta(weeks=1)
			
			if dt.date() == dt_next.date():
				is_equals = (True, week+1)
				break  
		return is_equals

	def __normalize_date(self, date: str, number: int):
		dt = datetime.strptime(date, '%Y-%m-%d') + timedelta(weeks=number-1)
		return dt.strftime('%d.%m.%Y') + 'г.'

# -------------------------------------------------------------------------