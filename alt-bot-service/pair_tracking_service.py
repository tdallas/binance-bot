from models import PairsContent

class TrackingService:
    def __init__(self, db):
        self.db = db

    def save_pairs_and_send_notification(self, content: PairsContent):
        for pair in content:
            if not self.contains_pair(pair):
                print("a")
                # save pair with date
                # send notification

    def contains_pair(self, pair):
        return self.db.execute(f'SELECT COUNT(*) FROM pairs WHERE pair={pair}').fetch() > 0