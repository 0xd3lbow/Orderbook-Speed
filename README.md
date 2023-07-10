# Simple Model for High Frequency Orderbook Data

This is a lightweight tool that measures the `speed` and `velocity` of the limit orderbook, by using a Websocket to fetch orderbook updates it can track the fluctuation of quotes and return the total changes per second.
  * Plot the rate of change of the bid and ask
  * Can be applied to any exchange's websocket connection

<img width="473" alt="orderbookspeed" src="https://github.com/0xd3lbow/Orderbook-Speed/assets/130616587/39511948-77d1-45a9-8661-a0b1aaa8394b">

# Velocity in Relation to Orderbook Speed
**Velocity** is a metric for the `rate of change in speed`, in this script I use **velocity** to represent the change in speed per unit of time, in order to measure the acceleration and deceleration of aggregated quotes.

<img width="580" alt="Terminal-Output" src="https://github.com/0xd3lbow/Orderbook-Speed/assets/130616587/20c522fb-3e14-47d5-a90c-89df2cc9ae61">


In the physical world, **velocity** is expressed in terms of distance traveled per unit of time and the unit of velocity is meters per second `(m/s)` .

  * However, when **velocity** is measured in terms of `changes in speed per unit of time`, it can be described as changes per second squared `(c/s²)` . **(c/s²)** means we're measuring the change in the number of quote updates per second, the rate is squared to indicate the acceleration or deceleration of those changes over time.
   
  * The squared unit `(s²)` indicates the rate of change is measured per unit of time squared.

# Pulled Bids & Asks for Altcoin Orderbooks

Outputs for pulled bids and asks have been added.
* To run this script on altcoins, you'll have to update the size property under the for-loop to calculate the pulled orders from the new ticker.
* **Note:** If you refer to the Coinbase documentation on Websocket channels, a message containing a size property of "0" indicates a previously active order was removed from that price level. 

<img width="749" alt="Pulled-BidAsk" src="https://github.com/0xd3lbow/Orderbook-Speed/assets/130616587/9919bc9f-6058-4b95-9420-b823afcb97b6">



# Size Property Variance
* In the case of "BTC-USD" the size property for a pulled order is `"0.00000000"` .
  
```python
# BTC-USD
if message['type'] == 'l2update':
            for change in message['changes']:
                side, price, size = change
                if side == 'buy' and size == '0.00000000':
                    pulledBids += 1
                elif side == 'sell' and size == '0.00000000':
                    pulledAsks += 1
```
* For other tokens the l2update can return a different integer such as `"0.00"` . Here's `"LDO-USD"` for example.

```python
# LDO-USD
if side == 'buy' and size == '0.00':
    pulledBids += 1
elif side == 'sell' and size == '0.00':
    pulledAsks += 1
```

* To find the correct format from the websocket, use a print statement under the `on_message` function.

```python
def on_message(ws, message):
    global changeCount, pulledBids, pulledAsks

    message = json.loads(message)
    print('WebSocket Message:', message)
```

