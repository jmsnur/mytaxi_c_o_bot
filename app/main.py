import telebot
from telebot import types
from secret_config import BOTTOKEN

from db import *
from functions import *


TOKEN = BOTTOKEN
bot = telebot.TeleBot(TOKEN)


date_regex = r"^(20|21)[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"
date_m2_regex = r"^[+](20|21)[0-9]{2}-(0[1-9]|1[0-2])$"
date_interval_regex = r"^(20|21)[0-9]{2}/(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|3[0-1])-(20|21)[0-9]{2}/(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|3[0-1])$"


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    msg = 'Hello! Below the list of information that I can show.\n'
    msg +='TASK1: Canceled orders grouped by regions in one exact date\n'
    msg +='TASK2: Detailed statististics of requested month\n'
    msg +='TASK3: More precise count of canceled orderes grouped by client_id of requested period\n' 
    msg +='\nFOR TASK1: \'YYYY-MM-DD\' \ne.g.: 2019-04-04\nFOR TASK2: \'+YYYY-MM\' \ne.g.: +2019-04 \nFOR TASK3: \'YYYY/MM/DD-YYYY/MM/DD\' \ne.g.: 2019/04/04-2019/06/30'
    bot.send_message(chat_id, msg)
    return


@bot.message_handler(regexp=date_regex)
def task_1(message):
    chat_id = message.chat.id
    date = message.text
    msg = get_day_cancel(date)
    bot.send_message(chat_id, msg)
    return


@bot.message_handler(regexp=date_m2_regex)
def task_2(message):
    chat_id = message.chat.id
    date_m = message.text[1:]
    msg = month_stat(date_m)
    bot.send_message(chat_id, msg)
    return


@bot.message_handler(regexp=date_interval_regex)
def task_3(message):
    chat_id = message.chat.id
    date_interval = message.text
    msg = get_interval_stat(date_interval)
    bot.send_message(chat_id, msg)
    return



@bot.message_handler(content_types=['text'])
def recommendation(message):
    chat_id = message.chat.id
    msg ='FOR TASK1: \'YYYY-MM-DD\' \ne.g.: 2019-04-04\nFOR TASK2: \'+YYYY-MM\' \ne.g.: +2019-04 \nFOR TASK3: \'YYYY/MM/DD-YYYY/MM/DD\' \ne.g.: 2019/04/04-2019/06/30'
    bot.send_message(chat_id, msg)
    return


if __name__ == "__main__":
    bot.polling(None)
