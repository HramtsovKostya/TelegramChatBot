# -------------------------------- PARSER ---------------------------------
 
import config as cnf
import gspread as gs
import json

from oauth2client.service_account import ServiceAccountCredentials as sac

# -------------------------------------------------------------------------

class SheetParser(object):
	def __init__(self):
		self.__scope = [
			cnf.GOOGLE_SHEETS_API,
			cnf.GOOGLE_DRIVE_API]

		self.__creds = sac.from_json_keyfile_name(
		cnf.CREDENTIALS_FILE, self.__scope)

		self.__client = gs.authorize(self.__creds)

	def get_data(self):
		sh = self.__client.open_by_key(cnf.SPREAD_SHEET_ID).sheet1
		self.__data = sh.get_all_records()
		return self.__data

	def save_json(self):
		with open(cnf.SPREAD_SHEET_FILE, 'w', encoding='utf-8') as f:
			json.dump(self.__data, f, indent=4, ensure_ascii=False)
		print('Данные успешно записаны!')

	def load_json(self):
		with open(cnf.SPREAD_SHEET_FILE, 'r', encoding='utf-8') as f:
			self.__data = json.load(f)
		print('Данные успешно прочтены!')
		return self.__data

	def to_str(self, data):
		return json.dumps(data, indent=4, ensure_ascii=False)

# -------------------------------------------------------------------------