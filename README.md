# backtrader_strategies
In this project we use backtrader, a open platform that is suitable for designing and testing trading strategies.  

We implemented three strategies: momentum with simple moving average, dual thrust, rebalacing strategy. 

Momentum with simple moving average is a strategy that uses two different moving averages to create buy/sell signals. e.g., we buy when 50-days moving average cross 200 days moving average from below. 

Rebalacing strategy is a strategy that usually used to manage a large porfolio. e.g. at the begining of every month we rebalance the porpotions of stocks/bonds to be 5:5. 

Dual thrust strategy is also a kind of momentum strategy. We use the daily high/low data of past several days to set buy/sell signal. For detail explanation, see this [nice explaination](https://medium.com/@FMZ_Quant/dual-thrust-trading-strategy-2cc74101a626). 

We build these strategies, optimize them, and test again buy and hold method. We also compute some metrics including Sharp ratio. 

