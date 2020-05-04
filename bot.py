import telebot
import os

bot = telebot.TeleBot(os.environ['MYFUNKYBOT_API'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if('arepas' in message.text):
        bot.reply_to(message, 'claro q si papa')


bot.polling()
