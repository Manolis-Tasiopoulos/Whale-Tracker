import tracker
import csv
import yfinance as yf
import datetime as dt


def update_csv(missing_txs):

    for tx in missing_txs:
        missing_txs_row = []
        for key, value in tx.items():
            missing_txs_row.append(value)

        with open('Transactions.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(missing_txs_row)


def get_bitcoin_price(time=None):
    start = time
    end = time + dt.timedelta(minutes=1)

    try:
        data = yf.download(tickers="BTC-USD", start=start, end=end, interval="1m", progress=False, show_errors=True)
        data = data.iloc[-1].tolist()

        return data[1]
    except IndexError:
        return 0


def refine_tx(transactions):
    doubles_indexes = []

    for i in range(1, len(transactions)):
        if transactions[i]['block'] == transactions[i - 1]['block']:
            transactions[i]['amount (BTC)'] += transactions[i - 1]['amount (BTC)']
            transactions[i]['total cost ($)'] += transactions[i - 1]['total cost ($)']

            doubles_indexes.append(i - 1)

    for double in doubles_indexes:
        del transactions[double]

    for tx in transactions:
        tx['time'] = tx['time'].strftime('%d-%m-%Y %H:%M')
        tx['amount (BTC)'] = ('%f' % tx['amount (BTC)']).rstrip('.0')
        tx['total cost ($)'] = ('%f' % tx['total cost ($)']).rstrip('.0')

    transactions.reverse()

    return transactions


def main(verbose):
    missing_txs = []
    all_transactions = []
    csv_last_blocks = []

    tracker_transactions = tracker.main(verbose=False)

    del tracker_transactions[-1]

    with open('Transactions.csv') as file:
        dataset_csv = csv.reader(file)

        next(dataset_csv)

        for row in dataset_csv:
            all_transactions.append(row)

    all_transactions.reverse()

    tx_num = len(tracker_transactions)

    for i in range(tx_num - 1, -1, -1):
        temp = all_transactions[i][0::-6]
        csv_last_blocks.append(int(temp[0]))

    for tx in tracker_transactions:
        if tx['block'] not in csv_last_blocks:
            temp = {}

            for key, value in tx.items():
                temp[key] = value

            dollar_price = get_bitcoin_price(time=tx['time'])
            total_btc = round(tx['amount (BTC)'], 10)
            total_cost = float(dollar_price * float(total_btc))

            temp.update({'BTC price ($)': dollar_price,
                         'total cost ($)': total_cost})

            missing_txs.append(temp)

    missing_txs = refine_tx(missing_txs)
    update_csv(missing_txs)

    if verbose:
        #newTransaction
        for tx in missing_txs:
            print('---NEW TRANSACTION---')
            for key, value in tx.items():
                print('\t', key, ' : ', value)
            print()

    return missing_txs


if __name__ == '__main__':
    main(True)
