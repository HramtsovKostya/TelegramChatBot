# -------------------------------- PARSER ---------------------------------
 
from datetime import datetime
import gspread as gs
import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials as sac 
from os import path

# -------------------------------------------------------------------------

class SheetParser(object):
	def __init__(self, file_name: str, scopes: str):
		creds = sac.from_json_keyfile_name(file_name, scopes)
		self.__client = gs.authorize(creds)

	def get(self, sheet_id: str, index: int = 0, head: int = 1):
		wb = self.__client.open_by_key(sheet_id)
		sheet = wb.get_worksheet(index)
		records = sheet.get_all_records(head=head)
		data = self.__get_data(records[1:])
  
		return pd.DataFrame(data, columns=data[0].keys())

	def __get_data(self, records):
		return [{
				'Название курса'	: item['ПолнНаим'],
    			'Преподаватель'		: self.__to_name(item['Преподаватель']),
				'Поток курса'		: int(item['Поток']),
				'Стадия курса'		: item['Стадия'],
				'Место проведения'	: item['Площадка'],
				'Мастер-класс'		: self.__to_date(item['МК']),
				'Дата начала курса'	: self.__to_date(item['НАЧАЛО']),
				'Время проведения'	: self.__to_time(item['Время'])
    		} for item in records]
  
	def __to_name(self, record: str):
		name = ''
     
		if record != '' and not record.isspace(): 
			first_name, last_name = tuple(record.split(' ')[:2])
			name = last_name + ' ' + first_name

		return name
  
	def __to_date(self, record: str):
		date = ''

		if record != '' and not record.isspace(): 
			MONTH_NAMES = [
				'янв.', 'февр.', 'мар.',
				'апр.', 'мая', 'июн.', 
				'июл.', 'авг.', 'сент.',
				'окт.', 'нояб.', 'дек.'
			]

			day, month = tuple(record.split(' ')[:2])
			day = '0' + day if int(day) < 10 else day

			index = str(MONTH_NAMES.index(month) + 1)
			month = '0' + index if int(index) < 10 else index

			str_date = day + '.' + month + '.21'
			date = datetime.strptime(str_date, '%d.%m.%y')
  
		return date

	def __to_time(self, record: str):
		time = ''  		
		if record != '' and not record.isspace():
			time = record.split(' ')[1]   
		return time
      
	@staticmethod
	def save(df: pd.DataFrame, file_name: str):
		df.to_csv(file_name, sep=';')

	@staticmethod
	def load(file_name: str) -> pd.DataFrame:
		df_sheet = pd.DataFrame()
		if path.exists(file_name):
			df_sheet = pd.read_csv(file_name, delimiter=';')
		return df_sheet

# -------------------------------------------------------------------------