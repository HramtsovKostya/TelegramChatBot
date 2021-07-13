# ------------------------------- CHAT-BOT --------------------------------

import config as cfg
import pandas as pd

from telebot import TeleBot
from telebot import types as ts
from subscribe import Subscriber
from subscribe import Role, Status

# -------------------------------------------------------------------------

__bot = TeleBot(cfg.TOKEN)

# -------------------------------------------------------------------------

class ChatBot(object):      
	def __init__(self, users: list, sheet: pd.DataFrame):
		ChatBot.__users = users
		ChatBot.__sheet = sheet
		ChatBot.__role = ''

	def start(self, bot):
		print("Чат-бот успешно запущен!\n")  
		bot.polling(none_stop=True, timeout=20)  
		print("\nЧат-бот успешно остановлен!")

	@staticmethod
	def users():
		return ChatBot.__users

	@staticmethod
	def get_by_id(id: int) -> Subscriber:
		for user in ChatBot.users():
			if user.chat_id == id:
				return user
		return None

	@staticmethod
	def sheet():
		return ChatBot.__sheet

	@staticmethod
	def get_role():
		return ChatBot.__role

	@staticmethod
	def set_role(role: str):
		ChatBot.__role = role

# -------------------------------------------------------------------------

def get_bot_name():
	return __bot.get_me().first_name


def user_name(msg: ts.Message):
	user = msg.from_user
	return user.last_name + ' ' + user.first_name

# ------------------------------ HANDLERS ---------------------------------

@__bot.message_handler(commands=['start'])
def __handle_start(msg: ts.Message):
	text = 'Добро пожаловать, ' + user_name(msg) + '!\n\nЯ <b>'
	text += get_bot_name() + '</b> - бот, созданный для рассылки '
	text += 'уведомлений о предстоящих занятиях.'
 
	__bot.send_message(msg.chat.id, text, 
		reply_markup=__start_kb(msg.chat.type), parse_mode='html')


@__bot.message_handler(commands=['help'])
def __handle_help(msg: ts.Message):
	text = '<b>Список команд</b>:\n/about - Описание чат-бота'
	text += '\n/authors - Список авторов проекта'
	text += '\n/help - Список доступных команд'
	text += '\n/start - Повторный запуск чат-бота'
	__bot.send_message(msg.chat.id, text, parse_mode='html')


@__bot.message_handler(commands=['about'])
def __handle_about(msg: ts.Message):
	text = '<b>О боте:</b>\n<i>' + get_bot_name()
	text += '</i> - это тестовый чат-бот, '
	text += '\nкоторый пока ни чего не умеет.\n'
	__bot.send_message(msg.chat.id, text, parse_mode='html')


@__bot.message_handler(commands=['authors'])
def __handle_authors(msg: ts.Message):
	text = '<b>Главный разработчик:</b>\n'
	text += 'Константин Храмцов @KhramtsovKostya\n'
	text += '\nПо всем вопросам и предложениям'
	text += '\nпишите мне в личные сообщения.'
	__bot.send_message(msg.chat.id, text, parse_mode='html')


@__bot.message_handler(content_types=['text'])
def __handle_text(msg: ts.Message):  # sourcery no-metrics
	chat_id = msg.chat.id

	if msg.text == 'Регистрация':
		text = 'Выберите роль, в качестве которой'
		text += ' хотите зарегистрироваться'

		__bot.send_message(chat_id, text, 
			reply_markup=__select_role_kb(msg.chat.type))

	elif msg.text == 'Статус подписки':
		if msg.chat.type == 'private':
			text = 'Вы до сих пор не зарегистрировались!'

			if len(ChatBot.users()) > 0:      
				user = ChatBot.get_by_id(msg.from_user.id)

				if user is not None:
					kb = ts.InlineKeyboardMarkup()
					kb.add(__get_btn('Меня всё устраивает'))

					if user.user_status == Status.SUBSCRIBER:
						text = 'Подписка на рассылку уведомлений <i>активна</i>!'
						btn_sub = ts.InlineKeyboardButton(
							text='Отписаться', callback_data=Status.GUEST)
					else:
						text = 'Подписка на рассылку уведомлений <i>не активна</i>!'
						btn_sub = ts.InlineKeyboardButton(
							text='Подписаться', callback_data=Status.SUBSCRIBER)
					kb.add(btn_sub)
	
					__bot.send_message(chat_id, text, 
						reply_markup=kb, parse_mode='html')
				else:
					__bot.send_message(chat_id, text)	
			else:
				__bot.send_message(chat_id, text)

		elif msg.chat.type == 'group':
			text = 'Я не знаю, что ответить'
			__bot.send_message(chat_id, text)

	elif msg.text == 'Пользователи':
		text = 'Я не знаю, что ответить'		
  
		if msg.chat.type == 'private':
			text = 'Вы до сих пор не зарегистрировались!'
		
			if len(ChatBot.users()) > 0:
				user = ChatBot.get_by_id(msg.from_user.id)

				if user is not None:  
					if user.is_admin():
						text = '<b>Список пользователей:</b>\n'	

						for i in range(len(ChatBot.users())):
							user = ChatBot.users()[i]
							text += '\t' + str(i+1)  + '. ' 
							text += user.user_name + ' (' + user.user_role + ')\n'
					else:
						text = 'Вам отказано в доступе! Список пользователей'
						text += ' могут просматривать только администраторы!'
	
		__bot.send_message(chat_id, text, parse_mode='html')
	
	else:
		text = 'Я не знаю, что ответить'
		__bot.send_message(chat_id, text)


