
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
        #prices_array = pd.Series(prices[stock])
        rsi = ta.RSI(prices[stock], timeperiod = 14)[-1]
        #rsi = ta.RSI(prices_array.values, timeperiod = 14)[-1]
        rsis[stock] = rsi

        current_position = context.portfolio.positions[stock].amount

        if rsi > context.high_rsi and current_position > 0 and data.can_trade(stock):
            order_target(stock, 0)
        elif rsi < context.low_rsi and current_position == 0 and data.can_trade(stock):
            order_target(stock, context.target_pcts)

    record(aapl_rsi = rsis[symbol('AAPL')], fb_rsi = rsis[symbol('FB')], amzn_rsi = rsis[symbol('AMZN')], nflx_rsi = rsis[symbol('NFLX')])


# %%
def analyze(context, perf):
    # Use PyFolio to generate a performance report
    returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(perf)
    pf.create_returns_tear_sheet(returns, benchmark_rets=None)
    
# %%
from datetime import datetime, timezone
import pytz
start_date = pd.Timestamp(datetime(2010, 1, 1, tzinfo=pytz.UTC))
end_date = pd.Timestamp(datetime(2018, 12, 31, tzinfo=pytz.UTC))
result = run_algorithm(
    start=start, 
    end=end, 
    initialize=initialize, 
    analyze=analyze, 
    capital_base=10000, 
    data_frequency = 'daily', 
    bundle='quandl' 
)

# %%
