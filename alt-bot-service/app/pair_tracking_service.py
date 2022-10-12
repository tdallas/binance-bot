import threading

from binance_service import perform_trade, get_trades_for_pair, get_order_status, get_market_info, get_binance_info
from email_sender import send_email
from models import PairsContent, PairContent, Pair


class TrackingService:
    def __init__(self, db):
        self.db = db

    def save_pairs_and_send_notification(self, content: PairsContent):
        pairs_for_notifications = []
        for pair in content.content:
            if not self.contains_pair(pair.pair):
                self.save_pair(pair)
                pairs_for_notifications.append(pair)
        send_email(pairs_for_notifications)

    def contains_pair(self, pair: str):
        cursor = self.db.cursor()
        cursor.execute(f'SELECT * FROM pairs WHERE pair="{pair}"')
        cursor.fetchall()
        return cursor.rowcount > 0

    def save_pair(self, pair: PairContent):
        cursor = self.db.cursor()
        cursor.execute(
            f"INSERT INTO pairs(pair, date, traded) VALUES (%s, %s, %s)", (pair.pair, pair.date, False))
        self.db.commit()

    def get_pairs_for_trade(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * from Pairs WHERE traded = False")
        return cursor.fetchall()

    def trade(self):
        tasks = []
        pairs_for_trade = self.get_pairs_for_trade()
        print('About to trade:', pairs_for_trade)
        if len(pairs_for_trade) > 0:
            pairs = list(map(lambda row: Pair(pair=row[0], date=row[1], traded=row[2], buy_price=row[3]),
                             pairs_for_trade))
            for pair in pairs:
                task = threading.Thread(target=perform_trade, args=(pair.pair, pair.buy_price))
                tasks.append(task)
                task.start()

            # wait for every task to finish
            for task in tasks:
                task.join()

        return f"Traded {len(tasks)} pairs"

    def get_trades_for_pair(self, pair: str, qty: int, simple: bool):
        trades = []
        first_id = 0
        while qty > 0:
            response = get_trades_for_pair(pair, limit=500 if qty < 1000 else 1000, from_id=first_id)
            trades = trades + response
            first_id += (1000 if qty >= 1000 else 500)
            qty -= (1000 if qty >= 1000 else 500)

        return list(map(lambda x: {"timestamp": x['time'], "price": x['price'], "qty": x['qty'],
                                   "isBuy": 1 if x['isBuyerMaker'] is False else 0}, trades)) if not simple else list(
            map(lambda x: [x['time'], x['price'], x['qty'], 1 if x['isBuyerMaker'] is False else 0], trades))

    def set_buy_price(self, pair, price):
        print(price)
        cursor = self.db.cursor()
        cursor.execute(f"UPDATE Pairs SET buy_price = {price} WHERE pair = '{pair}'")
        self.db.commit()

    def get_order_status(self, pair, order_id):
        return get_order_status(pair, order_id)

    def get_market_info(self, pair):
        return get_market_info(pair)

    def get_pairs_quote(self, crypto):
        response = get_binance_info()
        symbols = list(filter(lambda x: x.find(crypto) != -1 and x.find("BTC") == -1 and x.find("ETH") == -1,
                              map(lambda x: x['symbol'], response['symbols'])))
        return symbols
