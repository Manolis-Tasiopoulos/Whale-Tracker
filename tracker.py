from decimal import Decimal
import datetime as dt

from blockcypher import get_address_full

import yfinance as yf


def sent_tx(tx_item, address):
    for tx_key, tx_value in tx_item.items():
        if tx_key == 'inputs':
            for input_dict in tx_value:
                if address in input_dict['addresses']:
                    return True
                else:
                    return False


def calculate_total(tx_item, address, is_sent_tx=None):
    total_satoshi = 0

    for tx_key, tx_value in tx_item.items():
        if tx_key == 'inputs':
            for input_dict in tx_value:
                if address in input_dict['addresses']:
                    total_satoshi += input_dict['output_value']

        if tx_key == 'outputs':
            for outputs_dict in tx_value:
                if address in outputs_dict['addresses']:
                    if is_sent_tx is True:
                        total_satoshi -= outputs_dict['value']
                    else:
                        total_satoshi += outputs_dict['value']
    convert_to_decimal = Decimal(total_satoshi / pow(10, 8))
    return convert_to_decimal


def bitcoin_price(time=None):
    start = time
    end = start + dt.timedelta(hours=1)

    data = yf.download(tickers="BTC-USD", start=start, end=end, interval="1m", progress=False)
    data = data.iloc[-1].tolist()

    return data[3]


# -------------------------FULL DETAILS OF TRANSACTIONS-------------------------
def main(verbose):
    address = '1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ'
    txs = get_address_full(txn_limit=4, address=address)
    balance = txs['final_balance']
    tx_date = dt
    position_in_transactions = 0
    temp_btc_value = 0
    dollar_price = 0

    tx_type = ''

    is_next_block_same = False

    for item in txs['txs']:

        total_btc = calculate_total(item, address, is_sent_tx=sent_tx(item, address))
        total_btc += temp_btc_value
        temp_btc_value = 0

        if position_in_transactions < len(txs['txs']) - 1:
            if txs['txs'][position_in_transactions]['block_height'] == txs['txs'][position_in_transactions + 1]['block_height']:
                if verbose:
                    print('-----------------------------Skipping Double Block-----------------------------')
                is_next_block_same = True
                temp_btc_value = total_btc
                if verbose:
                    print(temp_btc_value)

        if is_next_block_same is False:
            for key, value in item.items():
                if key == 'inputs' or key == 'outputs':
                    if verbose:
                        print('-----------------------------', key, '-----------------------------')
                    for item_in_out in value:
                        for key_in_out, value_in_out in item_in_out.items():
                            if verbose:
                                print('\t', key_in_out, ' : ', value_in_out)
                        if verbose:
                            print()
                else:
                    if verbose:
                        print(key, ' : ', value)

            if sent_tx(item, address) is True:
                tx_type = 'SELL'
                if verbose:
                    print('SELL')
                    print('Sent BTC: ', total_btc)
            else:
                tx_type = 'BUY'
                if verbose:
                    print('BUY')
                    print('Sent BTC: ', total_btc)

            tx_date = txs['txs'][position_in_transactions]['confirmed']
            tx_date = tx_date + dt.timedelta(hours=3)

            dollar_price = bitcoin_price(time=tx_date)

            tx_date = tx_date.strftime('%d-%m-%Y %H:%M')

        if total_btc != 0:
            transactions.append({'block': txs['txs'][position_in_transactions]['block_height'],
                                 'time': tx_date,
                                 'type': tx_type,
                                 'amount (BTC)': total_btc,
                                 'BTC price ($)': int(dollar_price),
                                 'total cost ($): ': float(dollar_price * float(total_btc))})

        position_in_transactions += 1
        is_next_block_same = False
        if verbose:
            print("\n=========================================================================================================================================================\n")

    for key, value in transactions[1].items():
        if verbose:
            print('\t', key, ' : ', value)


transactions = []

if __name__ == '__main__':
    main(verbose=True)
else:
    main(verbose=False)
