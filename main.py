import constants
from patterns.weather_bot.weather_bot import keep_alive, execute
import pip

pip.main(['install', 'pytelegrambotapi'])
import telebot

bot = telebot.TeleBot(constants.TOKEN)


def send_message(message):
    if message.text == '/start' and len(constants.START_MESSAGE) != 0:
        bot.send_message(message.from_user.id, constants.START_MESSAGE)
    else:
        execute(bot, message)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    send_message(message)

keep_alive()
bot.polling(non_stop=True, interval=0)
