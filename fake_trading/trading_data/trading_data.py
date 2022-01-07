import sched, time

from yfinance.ticker import Ticker
from pubsub import pub

class TradingData:
    def __init__(self, stock: str):
        self.stock_name = stock
        self.stock = Ticker(self.stock_name)
        self.data = self.stock.history(period='1d', interval='1m')
        self.s = sched.scheduler(time.time, time.sleep)
        self.current_index = 0
        self.max_index = len(self.data['Close'])

    def publish_last_price(self, sc):
        if self.current_index < self.max_index:
            pub.sendMessage(self.stock_name, arg={'last_traded_price': self.data['Close'][self.current_index], 'volume': self.data['Volume'][self.current_index]})
            self.current_index += 1
            self.s.enter(5, 1, self.publish_last_price, (sc,))

    def start_publish(self):
        self.s.enter(5, 1, self.publish_last_price, (self.s, ))
        self.s.run()