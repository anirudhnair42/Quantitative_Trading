#%%
!zipline ingest -b quantopian-quandl
# %%

# %%
%%zipline --start 2015-1-1 --end 2018-1-1 --capital-base 10000.0 -o rsi.pkl 

# imports ----
from zipline.api import order_target, record, symbol, set_commission, order_percent, set_benchmark, order_target_percent, set_slippage
from zipline.finance import commission
import talib as ta


def initialize(context):

  # Stocks to trade
  stock_list = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOGL']
  context.stocks = [symbol(stock) for stock in stock_list]

  # How much of the portfolio is invested in each stock (20% each)
  context.target_pct_per_stock = 1 / len(context.stocks)

  # Transaction costs
  #context.set_commission(commission.PerShare(cost=0.0, min_trade_cost=0))
  #context.set_commission(commission.PerDollar(cost=0.0015)) # default is 0.0015
  #context.set_commission(commission.PerTrade(cost=0.0))

  # Slippage
  #context.set_slippage(slippage.VolumeShareSlippage())

  # Upper and Lower bound for RSI trading signals
  context.low_rsi = 30
  context.high_rsi = 70

  # Moving average window
  #context.index_average_window = 100

  set_benchmark(False)

def handle_data(context, data):

  # Historical data
  prices = data.history(context.stocks, 'price', bar_count=20, frequency='1d')
  
  rsis = {}

  # Loop thru the stocks and determine when to buy and sell them
  for stock in context.stocks:
    rsi = ta.RSI(prices[stock], timeperiod=14)[-1]
    rsis[stock] = rsi
  
    current_position = context.portfolio.positions[stock].amount

    if rsi > context.high_rsi and current_position > 0 and data.can_trade(stock):
      order_target(stock, 0)
    elif rsi < context.low_rsi and current_position == 0 and data.can_trade(stock):
      order_target_percent(stock, context.target_pct_per_stock)

  
  record(fb_rsi=rsis[symbol('FB')],
         amzn_rsi=rsis[symbol('AMZN')],
         aapl_rsi=rsis[symbol('AAPL')],
         nflx_rsi=rsis[symbol('NFLX')],
         googl_rsi=rsis[symbol('GOOGL')])

# %%
# Plotting tear sheet (simple/extended)
import pandas as pd
import pyfolio as pf
import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook
warnings.simplefilter('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=matplotlib.cbook.mplDeprecation)

#rsi = pd.read_pickle("rsi.pkl")
#pf.create_simple_tear_sheet(rsi.returns);
#pf.create_returns_tear_sheet(rsi.returns);
#pf.create_full_tear_sheet(rsi.returns);

def process_performance(fname):
    perf = pd.read_pickle('{}.pkl'.format(fname))
    perf.to_csv('{}.csv'.format(fname))
    # Normalize the dates
    perf.index = perf.index.normalize()
    return perf

def create_benchmark(fname):
    # benchmark_rets (pd.Series, optional) -- Daily noncumulative returns of the benchmark. This is in the same style as returns.
    dir = 'https://raw.githubusercontent.com/quantopian/zipline/master/zipline/resources/market_data/'
    bench = pd.read_csv(dir+'{}.csv'.format(fname), index_col='date', parse_dates=True, date_parser=lambda col: pd.to_datetime(col, utc=True))
    # Create a series
    bench_series = pd.Series(bench['return'].values, index=bench.index)
    bench_series.rename(fname, inplace=True)
    return bench_series

# Use PyFolio to generate a performance report - benchmark_rets is optional
def analyze(perfdata, benchdata):
    returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(perfdata)
    # pf.create_full_tear_sheet(returns, positions=positions, transactions=transactions, benchmark_rets=benchdata)
    pf.create_returns_tear_sheet(returns, benchmark_rets=benchdata)


# Create the performance dataframe
perf = process_performance('rsi')

# Create a benchmark dataframe
bench_series = create_benchmark('SPY_benchmark')

# Filter for the dates in returns to line up the graphs - normalize cleans up the dates
bench_series = bench_series[bench_series.index.isin(perf.index)]

# Run the tear sheet analysis
analyze(perf, bench_series)
# %%