@__bot.callback_query_handler(
	func=lambda call: call.data in Role.roles())
def __register_callback(call: ts.CallbackQuery):
	chat = call.message.chat
	user_role = call.data
 
	__bot.edit_message_reply_markup(chat.id, 
		message_id=call.message.id, reply_markup='')
 
	name = user_name(call)
	user_id = call.from_user.id

	if user_role == Role.GROUP:
		name = chat.title
		user_id = chat.id

	user = Subscriber(user_id, name, role=user_role)
	text = __add_user(user)
 
	__bot.edit_message_text(text, chat_id=chat.id,
		message_id=call.message.id, parse_mode='html')


@__bot.callback_query_handler(
	func=lambda call: call.data in Status.statuses())
def __subscribe_callback(call: ts.CallbackQuery):
	chat = call.message.chat
	status = call.data

	__bot.edit_message_reply_markup(chat.id, 
		message_id=call.message.id, reply_markup='')
 
	user = ChatBot.get_by_id(call.from_user.id)
	user.user_status = status
 
	text = 'Вы успешно <i>подписались</i> на рассылку уведомлений!'
	
	if status == Status.GUEST:
		text = 'Вы успешно <i>отписались</i> от рассылки уведомлений!'
 
	Subscriber.save(ChatBot.users(), cfg.USERS_LIST_FILE)
 
	__bot.edit_message_text(text, chat_id=chat.id,
		message_id=call.message.id, parse_mode='html')
 
@__bot.callback_query_handler(
	func=lambda call: call.data == 'Меня всё устраивает')
def __cancel_callback(call: ts.CallbackQuery):
	chat = call.message.chat

	__bot.edit_message_reply_markup(chat.id, 
		message_id=call.message.id, reply_markup='')
	
	user = ChatBot.get_by_id(call.from_user.id)
	text = 'Вы по-прежнему <i>подписаны</i> на рассылку уведомлений'
 
	if user.user_status == Status.GUEST:
		text = 'Вы по-прежнему <i>не подписаны</i> на рассылку уведомлений'
 
	__bot.edit_message_text(text, chat_id=chat.id,
		message_id=call.message.id, parse_mode='html')

# -----------------------------------------------------------------------

def __start_kb(chat_type: str):
	kb = ts.ReplyKeyboardMarkup(resize_keyboard=True)
	
	btn_login = ts.KeyboardButton('Регистрация')
	kb.add(btn_login)
 
	if chat_type == 'private':
		btn_sub = ts.KeyboardButton('Статус подписки')
		kb.add(btn_sub)
	
		btn_users = ts.KeyboardButton('Пользователи')
		kb.add(btn_users)
 
	return kb


def __select_role_kb(chat_type: str):
	kb = ts.InlineKeyboardMarkup()
 
	kb.add(__get_btn(Role.TEACHER))
	kb.add(__get_btn(Role.ADMIN))
 
	if chat_type == 'group':
		kb.add(__get_btn(Role.GROUP))
 
	return kb


def __get_btn(text: str):
	return ts.InlineKeyboardButton(text=text, callback_data=text)


def __add_user(user: Subscriber):
	users = ChatBot.users()
	name = user.user_name
 
	text = f'Вы успешно зарегистрированы как <b>{name}</b>!'
 
	if user.is_group():
		text = f'Группа <b>{name}</b> успешно зарегистрирована!'
 
	if user.exists(users):		
		text = text.replace('успешно', 'уже')		
	else:
		users.append(user)
		Subscriber.save(users, cfg.USERS_LIST_FILE)
	
	return text

# -----------------------------------------------------------------------