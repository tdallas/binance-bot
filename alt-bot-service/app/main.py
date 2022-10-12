# This is a sample Python script.

import time
from datetime import datetime

import mysql.connector
import schedule
from fastapi import FastAPI

from models import PairsContent, SetBuyPriceBody
from pair_tracking_service import TrackingService

app = FastAPI()

connected = False
while not connected:
    try:
        db = mysql.connector.connect(
            host="mysql",
            user="root",
            password="alt-bot",
            database="alt_bot_service",
            port=3330
        )
        connected = True
    except Exception as e:
        time.sleep(2)
        print(e)

pair_service = TrackingService(db)

print(db.is_connected())

# Testing
job = schedule.every().hour.do(lambda _: pair_service.trade())


def get_timestamp():
    return int(time.time())


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/pair")
def send_email_notification_with_pairs(content: PairsContent):
    pair_service.save_pairs_and_send_notification(content)
    return {"email_sent": "true"}


@app.post("/trade")
def trade():
    print('timestamp for request: ', datetime.fromtimestamp(get_timestamp()))
    return pair_service.trade()


@app.post("/set-buy-price")
def set_buy_price(body: SetBuyPriceBody):
    pair_service.set_buy_price(body.pair, body.buy_price)
    return "Price setted, new buy price= "


@app.get("/get-trades/{pair}")
def get_trades_for_pair(pair: str, qty: int = 1000, simple: bool = False):
    # Only first 1000 trades
    return pair_service.get_trades_for_pair(pair, qty, simple)


@app.get("/pair/order-status/{pair}")
def get_order_status(pair: str, order_id: int):
    return pair_service.get_order_status(pair, order_id)


@app.get("/pair/market-info/{pair}")
def get_market_info(pair: str):
    return pair_service.get_market_info(pair)


@app.get("/market-info/{crypto}")
def get_all_pairs_quote(crypto: str):
    return pair_service.get_pairs_quote(crypto)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
