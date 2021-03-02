
#%%
import talib as ta
from zipline.api import order_target, record, symbol, order_target_percent
import pandas as pd
import zipline
#%%

def initialize(context):
    stocklist = ["AAPL","FB","AMZN","NFLX"]

    context.stocks = [symbol(s) for s in stocklist]

    context.target_pcts = 1.0/len(context.stocks)

    context.low_rsi =  40
    context.high_rsi = 60


#%%

def handle_data(context, data):

    prices = data.history(context.stocks, 'close', 20,'1d')
    rsis = {}

    for stock in context.stocks:
        prices_array = pd.Series(prices[stock])
        #rsi = ta.RSI(prices[stock], timeperiod = 14)[-1]
        rsi = ta.RSI(prices_array.values, timeperiod = 14)[-1]
        rsis[stock] = rsi

        current_position = context.portfolio.positions[stock].amount

        if rsi > context.high_rsi and current_position > 0 and data.can_trade(stock):
            order_target(stock, 0)
        elif rsi < context.low_rsi and current_position == 0 and data.can_trade(stock):
            order_target(stock, context.target_pcts)

    record(aapl_rsi = rsis[symbol('AAPL')], fb_rsi = rsis[symbol('FB')], amzn_rsi = rsis[symbol('AMZN')], nflx_rsi = rsis[symbol('NFLX')])


# %%
def analyze(context, perf):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(311)
    ax.set_title('Strategy Results')
    ax.semilogy(perf['portfolio_value'], linestyle='-', label='Equity Curve', linewidth=3.0)
    ax.legend()
    ax.grid(False)
    
    ax = fig.add_subplot(312)
    ax.plot(perf['gross_leverage'],
            label = 'Exposure', linestyle='-', linewidth=1.0)
    ax.legend()
    ax.grid(True)
 
    ax = fig.add_subplot(313)
    ax.plot(perf['returns'], label='Returns', linestyle='-.', linewidth=1.0)
    ax.legend()
    ax.grid(True)


# %%
from datetime import datetime
import pytz
from zipline import run_algorithm

start_date = pd.Timestamp(datetime(2010, 1, 1, tzinfo=pytz.UTC))
end_date = pd.Timestamp(datetime(2018, 12, 31, tzinfo=pytz.UTC))

results = run_algorithm(
    start=start_date,
    end=end_date,
    initialize=initialize,
    analyze=analyze,
    handle_data=handle_data,
    capital_base=10000,
    data_frequency='daily',
    bundle='quandl',
    benchmark_returns=None
)
# %%
handle_data()
#per = zipline.run_algorithm(initialize=initialize, handle_data=handle_data, capital_base = 20000, start=pd.Timestamp('2014-01-01', tz='utc'), end= pd.Timestamp('2015-01-01', tz='utc'), bundle='quandl', analyze=False)
#print(per)
# %%
