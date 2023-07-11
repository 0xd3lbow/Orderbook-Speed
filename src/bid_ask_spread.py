import json
import websocket

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
            print('--------------------------')
            print('Bid Price:', bid_price)
            print('Ask Price:', ask_price)
            print('Spread:', spread)
            print('--------------------------')
        else:
            print('Bid-Ask prices not found in the Websocket message.')

def on_error(ws, error):
    print('WebSocket error:', error)

socket = websocket.WebSocketApp('wss://ws-feed.exchange.coinbase.com')
socket.on_open = on_open
socket.on_message = on_message
socket.on_error = on_error
socket.run_forever()
