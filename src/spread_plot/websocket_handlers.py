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
            spread = utils.calculate_spread(bid_price, ask_price)
            timestamps.append(message['time'])
            spread_values.append(spread)
        else:
            print('Bid-Ask prices not found in the WebSocket message.')

def on_error(ws, error):
    print('WebSocket error:', error)
