import time
from pubsub import pub

from trading_data.trading_data import TradingData

def origiinal_listener(arg):
    print(arg)

if __name__ == '__main__':
    trading_data = TradingData('MSFT')
    pub.subscribe(origiinal_listener, 'MSFT')
    trading_data.start_publish()
    time.sleep(60)


