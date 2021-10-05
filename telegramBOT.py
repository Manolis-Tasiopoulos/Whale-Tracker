from datetime import datetime
import telegram.ext
import scanner


starting_time = datetime.now()
starting_hour = int(starting_time.strftime("%H"))


def check_address(context):
    now = datetime.now()
    now_hour = int(now.strftime("%H"))
    print(starting_hour, ' ', now_hour)

    if now_hour > starting_hour:
        print('Complete')
        missing_transactions = scanner.main(verbose=False)
        str_tx = ''

        if missing_transactions is None:
            missing_transactions = []

        # print(missing_transactions)
        if len(missing_transactions) != 0:
            str_tx = '---NEW TRANSACTION---\n\n'
            for tx in missing_transactions:
                for key, value in tx.items():
                    # print('\t', key, ' : ', value)
                    str_tx += key + ': ' + str(value)

                    if key != 'total cost ($)':
                        str_tx += '\n'

        if str_tx != '':
            context.bot.send_message(chat_id=context.job.context, text=str_tx)


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Start monitoring...')
    context.job_queue.run_repeating(check_address, 240, context=update.message.chat_id)


def stop(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Stopped!')
    context.job_queue.stop()


with open('token.txt', 'r') as f:
    TOKEN = f.read()


updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher

updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
updater.dispatcher.add_handler(telegram.ext.CommandHandler('stop', stop))
updater.start_polling()
updater.idle()
