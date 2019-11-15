import paho.mqtt.client as mqtt 

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import socket

temp = "36.8"
pressure = " "

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Greeting  {}'.format(update.message.from_user.first_name))

def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def status(update, context):
    global temp
    global pressure
    # ToBe edited
    with open('data.txt','r') as f:
        for line in f:
            if "[sensor/bluetooth/temp]" in line:
                temp = line
            if "[sensor/bluetooth/pressure]" in line:
                pressure = line
    status = "Normal"
    #temp = "36.8"
    heart_rate = "Beep Beep"
    ECG = "Zap Zap"
    msg = ("Status: " + status +
    	"\nTemperature: " + temp + "°C" + 
    	"\nHeart Rate: " + heart_rate + "\nPressure: " + pressure)

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main():
    # bot token
    bot_token = '1062467996:AAGx8i12_5ca1HOOgiP9b1y9xrMHB5Wg1yI'
    bot = telegram.Bot(token=bot_token)
    print(bot.get_me())

    # setting up updater & dispatcher
    updater = Updater(token=bot_token, use_context=True, request_kwargs={'read_timeout': 6, 'connect_timeout': 7})
    dispatcher = updater.dispatcher

	# debugging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('hello', hello))

    dispatcher.add_handler(CommandHandler('status', status))

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()

main()


