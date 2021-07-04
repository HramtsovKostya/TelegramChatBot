# ------------------------------- CHAT-BOT --------------------------------

import config as cnf
import pandas as pd

from telebot import TeleBot
from telebot import types as ts

from model.subscribe import Subscriber, Role

# -------------------------------------------------------------------------

bot = TeleBot(cnf.TOKEN)

users = []
sheet = pd.DataFrame()

# -------------------------------------------------------------------------

def bot_name():
	return bot.get_me().first_name


def user_name(msg: ts.Message):
	user = msg.from_user
	return user.last_name + ' ' + user.first_name


def chat_id(msg: ts.Message):
	return msg.chat.id

# ------------------------------ HANDLERS ---------------------------------

@bot.message_handler(commands=['start'])
def __handle_start(msg: ts.Message):
	text = 'Добро пожаловать,' + user_name(msg)
	text += '!\nЯ <b>' + bot_name()
	text += '</b> -  бот, созданный для рассылки '
	text += 'уведомлений о предстоящих занятиях.'

	bot.send_message(chat_id(msg), text, 
		reply_markup=__get_keyboard(), parse_mode='html')


@bot.message_handler(commands=['help'])
def __handle_help(msg: ts.Message):
	text = '<b>Список команд</b>:\n/about - Описание чат-бота'
	text += '\n/authors - Список авторов проекта'
	text += '\n/help - Список доступных команд'
	text += '\n/start - Повторный запуск чат-бота'

	bot.send_message(chat_id(msg), text, parse_mode='html')


@bot.message_handler(commands=['about'])
def __handle_about(msg):
	text = '<b>О боте:</b>\n<i>' + bot_name()
	text += '</i> - это тестовый чат-бот, '
	text += 'который пока ни чего не умеет.\n'

	bot.send_message(chat_id(msg), msg, parse_mode='html')


@bot.message_handler(commands=['authors'])
def __handle_authors(msg: ts.Message):
	text = '<b>Главный разработчик:</b>\n'
	text += '❤️ Константин Храмцов @KhramtsovKostya\n'
	text += '\nПо всем вопросам и предложениям'
	text += ' пишите мне в личные сообщения.'

	bot.send_message(chat_id(msg), text, parse_mode='html')


@bot.message_handler(content_types=['text'])
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
		if len(users) > 0:
			text = '<b>Список пользователей:</b>\n'			
			for i in range(len(users)):
				text += '\t' + str(i+1)  + '.' 
				text += users[i].user_name + '\n'
		else:
			text = 'В списке нет ни одного пользователя.'
				
	bot.send_message(chat, text, parse_mode='html')

# -----------------------------------------------------------------------

def __get_keyboard():
	kb = ts.ReplyKeyboardMarkup(resize_keyboard=True)
	
	btn_login = ts.KeyboardButton('Регистрация')
	btn_users = ts.KeyboardButton('Список пользователей')
	btn_sheet = ts.KeyboardButton('Данные из таблицы')
	
	kb.add(btn_login, btn_users, btn_sheet)
	return kb

def __add_user(user: Subscriber):
	if user.exists(users):
		return 'Такой пользователь уже существует!'
	
	users.append(user)
	Subscriber.save(cnf.USERS_LIST_FILE)

	return 'Вы успешно зарегистрированы!'

# -----------------------------------------------------------------------