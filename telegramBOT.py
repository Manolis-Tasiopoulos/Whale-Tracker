import logging
import scanner
import tokens

from datetime import datetime
from telegram.ext import Updater, CommandHandler
from os import path


def time_check():
    now = datetime.now()
    now_hour_int = int(now.strftime("%H"))

    if now_hour_int > starting_hour_int or (starting_hour_int == 23 and now_hour_int < 1):
        global starting_hour
        starting_hour = -1

        return False
    else:
        remain_min = 60 - now.minute
        print('Starting at:', remain_min, 'minutes')

        return True


def check_address(context):

    if time_check() is False:

        missing_transactions = scanner.main(verbose=False)
        str_tx = ''

        if missing_transactions is None:
            missing_transactions = []

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
    update.message.reply_text("""Hello ! Welcome to WhaleTrackerBot. \n\nThis bot will check if the biggest bitcoin whale is adding or removing btc from its wallet.
       
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
            file.write(chat_id + '\n')

        chat_ids.append(chat_id)
        update.message.reply_text("Start monitoring...")
        print(chat_ids)
    else:
        update.message.reply_text("You are already monitoring...")


def admin_users(update, context):
    users_count = len(chat_ids)

    update.message.reply_text(str(users_count) + " active user(s)")


logging.basicConfig(filename='logging_telegramBOT.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s', )

print("Starting Telegram Bot...")

starting_hour = datetime.now()
starting_hour_int = int(starting_hour.strftime("%H"))

updater = Updater(tokens.Telegram_token, use_context=True)
disp = updater.dispatcher
chat_ids = []

if not path.exists("chat_ids.txt"):
    with open("chat_ids.txt", 'x') as f:
        f.write('')

else:
    with open("chat_ids.txt") as f:
        lines = f.readlines()
        chat_ids = [line.rstrip() for line in lines]

print('Active users chat ID\'s:', chat_ids)

updater.job_queue.run_repeating(check_address, interval=60)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('stop', stop))
updater.dispatcher.add_handler(CommandHandler('check', check))
updater.dispatcher.add_handler(CommandHandler('admin_users', admin_users))

updater.start_polling()
updater.idle()
