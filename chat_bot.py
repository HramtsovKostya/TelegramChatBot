# ------------------------------- CHAT-BOT --------------------------------

import config as cnf

from telebot import TeleBot
from telebot import types as ts

from subscribe import Subscriber, Role
from sheet_parser import SheetParser

# -------------------------------------------------------------------------

__bot = TeleBot(cnf.TOKEN)

# -------------------------------------------------------------------------

class ChatBot(object):      
	def __init__(self):
		ChatBot.__users = Subscriber.load(cnf.USERS_LIST_FILE)
		ChatBot.__sheet = SheetParser.load(cnf.SPREAD_SHEET_FILE)
     
	def start(self, bot):
		print("Бот успешно запущен!")  
		bot.polling(none_stop=True, timeout=20)  
		print("Бот остановлен!")
  
	@staticmethod
	def users():
		return ChatBot.__users

	@staticmethod
	def sheet():
		return ChatBot.__sheet

# -------------------------------------------------------------------------

def bot_name():
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

# TODO Почему-то не работает!
# @__bot.message_handler(content_types=['new_chat_members'])
# def __handle_new_user(msg: ts.Message):
#     text = hello_msg(msg, new_user_name(msg))
#     __bot.send_message(chat_id(msg), text,
# 		reply_markup=get_keyboard(), parse_mode='html')


@__bot.message_handler(commands=['start'])
def __handle_start(msg: ts.Message):
	text = hello_msg(msg, user_name(msg))
	__bot.send_message(chat_id(msg), text, 
		reply_markup=get_keyboard(), parse_mode='html')


@__bot.message_handler(commands=['help'])
def __handle_help(msg: ts.Message):
	text = '<b>Список команд</b>:\n/about - Описание чат-бота'
	text += '\n/authors - Список авторов проекта'
	text += '\n/help - Список доступных команд'
	text += '\n/start - Повторный запуск чат-бота'
	__bot.send_message(chat_id(msg), text, parse_mode='html')


# TODO При вызове бросается исключение!
# @__bot.message_handler(commands=['about'])
# def __handle_about(msg: ts.Message):
# 	text = '<b>О боте:</b>\n<i>' + bot_name()
# 	text += '</i> - это тестовый чат-бот, '
# 	text += 'который пока ни чего не умеет.\n'
# 	__bot.send_message(chat_id(msg), msg, parse_mode='html')


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
		text = add_user(user)

	elif msg.text == 'Список пользователей':
		if len(ChatBot.users()) > 0:
			text = '<b>Список пользователей:</b>\n'	
   		
			for i in range(len(ChatBot.users())):
				user = ChatBot.users()[i]

				text += '\t' + str(i+1)  + '. ' 
				text += user.user_name + ' ('
				text += user.user_role + ')\n'
		else:
			text = 'В списке нет ни одного пользователя.'
				
	__bot.send_message(chat, text, parse_mode='html')

# -----------------------------------------------------------------------

def hello_msg(msg: ts.Message, user_name: str):
    text = 'Добро пожаловать, ' + user_name + '!\nЯ <b>'
    text += bot_name() + '</b> -  бот, созданный для рассылки '
    text += 'уведомлений о предстоящих занятиях.'
    return text


def get_keyboard():
	kb = ts.ReplyKeyboardMarkup(resize_keyboard=True)
	
	btn_login = ts.KeyboardButton('Регистрация')
	btn_users = ts.KeyboardButton('Список пользователей')
	
	for btn in [btn_login, btn_users]:
		kb.add(btn)  
	return kb

def add_user(user: Subscriber):
	if user.exists(ChatBot.users()):
		return 'Вы уже зарегистрированы!'
	
	ChatBot.users().append(user)
	Subscriber.save(ChatBot.users(), cnf.USERS_LIST_FILE)
	return 'Вы успешно зарегистрированы!'

# -----------------------------------------------------------------------