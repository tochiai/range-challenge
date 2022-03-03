import redis
import datetime


class StatsClient:
    def __init__(self):
        self.redis = redis.Redis(host="cache")

    def visits_key(self, short_url: bytes):
        return f"visits:{short_url.decode('utf-8')}"

    def visits_on_date_key(self, short_url: bytes, date: str):
        return f"visit_on#{date}#{short_url}"

    def update_stats(self, short_url: bytes):
        # aggregate visits incr
        self.redis.incr(self.visits_key(short_url), amount=1)
        # visit today's date
        self.redis.incr(
            self.visits_on_date_key(
                short_url,
                datetime.date.today().isoformat(),
            ),
            amount=1,
        )

    def get_stats(self, short_url: bytes):
        visits = self.redis.get(self.visits_key(short_url))
        today = datetime.date.today()
        # get histogram for last week
        dates = [today - datetime.timedelta(days=delta) for delta in range(7, -1, -1)]
        keys = [self.visits_on_date_key(short_url, date) for date in dates]
        hist = self.redis.mget(keys)
        hist = dict(zip(dates, hist))
        return {"visits": visits, "hist": hist}
