# ------------------------------- CHAT-BOT --------------------------------

import config as cnf
import telebot as tb
import pandas as pd

from model.schedule import BotScheduler
from model.subscribe import Subscriber
from model.subscribe import Role
from parse.sheet_parser import SheetParser
from telebot import types as ts

# -------------------------------------------------------------------------

bot = tb.TeleBot(cnf.TOKEN)
df_sheet = pd.DataFrame()
all_users = []

# ------------------------------- START -----------------------------------

@bot.message_handler(commands=['start'])
def handle_start(message):
	user_name = message.from_user.first_name
	bot_name = bot.get_me().first_name

	keyboard = ts.ReplyKeyboardMarkup(resize_keyboard=True)
	btn_login = ts.KeyboardButton('Регистрация')
	btn_users = ts.KeyboardButton('Список пользователей')
	btn_sheet = ts.KeyboardButton('Данные из таблицы')
	
	for btn in [btn_login, btn_users, btn_sheet]:
		keyboard.add(btn)

	bot_message = f"Добро пожаловать, {user_name}!\nЯ - <b>{bot_name}</b>"
	bot_message += ", бот созданный быть подопытным кроликом."
	
	bot.send_message(message.chat.id, bot_message, 
		parse_mode='html', reply_markup=keyboard)

# -------------------------------- HELP -----------------------------------

@bot.message_handler(commands=['help'])
def handle_help(message):
	bot_message = "<b>Список команд</b>:\n/about - Описание чат-бота"
	bot_message += "\n/authors - Список авторов проекта"
	bot_message += "\n/help - Список доступных команд"
	bot_message += "\n/start - Повторный запуск чат-бота"

	bot.send_message(message.chat.id, bot_message, parse_mode='html')

# -------------------------------- ABOUT ----------------------------------

@bot.message_handler(commands=['about'])
def handle_about(message):
	bot_name = bot.get_me().first_name

	bot_message = f"<b>О боте:</b>\n<i>{bot_name}</i> - это тестовый чат-бот,"
	bot_message += " который пока ни чего не умеет.\n"

	bot.send_message(message.chat.id, bot_message, parse_mode='html')

# ------------------------------ AUTHORS ----------------------------------

@bot.message_handler(commands=['authors'])
def handle_authors(message):
	bot_message = "<b>Главный разработчик:</b>\n"
	bot_message += "❤️ Константин Храмцов @KhramtsovKostya\n"
	bot_message += "\nПо всем вопросам и предложениям"
	bot_message += " пишите мне в личные сообщения."
	bot_message += " Буду рад НЕ ответить. 😈"

	bot.send_message(message.chat.id, bot_message, parse_mode='html')

# ------------------------------- TEXT -----------------------------------

@bot.message_handler(content_types=['text'])
def handle_text(message):  # sourcery no-metrics
	if message.chat.type == 'private':
		if message.text == "Регистрация":
			first_name = message.from_user.first_name
			last_name = message.from_user.last_name

			add_user(Subscriber(message.chat.id, first_name + ' ' + last_name))
		elif message.text == "Данные из таблицы":
			pass		
		elif message.text == "Список пользователей":
			if len(all_users) > 0:
				cur_user = [u for u in all_users if u.chat_id == message.chat.id][0]

				if cur_user.user_role == Role.ADMIN:
					bot_message = '<b>Список пользователей:</b>\n'			
					for i in range(len(all_users)):
						bot_message += f'\t{i+1}. {all_users[i].user_name}\n'
					bot.send_message(message.chat.id, bot_message, parse_mode='html')
				else:
					bot.send_message(message.chat.id, 'У вас недостаточно прав доступа!')
			else:
				bot.send_message(message.chat.id, 'Вы забыли зарегистрироваться!')
		else:
			bot.send_message(message.chat.id, "Я не знаю что ответить 😥")

	elif message.chat.type == 'group':
		if message.text == "Регистрация":
			add_user(Subscriber(message.chat.id, message.chat.title, role=Role.GROUP))			
		elif message.text == "Данные из таблицы":
			pass
		elif message.text == "Список пользователей": 
			bot.send_message(message.chat.id, "Данная команда недоступна!")
		else:
			bot.send_message(message.chat.id, "Я не знаю что ответить 😥")

# -----------------------------------------------------------------------

def add_user(user: Subscriber):
	users = Subscriber.load(cnf.USERS_LIST_FILE)
	
	if user.exists(users):
		bot.send_message(user.chat_id, 'Такой пользователь уже существует!')
	else:
		all_users.append(user)
		Subscriber.save(all_users, cnf.USERS_LIST_FILE)
		bot.send_message(user.chat_id, 'Вы успешно зарегистрированы!')

# --------------------------- RUN CHAT-BOT ------------------------------

if __name__ == '__main__':
	all_users = Subscriber.load(cnf.USERS_LIST_FILE)
	df_sheet = SheetParser.load(cnf.SPREAD_SHEET_FILE)

	# parser = SheetParser(
	# 	cnf.CREDENTIALS_FILE, [
	# 	cnf.GOOGLE_SHEETS_API,
	# 	cnf.GOOGLE_DRIVE_API
	# ])

	# df_sheet = parser.get(cnf.SPREAD_SHEET_ID, head=3)
	# SheetParser.save(df_sheet, cnf.SPREAD_SHEET_FILE)

	scheduler = BotScheduler(bot)
	scheduler.start()
	
	print("Бот успешно запущен!")
	bot.polling(none_stop=True, timeout=20)

	print("Бот остановлен!")
	scheduler.stop()

# -----------------------------------------------------------------------
