from decimal import *
import numpy as np
from binance_client import BinanceClient
import time

RET_EXPECTED = 1.05
QTY_TO_BUY = 0  # Amount of sell / current_btc_price
QTY_TO_SELL = 0

FILLED_ORDER_STATUS = "FILLED"

TESTNET = False


def calculate_qty(token_price, amount_in_usd):
    return '{0:.1f}'.format(amount_in_usd / token_price)


def extract_price_from_order(order):
    return float(order['price']) * RET_EXPECTED if float(order['price']) != 0 else np.array(
        list(map(lambda x: float(x['price']), order['fills']))).mean() * RET_EXPECTED


def extract_price_from_order_formatted(order):
    return '{0:.3f}'.format(extract_price_from_order(order))


def get_trades_for_pair(pair: str, from_id: int, limit: int):
    client = BinanceClient(testnet=TESTNET)
    return client.get_trades_for_pair(pair, limit, from_id)


def get_order_status(pair: str, order_id: int):
    client = BinanceClient(testnet=TESTNET)
    return client.get_order_status(pair, order_id)


def get_market_info(pair: str):
    client = BinanceClient(testnet=TESTNET)
    return client.get_market_info(pair)

def get_binance_info():
    client = BinanceClient(testnet=TESTNET)
    return client.get_binance_info()


def perform_trade(pair: str, price: Decimal):
    print(f'en perform trade con pair {pair} {price}')
    client = BinanceClient(testnet=TESTNET)
    error = True
    while error:
        try:
            order = client.send_buy_order(pair, calculate_qty(price, 18))
            print(order)

            if order['orderId'] > 0:
                error = False
        except Exception as e:
            print('exception', e)
            time.sleep(0.01)
    print('order', order)
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
