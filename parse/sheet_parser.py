# -------------------------------- PARSER ---------------------------------
 
import gspread as gs
import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials
from os import path

# -------------------------------------------------------------------------

class SheetParser(object):
	def __init__(self, scope: list[str], key: str):
		creds = ServiceAccountCredentials.from_json_keyfile_name(key, scope)
		self.__client = gs.authorize(creds)

	def get(self, sheet_id: str, index: int = 0, head: int = 1) -> pd.DataFrame:
		wb = self.__client.open_by_key(sheet_id)
		sheet = wb.get_worksheet(index)
		data = sheet.get_all_records(head=head)
		return pd.DataFrame(data, columns=data[0].keys())

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