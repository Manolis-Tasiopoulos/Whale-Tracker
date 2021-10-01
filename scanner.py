import tracker
import csv


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


def main(verbose):
    missing_tx = []
    all_transactions = []

    csv_last_blocks = []
    tracker_blocks = []

    tracker_transactions = tracker.main(verbose=False)
    balance = "{:,}".format(tracker_transactions[-1])
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

            update_csv(tracker_blocks[i], tracker_transactions)

            return missing_tx


if __name__ == '__main__':
    main(True)
