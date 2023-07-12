from matplotlib.animation import FuncAnimation
from matplotlib.dates import date2num
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import threading
import websocket
import datetime
import json

timestamps = []
spread_values = []

def calculate_spread(bid_price, ask_price):
    return ask_price - bid_price

def on_open(ws):
    print('WebSocket connection opened')
    subscription_data = {
        'type': 'subscribe',
        'product_ids': ['BTC-USD'],
        'channels': ['ticker']
    }
    ws.send(json.dumps(subscription_data))

def on_message(ws, message):
    message = json.loads(message)
    if message['type'] == 'ticker':
        if 'best_bid' in message and 'best_ask' in message:
            bid_price = float(message['best_bid'])
            ask_price = float(message['best_ask'])
            spread = calculate_spread(bid_price, ask_price)
            timestamps.append(message['time'])
            spread_values.append(spread)
        else:
            print('Bid and ask prices not found in the message.')

def on_error(ws, error):
    print('WebSocket error:', error)

socket = websocket.WebSocketApp('wss://ws-feed.exchange.coinbase.com')
socket.on_open = on_open
socket.on_message = on_message
socket.on_error = on_error

thread = threading.Thread(target=socket.run_forever)
thread.daemon = True
thread.start()

fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlabel('Time')
ax.set_ylabel('Spread')
ax.set_title('Bid-Ask Spread')

formatter = ticker.FuncFormatter(lambda x, _: '${:,.2f}'.format(x))
ax.yaxis.set_major_formatter(formatter)

def update_plot(frame):
    x = [date2num(datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')) for t in timestamps]
    line.set_data(x, spread_values)
    ax.relim()
    ax.autoscale_view()
    return line,

ani = FuncAnimation(fig, update_plot, interval=1000)

plt.show()
