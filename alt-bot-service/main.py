# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from typing import Union
from email_sender import send_email, PairsContent
from fastapi import FastAPI
import mysql.connector

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
app = FastAPI()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="alt-bot",
    database="alt_bot_service"
)

print(db.is_connected())


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/notification")
def send_email_notification_with_pairs(content: PairsContent):
    print(content)
    send_email(content)
    return {"email_sent": "true"}

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
