import websocket
import json
import time
import threading
from colorama import Fore, Style
from decimal import Decimal, ROUND_DOWN

changeCount = 0
measurementInterval = 3
ticker = 'BTC-USD'  

logFile = open('order_book_stats.json', 'a')

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(str(o.quantize(Decimal('.00'), rounding=ROUND_DOWN)))
        return super().default(o)

def on_open(ws):
    with open('logo.txt', 'r') as logo_file:
        logo = logo_file.read()
        print(logo)
    print('WebSocket Connection Opened. . . .')

    subscriptionData = {
        'type': 'subscribe',
        'product_ids': ['ticker'],
        'channels': [
            {'name': 'level2', 'product_ids': [ticker]},
            {'name': 'ticker', 'product_ids': [ticker]}
        ]
    }

    ws.send(json.dumps(subscriptionData))

def on_message(ws, message):
    global changeCount

    message = json.loads(message)

    if message['type'] == 'snapshot' or message['type'] == 'l2update':
        changeCount += 1

def on_error(ws, error):
    print('WebSocket error:', error)

def on_close(ws):
    logFile.close()
    print('WebSocket Connection Closed')

def print_statistics():
    global changeCount

    previous_speed = 0  
    first_interval = True  

    while True:
        time.sleep(measurementInterval)
        statistics = {
            'measurementInterval': measurementInterval,
            'totalChanges': Decimal(changeCount),
            'speed': Decimal(changeCount) / Decimal(measurementInterval),
            'velocity': Decimal(changeCount / measurementInterval) - Decimal(previous_speed),  # Calculate velocity
            'symbol': ticker
        }

        if not first_interval:
            print('---------------------------')
            print('Symbol:', Fore.MAGENTA + statistics['symbol'] + Style.RESET_ALL)
            print('Interval:', statistics['measurementInterval'], 'seconds')
            print('Total Changes:', Fore.MAGENTA + str(statistics['totalChanges']) + Style.RESET_ALL)
            print('Speed:', Fore.BLUE + f'{statistics["speed"]:.2f}', 'changes per second' + Style.RESET_ALL)

            if statistics['velocity'] >= 0:
                velocity_str = '+' + format(statistics['velocity'], '.2f')
            else:
                velocity_str = format(statistics['velocity'], '.2f')

            print('Velocity Δ:', Fore.MAGENTA + velocity_str + ' (c/s²)' + Style.RESET_ALL)
            print('---------------------------')

            logFile.write(json.dumps(statistics, cls=DecimalEncoder) + '\n')

        if first_interval:
            first_interval = False

        previous_speed = changeCount / measurementInterval 
        changeCount = 0

if __name__ == '__main__':
    statistics_thread = threading.Thread(target=print_statistics)
    statistics_thread.start()

    socket = websocket.WebSocketApp('wss://ws-feed.exchange.coinbase.com')
    socket.on_open = on_open
    socket.on_message = on_message
    socket.on_error = on_error
    socket.on_close = on_close
    
    socket.run_forever()
    
