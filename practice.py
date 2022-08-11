import pandas as pd
import numpy as np
import yfinance as yf
import quandl
import matplotlib.pyplot as plt

df = yf.download(
    'AAPL',
    start='2000-01-01',
    end='2010-12-31',
    progress=False
)
df = df.loc[:, ['Adj Close']]
df.rename(columns={'Adj Close': 'adj_close'}, inplace=True)

df['simple_rtn'] = df.adj_close.pct_change()
df['log_rtn'] = np.log(df.adj_close/df.adj_close.shift(1))

# QUANDL_KEY = '88Tz7sQta_7w6-1w3mZM'
# quandl.ApiConfig.api_key = QUANDL_KEY

# df_all_dates = pd.DataFrame(index=pd.date_range(start='1999-12-31', end='2010-12-31'))
# df = df_all_dates.join(df[['adj_close']], how='left').fillna(method='ffill').asfreq('M')

# df_cpi = quandl.get(
#     dataset='RATEINF/CPI_USA',
#     start_date='1999-12-01',
#     end_date='2010-12-31'
# )
# df_cpi.rename(columns={'Value':'cpi'}, inplace=True)

# df_merged = df.join(df_cpi, how='left')

# df_merged['simple_rtn'] = df_merged.adj_close.pct_change()
# df_merged['inflation_rate'] = df_merged.cpi.pct_change()

# df_merged['real_rtn'] = (df_merged.simple_rtn + 1) / (df_merged.inflation_rate + 1) - 1

# The adjusted close price differs from the book's data.
# df_merged['adj_close'] *= 3.194901 / df_merged['adj_close'][0]

def realized_volatility(x):
    return np.sqrt(np.sum(x ** 2))

print(df)
df_rv = df.groupby(pd.Grouper(freq='M')).apply(realized_volatility)
df_rv.rename(columns={'log_rtn': 'rv'}, inplace=True)
df_rv.rv *= np.sqrt(12)

fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(df.log_rtn)
ax[1].plot(df_rv.rv)

