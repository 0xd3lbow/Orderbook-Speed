import websocket
import json
import time
from decimal import Decimal, ROUND_DOWN
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.animation import FuncAnimation
import threading

buyChangeCount = 0
sellChangeCount = 0
totalChangeCount = 0
measurementInterval = 3 
lookback_duration = 120  
update_interval = 10  
last_update_time = 0
animation_running = True

logFile = open('order_book_stats.json', 'a')

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(str(o.quantize(Decimal('.1'), rounding=ROUND_DOWN)))
        return super().default(o)

def on_open(ws):
    print('WebSocket connection opened')

    subscriptionData = {
        'type': 'subscribe',
        'product_ids': ['BTC-USD'],
        'channels': [
            {'name': 'level2', 'product_ids': ['BTC-USD']},
            {'name': 'ticker', 'product_ids': ['BTC-USD']}
        ]
    }

    ws.send(json.dumps(subscriptionData))

def on_message(ws, message):
    global buyChangeCount, sellChangeCount, totalChangeCount

    message = json.loads(message)

    if message['type'] == 'snapshot' or message['type'] == 'l2update':
        if message.get('changes'):
            for change in message['changes']:
                if change[0] == 'buy':
                    buyChangeCount += 1
                elif change[0] == 'sell':
                    sellChangeCount += 1
                totalChangeCount += 1

def on_error(ws, error):
    print('WebSocket error:', error)

def on_close(ws):
    logFile.close()
    print('WebSocket connection closed')

def update_statistics(frame):
    global buyChangeCount, sellChangeCount, totalChangeCount

    buy_speed = Decimal(buyChangeCount) / Decimal(measurementInterval)
    sell_speed = Decimal(sellChangeCount) / Decimal(measurementInterval)
    total_speed = Decimal(totalChangeCount) / Decimal(measurementInterval)

    buyChangeCount = 0
    sellChangeCount = 0
    totalChangeCount = 0

    return buy_speed, sell_speed, total_speed

fig, ax = plt.subplots()

def animate(frame):
    global animation_running, last_update_time, time_intervals, buy_speeds, sell_speeds, total_speeds

    if not animation_running:
        return

    current_time = time.time()

    if current_time - last_update_time >= update_interval:
        buy_speed, sell_speed, total_speed = update_statistics(frame)
        buy_speeds.append(buy_speed)
        sell_speeds.append(sell_speed)
        total_speeds.append(total_speed)
        time_intervals.append(current_time)  
        last_update_time = current_time

    min_time_interval = current_time - (lookback_duration * 60)

    time_intervals_display = []
    buy_speeds_display = []
    sell_speeds_display = []
    total_speeds_display = []

    for i in range(len(time_intervals)):
        if time_intervals[i] >= min_time_interval:
            time_intervals_display.append(time_intervals[i])
            buy_speeds_display.append(buy_speeds[i])
            sell_speeds_display.append(sell_speeds[i])
            total_speeds_display.append(total_speeds[i])

    ax.clear()

    time_intervals_minutes = [(t - time_intervals_display[0]) / 60 for t in time_intervals_display]

    ax.plot(time_intervals_minutes, buy_speeds_display, label='Buy Speed')
    ax.plot(time_intervals_minutes, sell_speeds_display, label='Sell Speed')
    ax.plot(time_intervals_minutes, total_speeds_display, label='Total Speed')
    ax.set_xlabel('Time (minutes)')
    ax.set_ylabel('Changes per Second')
    ax.set_title('Order Book Speed')
    ax.legend()

    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    plt.pause(0.01)  

time_intervals = []
buy_speeds = []
sell_speeds = []
total_speeds = []

anim = FuncAnimation(fig, animate, interval=1000)

if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws-feed.pro.coinbase.com",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws_thread = threading.Thread(target=ws.run_forever)
    ws_thread.start()

    plt.show()
