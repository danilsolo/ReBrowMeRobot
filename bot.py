#coding:utf-8
import telebot
import sqlite3
import logging
import random
import time
import datetime
from telebot import types
import botparts


logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)-3s]# %(levelname)-5s [%(asctime)s] %(message)s'
                    , level=logging.INFO)


bot = telebot.TeleBot(botparts.token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    logging.debug(botparts.niceprint(message))
    userid = message.from_user.id
    username = message.from_user.username

    logging.info('user: ' + str(username) + ' command: /start')
    bot.send_message(message.chat.id
                     , 'Привет, {}. Я бот сети студий татуажа ReBrowme. Задайте мне ваш вопрос, я помогу'.format(message.from_user.first_name)
                     , reply_markup=botparts.userkeyboard)


@bot.message_handler(func=lambda message: message.text and 'Вопросы' in message.text, content_types=['text'])
def go(message):
    logging.info('user: ' + str(message.from_user.username) + ' позвал')
    out = botparts.allquestions
    msg = bot.send_message(message.chat.id, out, reply_markup=botparts.questionkeyboard)
    for i in botparts.questions:
        print(i + '. ' + botparts.questions[i]['question'])


@bot.message_handler(func=lambda message: message.text and 'Записаться' in message.text, content_types=['text'])
def go(message):
    logging.info('user: ' + str(message.from_user.username) + ' записаться')
    bot.send_message(message.chat.id, 'Выберите ваш город', reply_markup=botparts.signupkeyboard)


@bot.callback_query_handler(func=lambda call: call.data in botparts.towns)
def inlin(call):
    logging.info(botparts.niceprint(call))
    logging.info(call.data)

    town = call.data
    address = botparts.towns[call.data]
    out = '{}, в городе {} вы можете записаться по адресу {}, позвонив по номеру 8(800)555-59-18'\
        .format(call.from_user.first_name, town, address)
    bot.edit_message_text(out, call.message.chat.id, call.message.message_id
                          , parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data in botparts.questions)
def inlin(call):
    logging.info(botparts.niceprint(call))
    logging.info(call.data)
    bot.edit_message_text(botparts.questions[call.data]['answer'], call.message.chat.id, call.message.message_id
                          , reply_markup=botparts.questionbackkeyboard)

@bot.callback_query_handler(func=lambda call: call.data=='back')
def inlin(call):
    logging.debug(botparts.niceprint(call))
    logging.debug(call.data)
    bot.edit_message_text(botparts.allquestions, call.message.chat.id, call.message.message_id
                          , reply_markup=botparts.questionkeyboard)


bot.polling()