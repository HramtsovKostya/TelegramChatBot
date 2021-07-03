# --------------------------------- MAIN ----------------------------------

import config as cnf
import pandas as pd
from datetime import datetime, timedelta
from parse.sheet_parser import SheetParser

# -------------------------------------------------------------------------

def get_by_name(df: pd.DataFrame, name: str):
    for i, row in df.iterrows():
        if row['Преподаватель'] == name:
            return row
    return None


def is_next_week(date: str):
    is_equals = (False, 0)
    
    for week in range(12):
        dt = datetime.strptime(date, '%Y-%m-%d') + timedelta(weeks=week)
        dt_next = datetime.now() + timedelta(weeks=1)
        
        if dt.date() == dt_next.date():
            is_equals = (True, week+1)
            break
        
    return is_equals

def normalize_date(date: str, number: int):
    dt = datetime.strptime(date, '%Y-%m-%d') + timedelta(weeks=number-1)
    return dt.strftime('%d.%m.%Y') + 'г.'


if __name__ == '__main__':
    # parser = SheetParser(
	# 	file_name=cnf.CREDENTIALS_FILE, 
    #     scopes=[cnf.GOOGLE_SHEETS_API, cnf.GOOGLE_DRIVE_API]
    # )

    # df = parser.get(cnf.SPREAD_SHEET_ID)
    # SheetParser.save(df, cnf.SPREAD_SHEET_FILE)
    
    df = SheetParser.load(cnf.SPREAD_SHEET_FILE)  
      
    date = get_by_name(df, 'Храмцов Константин')       
    is_equals, week = is_next_week(date['Дата начала курса'])
    
    if date is not None and is_equals:
        module = week // 4 if week % 4 == 0 else week // 4 + 1
        lesson = week % 4 if week % 4 > 0 else 4 
                
        message = 'Добрый день, ' +  date['Преподаватель'] + '! '
        message += 'Спешу вас уведомить, что через неделю, а именно '
        message += normalize_date(date['Дата начала курса'], week) + ', у ' 
        message += str(date['Поток курса']) + '-го потока курса "'
        message += date['Название курса']  + '" пройдет ' +  str(lesson)
        message += '-e занятие ' + str(module) + '-го модуля. '
        message += 'Место и время проведения: ' + date['Место проведения']
        message += ', c ' + date['Время проведения'].replace('-', ' до ')  + '.' 
        print(message)
    else:
        print('На сегодня уведомлений нет!')
    
# -------------------------------------------------------------------------