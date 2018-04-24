#coding:utf-8
import telebot
import logging
import time
import flask
from telebot import types
import botparts

###############################################################
API_TOKEN = '516231077:AAHz8hZQ71xHagXAZ1NsmJfHZSpZt2-1R_E'
WEBHOOK_HOST = 'ip'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % API_TOKEN
# logger = telebot.logger
# telebot.logger.setLevel(logger.info)
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
###############################################################


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


###############################################################
# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()
time.sleep(1)


# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))


# Start flask server
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)
