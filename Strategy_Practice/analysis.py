#%%
import pickle
import pandas as pd
import pyfolio as pf

#%%
def process_performance(fname):
    perf = pd.read_pickle('{}.pickle'.format(fname))
    perf.to_csv('{}.csv'.format(fname))
    perf.index = perf.index.normalize()
    return perf


#%%
perf = process_performance('perf')
# %%
