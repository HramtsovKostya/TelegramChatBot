# ------------------------------- SUBSCRIBE -------------------------------

import pandas as pd
import json

from datetime import datetime as dt
from os import path

# -------------------------------------------------------------------------

class Role(object):
    __ROLES = ['Преподаватель', 'Группа', 'Администратор']
    TEACHER, GROUP, ADMIN = tuple(__ROLES)

    @staticmethod
    def roles() -> list:
        return Role.__ROLES

# -------------------------------------------------------------------------

class Status(object):
    __STATUSES = ['Гость', 'Подписчик']
    GUEST, SUBSCRIBER = tuple(__STATUSES)

    @staticmethod
    def statuses() -> list:
        return Status.__STATUSES

# -------------------------------------------------------------------------

class UserKey(object):
    __USER_KEYS = [
        'Идентификатор чата', 
        'Имя пользователя', 
        'Роль пользователя',
        'Статус подписки', 
        'Дата регистрации'
    ]

    CHAT_ID, USER_NAME, ROLE, STATUS, REG_DATE = tuple(__USER_KEYS)

    @staticmethod
    def user_keys() -> list:
        return UserKey.__USER_KEYS

# -------------------------------------------------------------------------

class User(object):
    def __init__(self, chat_id: int, name: str,
        role    : str   = Role.TEACHER,
        status  : str   = Status.SUBSCRIBER,
        date    : str   = dt.now().strftime('%d.%m.%Y %H:%M')):  

        self.__chat_id      = chat_id
        self.__user_name    = name
        self.__user_role    = role
        self.__user_status  = status
        self.__reg_date     = date
   
    @property
    def chat_id(self) -> int:
        return self.__chat_id    

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def user_role(self) -> str:
        return self.__user_role    

    @property
    def user_status(self) -> str:
        return self.__user_status    

    @property
    def reg_date(self) -> str:
        return self.__reg_date    

    @user_role.setter
    def user_role(self, role: str):
        if role in Role.roles():
            self.__user_role = role     

    @user_status.setter
    def user_status(self, status: str):
        if status in Status.statuses():
            self.__user_status = status                

    def to_dict(self) -> dict:
        return {
            UserKey.CHAT_ID    : self.chat_id,
            UserKey.USER_NAME  : self.user_name,
            UserKey.ROLE       : self.user_role,
            UserKey.STATUS     : self.user_status,
            UserKey.REG_DATE   : self.reg_date
        }

    @classmethod
    def from_dict(init, data: dict):
        return init(
            chat_id = data[str(UserKey.CHAT_ID)],
            name    = data[UserKey.USER_NAME],
            role    = data[UserKey.ROLE],
            status  = data[UserKey.STATUS],
            date    = data[UserKey.REG_DATE]
        )

    @staticmethod
    def to_df(users: list) -> pd.DataFrame:
        return pd.DataFrame(
            columns = UserKey.user_keys(),
            data    = [u.to_dict() for u in users]
        )    
    
    @staticmethod
    def save(users: list, file_name: str):
        df_users = User.to_df(users)
        df_users.to_csv(file_name, sep=';')

    @staticmethod
    def load(file_name: str) -> list:
        users = []
        if path.exists(file_name):
            df_users = pd.read_csv(file_name, delimiter=';')
            users = [User.from_dict(row) for i, row in df_users.iterrows()] 
        return users    

    def exists(self, users: list) -> bool:
        
        df = User.to_df(users)        
        id_found = (df[str(UserKey.CHAT_ID)] == self.chat_id).any()
        name_found = (df[UserKey.USER_NAME] == self.user_name).any()
        return id_found or name_found
       
    def __str__(self) -> str:
        data = self.to_dict()
        return json.dumps(data, indent=4, ensure_ascii=False)

# -------------------------------------------------------------------------