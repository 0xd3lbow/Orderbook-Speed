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

  


