import tracker
import csv


def update_csv(block_number):
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

    f.close()


if __name__ == '__main__':

    file = open('Transactions.csv')
    dataset_csv = csv.reader(file)
    next(dataset_csv)

    tracker_transactions = tracker.transactions
    all_transactions = []

    csv_last_blocks = []
    tracker_blocks = []

    for row in dataset_csv:
        all_transactions.append(row)

    all_transactions.reverse()

    tx_num = len(tracker_transactions)

    for i in range(tx_num - 1, -1, -1):
        temp = all_transactions[i][0::-6]
        csv_last_blocks.append(int(temp[0]))

    file.close()

    for tx in tracker_transactions:
        tracker_blocks.append(tx['block'])

    tracker_blocks.reverse()

    for i in range(tx_num):
        if tracker_blocks[i] not in csv_last_blocks:
            print('---NEW TRANSACTION---')
            for tx in tracker_transactions:
                for key, value in tx.items():
                    if tx['block'] == tracker_blocks[i]:
                        print('\t', key, ' : ', value)

            update_csv(tracker_blocks[i])
