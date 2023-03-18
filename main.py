import telebot
from telebot import types

bot = telebot.TeleBot('5860281367:AAGmZCTEvrJRXPLOV8bXGtf4JMlwNKir_YU')

@bot.message_handler(commands = ['start'])
@bot.message_handler(commands = ['balance'])

def start(message):
    bot.send_message(message.chat.id, 'Привет! Добро пожаловать в НикольКредитБанк!')

def balance(message):
	bot.send_message(message.chat.id, 'Доступных пятерок на балансе:')

bot.polling(non_stop = True)