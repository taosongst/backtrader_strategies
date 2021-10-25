# backtrader_strategies
<!-- In this project we use [backtrader](https://www.backtrader.com/), a open platform that is suitable for designing and testing trading strategies.  

We implemented three strategies: momentum with simple moving average, dual thrust, rebalacing strategy. 

Momentum with simple moving average is a strategy that uses two different moving averages to create buy/sell signals. e.g., we buy when 50-days moving average cross 200 days moving average from below. 

Rebalacing strategy is a strategy that usually used to manage a large porfolio. e.g. at the begining of every month we rebalance the porpotions of stocks/bonds to be 5:5. 

Dual thrust strategy is also a kind of momentum strategy. We use the daily high/low data of past several days to set buy/sell signal. For detail explanation, see this [nice explaination](https://medium.com/@FMZ_Quant/dual-thrust-trading-strategy-2cc74101a626) posted by FMZ Quant.

We build these strategies, optimize them, and test again buy and hold method. We also compute some metrics including Sharpe ratio. Note that our purpose in this project is to get familiar with this platform other than finding a winning strategy.  -->
We did a few things in this project:

1. implemented three classical strategies both from stratch and using backtrader. See [this file](https://github.com/taosongst/backtrader_strategies/blob/main/strategies_backtrader.ipynb)
2. We take a closer look at momentum strategies. More specifically we:
- Define momentum effect of each stock inside a 1Y period using the maximal return, minimal return and std when varing the two hyperparameters (long period/short period) in the momentum strategies. Then we categorize them into three categories: profitable using momentum strategy with low std, lossing money using momentum strategy with low std, the rest. This is what we defined as momentum effect and is the main target we want to build a model for. See [this file](https://github.com/taosongst/backtrader_strategies/blob/main/momentumeEffects_multiprocessing.py)
- To build a model to predict these we download some fundamental and trading data of 1000+ stocks from yahoo finance and EOD API. We extract some features including the momentum effect of the previous year, std, pe, ps, revenue growth, correlation with overall market. See [this file](https://github.com/taosongst/backtrader_strategies/blob/main/EOD%20Data.ipynb)
- We use random forest and SVM to predict momentum effect. Using features selection we were able to get, in the best case scenerio, a 0.51 precision on val set. See [this file](https://github.com/taosongst/backtrader_strategies/blob/main/TreeModels.ipynb)
3. To be done:
- We want to extend this method to explore momentum effects across different periods.
- Use the same methology to exam other strategies. 



