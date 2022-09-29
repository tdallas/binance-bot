from email_sender import send_email
from models import PairsContent, PairContent
from datetime import datetime


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

    def get_pairs_not_traded(self):
        cursor = self.db.cursor()
        return cursor.execute("SELECT * from PAIRS WHERE traded = False").fetchall()
