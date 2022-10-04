from email_sender import send_email
from models import PairsContent, PairContent, Pair
from binance_service import perform_trade
import threading


class TrackingService:
    def __init__(self, db):
        self.db = db

    def save_pairs_and_send_notification(self, content: PairsContent):
        for pair in content.content:
            if not self.contains_pair(pair.pair):
                self.save_pair(pair)
                send_email(pair)

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
        cursor.execute("SELECT * from Pairs WHERE traded = False AND date >= NOW()")
        return cursor.fetchall()

    def trade(self):
        tasks = []
        pairs = list(map(lambda row: Pair(pair=row[0], date=row[1], traded=row[2], buy_price=row[3]),
                         self.get_pairs_for_trade()))
        for pair in pairs:
            task = threading.Thread(target=perform_trade, args=(pair.pair, pair.buy_price))
            tasks.append(task)
            task.start()

        # wait for every task to finish
        for task in tasks:
            task.join()

        return f"Traded {len(tasks)} pairs"

    def set_buy_price(self, pair, price):
        print(price)
        cursor = self.db.cursor()
        cursor.execute(f"UPDATE Pairs SET buy_price = {price} WHERE pair = '{pair}'")
        self.db.commit()
