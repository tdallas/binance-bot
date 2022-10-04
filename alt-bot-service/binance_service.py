from decimal import *
import numpy as np
from binance_client import BinanceClient

RET_EXPECTED = 1.05
QTY_TO_BUY = 0  # Amount of sell / current_btc_price
QTY_TO_SELL = 0

FILLED_ORDER_STATUS = "FILLED"


def calculate_qty(token_price, amount_in_usd):
    return '{0:.2f}'.format(amount_in_usd / token_price)


def extract_price_from_order(order):
    return float(order['price']) * RET_EXPECTED if float(order['price']) != 0 else np.array(
        list(map(lambda x: float(x['price']), order['fills']))).mean() * RET_EXPECTED


def extract_price_from_order_formatted(order):
    return '{0:.3f}'.format(extract_price_from_order(order))


def perform_trade(pair: str, price: Decimal):
    print(f'en perform trade con pair {pair}')
    client = BinanceClient(testnet=True)
    order = client.send_buy_order(pair, calculate_qty(price, 25))
    order_id = order['orderId']
    qty = order['executedQty']
    status = order['status']
    while status != FILLED_ORDER_STATUS:
        order = client.get_order_status(pair, order_id)
        status = order['status']
        qty = order['executedQty']
    price = extract_price_from_order_formatted(order)
    print(status, qty, price)
    sell_order = client.send_sell_order(pair, qty, price)
    print('sell_order', sell_order)
