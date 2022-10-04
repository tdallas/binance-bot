# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from typing import Union
from email_sender import send_email
from fastapi import FastAPI
import mysql.connector
from pair_tracking_service import TrackingService
from models import PairsContent, SetBuyPriceBody

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
app = FastAPI()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="alt-bot",
    database="alt_bot_service"
)

pair_service = TrackingService(db)

print(db.is_connected())


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/pairs")
def send_email_notification_with_pairs(content: PairsContent):

    pair_service.save_pairs_and_send_notification(content)
    return {"email_sent": "true"}

@app.post("/trade")
def trade():
    return pair_service.trade()

@app.post("/set-buy-price")
def set_buy_price(body: SetBuyPriceBody):
    pair_service.set_buy_price(body.pair, body.buy_price)
    return "Price setted, new buy price= "

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
