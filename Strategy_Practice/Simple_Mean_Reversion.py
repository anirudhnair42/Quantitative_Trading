
#%%

from zipline import run_algorithm
from zipline.api import order_target_percent, symbol
from datetime import datetime
import pytz
import matplotlib.pyplot as plt

import pandas as pd

#%%

def initialize(context):
    context.stock = symbol("AAPL")
    context.index_average_window = 100
#%%
def handle_data(context, data):
    equities_hist = data.history(symbol("AAPL"), "close", 100, "1d")
    
    if equities_hist[-1] > equities_hist.mean():
        stock_weight = 1.0
    else:
        stock_weight = 0.0
    
    order_target_percent(symbol("AAPL"), stock_weight)
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
%%time
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
