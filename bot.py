# ------------------------------- CHAT-BOT --------------------------------

import telebot as tb
from telebot import types as ts

from model.subscribe import Subscriber, Role
from model.schedule import BotScheduler
from parse.sheet_parser import SheetParser

# -------------------------------------------------------------------------

class ChatBot(object):   
	__USERS_FILE = ''
	__SHEET_FILE = ''
    
	def __init__(self, token: str, users_file: str, sheet_file: str):
		self.__bot = tb.TeleBot(token)
  
		__USERS_FILE = users_file
		__SHEET_FILE = sheet_file
  
		self.__users = Subscriber.load(__USERS_FILE)
		self.__sheet = SheetParser.load(__SHEET_FILE)
  
	@property
	def get_bot(self):
		return self.__bot

	@property
	def all_users(self):
		return self.__users

	@all_users.setter
	def all_users(self, users):
		self.__users = users
  
	@property
	def get_sheet(self):
		return self.__sheet	

	@property
	def bot_name(self):
		return self.__bot.get_me().first_name

	def user_name(self, msg: ts.Message):
		user = msg.from_user
		return user.last_name + ' '  + user.first_name

	def chat_id(self, msg: ts.Message):
		return msg.chat.id

# ------------------------------ HANDLERS ---------------------------------

	@get_bot.message_handler(commands=['start'])
	def __handle_start(self, msg: ts.Message):
		text = 'Добро пожаловать,' + self.user_name(msg) 
  		text += '!\nЯ <b>' + self.bot_name 
		text += '</b> -  бот, созданный для рассылки '
  		text += 'уведомлений о предстоящих занятиях.'
		
		self.get_bot.send_message(self.chat_id(msg), text, 
			reply_markup=self.__get_keyboard(), parse_mode='html')

	@get_bot.message_handler(commands=['help'])
	def __handle_help(self, msg: ts.Message):
		text = '<b>Список команд</b>:\n/about - Описание чат-бота'
		text += '\n/authors - Список авторов проекта'
		text += '\n/help - Список доступных команд'
		text += '\n/start - Повторный запуск чат-бота'

		self.get_bot.send_message(self.chat_id(msg), text, parse_mode='html')

	@get_bot.message_handler(commands=['about'])
	def __handle_about(self, msg):
		text = '<b>О боте:</b>\n<i>' + self.bot_name
  		text += '</i> - это тестовый чат-бот,'
		text += ' который пока ни чего не умеет.\n'

		self.get_bot.send_message(self.chat_id(msg), msg, parse_mode='html')

	@get_bot.message_handler(commands=['authors'])
	def __handle_authors(self, msg: ts.Message):
		text = '<b>Главный разработчик:</b>\n'
		text += '❤️ Константин Храмцов @KhramtsovKostya\n'
		text += '\nПо всем вопросам и предложениям'
		text += ' пишите мне в личные сообщения.'

		self.get_bot.send_message(self.chat_id(msg), text, parse_mode='html')

	@get_bot.message_handler(content_types=['text'])
	def __handle_text(self, msg: ts.Message):
		chat = self.chat_id(msg)
		text = 'Я не знаю что ответить 😥'
  
		all_users = self.all_users
		users_count = len(all_users)
	
		if msg.text == 'Регистрация':
			name = self.user_name(msg)
			user_role = Role.TEACHER
   
			if msg.chat.type == 'group':
				name = msg.chat.title
				user_role = Role.GROUP
           
			user = Subscriber(chat, name, role=user_role)
			text = self.__add_user(user)
	
		elif msg.text == 'Список пользователей':
			if users_count > 0:
				text = '<b>Список пользователей:</b>\n'			
				for i in range(users_count):
					text += '\t' + str(i+1)  + '.' 
					text += all_users[i].user_name + '\n'
			else:
				text = 'В списке нет ни одного пользователя.'
					
		self.get_bot.send_message(chat, text, parse_mode='html')

# -----------------------------------------------------------------------

	def __get_keyboard(self):
    		kb = ts.ReplyKeyboardMarkup(resize_keyboard=True)
		btn_login = ts.KeyboardButton('Регистрация')
		btn_users = ts.KeyboardButton('Список пользователей')
		btn_sheet = ts.KeyboardButton('Данные из таблицы')
		
		kb.add(btn_login, btn_users, btn_sheet)
		return kb

	def __add_user(self, user: Subscriber):
		text = 'Я не знаю что ответить 😥'
		users = self.all_users
		
		if user.exists(users):
			text = 'Такой пользователь уже существует!'
		else:
			users.append(user)
			Subscriber.save(ChatBot.__USERS_FILE)
			text = 'Вы успешно зарегистрированы!'
   
		return text

# -----------------------------------------------------------------------
