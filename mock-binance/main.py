# This is a sample Python script.

import time

from fastapi import FastAPI
import pandas as pd

app = FastAPI()

basePath = "../python/trades_data/"
files = ["AMBBUSD.json", "ASRBUSD.json", "GLMBUSD.json", "KEYBUSD.json", "LUNCUSDT.json", "PHBBUSD.json",
         "SSVBUSD.json", ]
files = list(map(lambda x: basePath + x, files))


def get_timestamp():
    return int(time.time() * 1000)

server_timestamp = get_timestamp()

@app.post("/api/v3/order")
def fake_send_buy_order(timestamp: int):
    # raise Exception("mocking error")
    diff_timestamp = get_timestamp() - server_timestamp
    print(diff_timestamp)
    for file in files:
        print(file)
        df = pd.read_json(file)
        first_timestamp = df['time'].iloc[0]
        print(first_timestamp)
        print((first_timestamp + diff_timestamp))
        # print(df)
        df = df[df['time'] <= (first_timestamp + diff_timestamp)]
        if len(df) > 1:
            df = df[df['time'] >= (first_timestamp + diff_timestamp)]
        print(df)

    return {"timestamp": get_timestamp()}
