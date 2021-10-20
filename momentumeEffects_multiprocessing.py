# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import backtrader as bt
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import numpy as np
from datetime import datetime
import time


class SMA(bt.Strategy):
    
    params=(('period_long',150),('period_short',5),("bs_ratio", 0.8)
           )
      
    def __init__(self):
        self.sma_long=bt.indicators.MovingAverageSimple(self.data, period=self.params.period_long) 
        self.sma_short=bt.indicators.MovingAverageSimple(self.data, period=self.params.period_short) 
        self.sma_signals=bt.indicators.CrossOver(self.sma_short, self.sma_long)    
        
    def next(self):
        buy_vol=7000
        sell_vol=buy_vol*self.params.bs_ratio
#         ma=self.sma[0]
#         pre_ma=self.sma[-1]
        
        if self.sma_signals[0]==1 and not self.position:           
            self.order=self.buy(size=buy_vol)
            
        if self.sma_signals[0]==1 and self.position:
            self.order=self.close()
            self.order=self.buy(size=buy_vol)
            
        if self.sma_signals[0]==-1 and not self.position:
            self.order=self.sell(size=sell_vol)
            
        if self.sma_signals[0]==-1 and self.position:
            self.order=self.close()
            self.order=self.sell(size=sell_vol)
#     def stop(self):
# #         global MinMomentum, MaxMomentume
#         print("when period_long={}, period_short={}, the final porfolio value of this strategy is {}".format(self.p.period_long, self.p.period_short, self.broker.getvalue()))

    # def stop(self):
    #     print("when period={}, the final porfolio value of this strategy is {}".format(self.p.period, self.broker.getvalue()))


from multiprocessing import Process
import multiprocessing
from multiprocessing import Semaphore

global dfResults
dfResults=pd.DataFrame(columns=['ticker', 'min_1', 'max_1', 'var_1', 'max_1_peroids','buyHold_1','maxDrawBack'])#, 'min_1_periods', 'min_2', 'max_2', 'var_2','max_2_peroids', 'min_2_periods'])
def f(x, return_dict):
    return_dict[x]=x

def download(stock, return_dict):
    print("start the process of", stock)
    global dfResults
    df3 = yf.download([stock], start = "2018-01-01", end = "2019-01-01")
    try:
        df3 = df3.div(df3['Open'][0])
    except:
        return None
    # buyHoldSharpe= np.log((df3['Close']/df3['Close'].shift(1)).dropna()).std()*np.sqrt(252)
#     print(buyHoldSharpe)
#     print("If we simply buy and hold, then the total return would be {}%".format(100*(df3['Open'][-1]-1)/1))
    resultThisStock=[]
    for period_short in range(1,20,2):
        for period_long in range(50,200,10):
            cerebro3=bt.Cerebro()
            cerebro3.addstrategy(SMA, period_long=period_long, period_short=period_short)
            IBM_day=bt.feeds.PandasData(dataname=df3,
                                        fromdate=datetime(2018,1,1),
                                        todate=datetime(2019,1,1),
                                        timeframe=bt.TimeFrame.Days)
            cerebro3.adddata(IBM_day)
    #         cerebro3.addanalyzer(bt.analyzers.SharpeRatio)
            cerebro3.addanalyzer(bt.analyzers.SharpeRatio)
            cerebro3.addanalyzer(bt.analyzers.DrawDown)
            cerebro3.addanalyzer(bt.analyzers.TimeReturn)
            cerebro3.addanalyzer(bt.analyzers.TradeAnalyzer)
            Res=cerebro3.run()[0]
            resultThisStock.append((cerebro3.broker.get_value(), period_short, period_long, Res.analyzers.drawdown.get_analysis()['max']['drawdown']))
#             print(Res.analyzers.sharperatio.get_analysis()['sharperatio'])   
#             print(Res.analyzers.drawdown.get_analysis())
    Min=min(resultThisStock)
    Max=max(resultThisStock)
    std=np.array([x[0] for x in resultThisStock]).std()
    std/10000
    new_row=pd.DataFrame([[stock, Min[0]/10000-1, Max[0]/10000-1,std/100, (Max[1], Max[2]), 100*(df3['Open'][-1]-1)/1, Max[3]]], columns=['ticker', 'min_1', 'max_1', 'var_1', 'max_1_peroids','buyHold_1','maxDrawBack'])
    return_dict[stock]=new_row
    time.sleep(2)
    # print("finished")
    # sema.release()

    
if __name__ == "__main__":
     
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    # sema = Semaphore(12)

    
    # stocksList=pd.read_csv('nasdaq_list.csv')
    stocksList=pd.read_csv('nasdaq_list.csv')
    BigCapStocksList=stocksList[stocksList['Market Cap']>5*10**9]['Symbol']
    tickers=BigCapStocksList
    taskQueue=[]
    for symbol in tickers:
        # if symbol in dfResults['ticker']:
        #     continue
        # try:  
            # if stock not in dfResults['ticker']:
            #     dfResults=pd.concat([dfResults, new_row])
        q=Process(target=download, args=(symbol,return_dict))
        taskQueue.append(q)
        q.start()
        print("Finished: {}".format(symbol))
        # except:
            # None
    for task in taskQueue:
        # task.start()
        task.join()
        
    for key,item in return_dict.items():
        dfResults=pd.concat([dfResults, item])
    dfResults.to_csv("BigCapMomentum2018.csv")
# df3 = yf.download(['AAPL'], start = "2015-01-01", end = "2020-01-01")
# df3 = df3.div(df3['Open'][0])
# df3.head(3)

# cerebro4=bt.Cerebro()
# IBM_day=bt.feeds.PandasData(dataname=df3,
#                             fromdate=datetime(2018,1,1),
#                             todate=datetime(2020,1,1),
#                             timeframe=bt.TimeFrame.Days)
# cerebro4.adddata(IBM_day)
# # cerebro4.addstrategy(SMA)
# cerebro4.optstrategy(SMA,period=range(5,7) )
# cerebro4.run()
