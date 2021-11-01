import scanner
import os.path

from datetime import datetime
from telegram.ext import Updater, CommandHandler
from os import path


starting_time = datetime.now()
starting_hour = int(starting_time.strftime("%H"))


def check_address(context):
    now = datetime.now()
    now_hour = int(now.strftime("%H"))
    now_hour = 13
    print(starting_hour, ' ', now_hour)

    if now_hour > starting_hour:
        print('Complete')
        missing_transactions = scanner.main(verbose=False)
        str_tx = ''

        if missing_transactions is None:
            missing_transactions = []

        print(missing_transactions)
        if len(missing_transactions) != 0:
            str_tx = '---NEW TRANSACTION---\n\n'
            for tx in missing_transactions:
                for key, value in tx.items():
                    print('\t', key, ' : ', value)
                    str_tx += key + ': ' + str(value)

                    if key != 'total cost ($)':
                        str_tx += '\n'

        if str_tx != '':
            for chat_id in chat_ids:
                context.bot.send_message(chat_id=chat_id, text=str_tx)


def start(update, context):
    update.message.reply_text("""Helo ! Welcome to WhaleTrackerBot. \n\nThis bot will check if the biggest bitcoin whale is adding or removing btc from its wallet.
       
* To start receiving new whales transactions click-type: /check 
    
* If you want to stop receiving messages from this bot click-type: /stop
    """)


def stop(update, context):
    chat_id = update.message.chat_id
    chat_id = str(chat_id)

    if chat_id in chat_ids:
        with open("chat_ids.txt", "r") as f:
            lines = f.readlines()
        with open("chat_ids.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != chat_id:
                    f.write(line)

        chat_ids.remove(chat_id)
        update.message.reply_text("Stopped! You will no longer receiving ny new transaction of the whale")
        print(chat_ids)
    else:
        update.message.reply_text("First you have to start receiving new whales transactions. Click-type: /check")


def check(update, context):
    chat_id = update.message.chat_id
    chat_id = str(chat_id)

    if chat_id not in chat_ids:
        with open("chat_ids.txt", 'a') as file:
            file.write(chat_id+'\n')

        chat_ids.append(chat_id)
        update.message.reply_text("Start monitoring...")
        print(chat_ids)
    else:
        update.message.reply_text("You are already monitoring...")


def admin_users(update, context):
    users_count = len(chat_ids)

    update.message.reply_text(str(users_count) + " active user(s)")


with open('token.txt', 'r') as f:
    TOKEN = f.readline()


updater = Updater(TOKEN, use_context=True)
disp = updater.dispatcher

chat_ids = []

if not path.exists("chat_ids.txt"):
    with open("chat_ids.txt", 'x') as f:
        f.write('')

else:
    with open("chat_ids.txt") as f:
        lines = f.readlines()
        print(lines)
        chat_ids = [line.rstrip() for line in lines]

print(chat_ids)

updater.job_queue.run_repeating(check_address, interval=30)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('stop', stop))
updater.dispatcher.add_handler(CommandHandler('check', check))
updater.dispatcher.add_handler(CommandHandler('admin_users', admin_users))

updater.start_polling()
updater.idle()
