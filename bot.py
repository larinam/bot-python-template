# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, StringRegexHandler
import os 
import sqlite3
import re
import json
import requests

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

conn = sqlite3.connect('sqlite.db')
c = conn.cursor()
# Create table
#c.execute('''CREATE TABLE stocks
#             (date text, trans text, symbol text, qty real, price real)''')
# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
# Save (commit) the changes
conn.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

def start(bot, update):
    update.message.reply_text('Hello World!')

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name.encode('utf8')))

def router(bot, update):
    if update.message.text == 'db':
        db(bot, update)
    if update.message.text == 'rest':
        rest(bot, update)

def db(bot, update):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    stocks = c.execute('select * from stocks')
    update.message.reply_text(str(list(stocks)))
    conn.commit()
    conn.close()

def rest(bot, update):
    base_url = "http://google.com"
    r = requests.get('http://google.com')
    update.message.reply_text(r.text[:2000])
 


updater = Updater(os.environ.get('BOT_TOKEN'))

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(MessageHandler(None, router))

updater.start_polling()
updater.idle()
