import tracker
import csv
import yfinance as yf
import datetime as dt


def update_csv(block_number, tracker_transactions):
    missing_txs = []
    new_tx_row = []

    for tx in tracker_transactions:
        for key, value in tx.items():
            if tx['block'] == block_number:
                new_tx_row.append(value)
        if len(new_tx_row) != 0:
            missing_txs.append(new_tx_row)
        new_tx_row = []

    with open('Transactions.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        for row in missing_txs:
            writer.writerow(row)


def get_bitcoin_price(time=None):
    start = time
    end = time + dt.timedelta(minutes=1)

    try:
        data = yf.download(tickers="BTC-USD", start=start, end=end, interval="1m", progress=False, show_errors=True)
        data = data.iloc[-1].tolist()

        return data[1]
    except IndexError:
        return 0


def refine_txs(transactions):
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

    return transactions


def main(verbose):
    missing_tx = []
    all_transactions = []

    csv_last_blocks = []
    tracker_blocks = []

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
        tracker_blocks.append(tx['block'])

    tracker_blocks.reverse()

    for i in range(tx_num):
        if tracker_blocks[i] not in csv_last_blocks:
            if verbose:
                print('---NEW TRANSACTION---')
            for tx in tracker_transactions:
                for key, value in tx.items():
                    if tx['block'] == tracker_blocks[i]:
                        missing_tx.append({key: value})
                        if verbose:
                            print('\t', key, ' : ', value)

                dollar_price = get_bitcoin_price(time=tx['time'])
                total_btc = round(tx['amount (BTC)'], 10)
                total_cost = float(dollar_price * float(total_btc))

                tx['BTC price ($)'] = dollar_price
                tx['total cost ($)'] = total_cost

            tracker_transactions = refine_txs(tracker_transactions)
            update_csv(tracker_blocks[i], tracker_transactions)

            return missing_tx


if __name__ == '__main__':
    main(True)
