# ------------------------------- CHAT-BOT --------------------------------

import config as cnf
import pandas as pd

from telebot import TeleBot
from telebot import types as ts
from subscribe import Subscriber, Role

# -------------------------------------------------------------------------

__bot = TeleBot(cnf.TOKEN)

# -------------------------------------------------------------------------

class ChatBot(object):      
	def __init__(self, users: list, sheet: pd.DataFrame):
		ChatBot.__users = users
		ChatBot.__sheet = sheet

	def start(self, bot):
		print("Чат-бот успешно запущен!\n")  
		bot.polling(none_stop=True, timeout=20)  
		print("\nЧат-бот успешно остановлен!")

	@staticmethod
	def users():
		return ChatBot.__users

	@staticmethod
	def sheet():
		return ChatBot.__sheet

# -------------------------------------------------------------------------

def get_bot_name():
	return __bot.get_me().first_name


def user_name(msg: ts.Message):
	user = msg.from_user
	return user.last_name + ' ' + user.first_name


def new_user_name(msg: ts.Message): 
	user = msg.new_chat_members[0]
	return user.last_name + ' ' + user.first_name
 
 
def group_name(msg: ts.Message):
	return msg.chat.first_name


def chat_id(msg: ts.Message):
	return msg.chat.id

# ------------------------------ HANDLERS ---------------------------------

@__bot.message_handler(commands=['start'])
def __handle_start(msg: ts.Message):
	text = 'Добро пожаловать, ' + user_name(msg) + '!\n\nЯ <b>'
	text += get_bot_name() + '</b> - бот, созданный для рассылки '
	text += 'уведомлений о предстоящих занятиях.'
	__bot.send_message(chat_id(msg), text, 
		reply_markup=__get_keyboard(), parse_mode='html')


@__bot.message_handler(commands=['help'])
def __handle_help(msg: ts.Message):
	text = '<b>Список команд</b>:\n/about - Описание чат-бота'
	text += '\n/authors - Список авторов проекта'
	text += '\n/help - Список доступных команд'
	text += '\n/start - Повторный запуск чат-бота'
	__bot.send_message(chat_id(msg), text, parse_mode='html')


@__bot.message_handler(commands=['about'])
def __handle_about(msg: ts.Message):
	text = '<b>О боте:</b>\n<i>' + get_bot_name()
	text += '</i> - это тестовый чат-бот, '
	text += '\nкоторый пока ни чего не умеет.\n'
	__bot.send_message(chat_id(msg), text, parse_mode='html')


@__bot.message_handler(commands=['authors'])
def __handle_authors(msg: ts.Message):
	text = '<b>Главный разработчик:</b>\n'
	text += '❤️ Константин Храмцов @KhramtsovKostya\n'
	text += '\nПо всем вопросам и предложениям'
	text += '\nпишите мне в личные сообщения.'
	__bot.send_message(chat_id(msg), text, parse_mode='html')


@__bot.message_handler(content_types=['text'])
def __handle_text(msg: ts.Message):
	chat = chat_id(msg)
	text = 'Я не знаю что ответить 😥'

	if msg.text == 'Регистрация':
		name = user_name(msg)
		user_role = Role.TEACHER

		if msg.chat.type == 'group':
			name = msg.chat.title
			user_role = Role.GROUP
		
		user = Subscriber(chat, name, role=user_role)
		text = __add_user(user)

	elif msg.text == 'Список пользователей':
		if len(ChatBot.users()) > 0:
			text = '<b>Список пользователей:</b>\n'	

			for i in range(len(ChatBot.users())):
				user = ChatBot.users()[i]

				text += '\t' + str(i+1)  + '. ' 
				text += user.user_name + ' (' + user.user_role + ')\n'
		else:
			text = 'В списке нет ни одного пользователя.'
				
	__bot.send_message(chat, text, parse_mode='html')

# -----------------------------------------------------------------------

def __get_keyboard():
	kb = ts.ReplyKeyboardMarkup(resize_keyboard=True)
	
	btn_login = ts.KeyboardButton('Регистрация')
	btn_users = ts.KeyboardButton('Список пользователей')
	
	for btn in [btn_login, btn_users]:
		kb.add(btn)  
	return kb


def __add_user(user: Subscriber):
	users = ChatBot.users()
	if user.exists(users):
		return 'Вы уже зарегистрированы!'
	
	users.append(user)
	Subscriber.save(users, cnf.USERS_LIST_FILE)
	
	return 'Вы успешно зарегистрированы!'

# -----------------------------------------------------------------------