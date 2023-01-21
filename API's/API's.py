import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib.pyplot as plt
import datetime
from pycoingecko import CoinGeckoAPI
from mplfinance.original_flavor import candlestick2_ohlc


# Creating Dictionary and converting it to DataFrame

dict_ = {'a': [11, 21, 31], 'b': [12, 22, 32]}
df = pd.DataFrame(dict_)

# Some Operations that can be made via the Pandas API

# type(df)
# df.head()
# df.mean()

# REST API'S

# Accessing the CoinGeckoAPI and get data on BTC Value
cg = CoinGeckoAPI()
bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=30)

type(bitcoin_data)  # Must be a JSON

# Getting The Value of BTC assigning it to a DataFrame and Create a Date column

bitcoin_price_data = bitcoin_data['prices']
data = pd.DataFrame(bitcoin_price_data, columns=['TimeStamp', 'Price'])
data['date'] = data['TimeStamp'].apply(lambda d: datetime.date.fromtimestamp(d/1000.0))

# Finding Min, Max, Open and Close values

candlestick_data = data.groupby(data.date, as_index=False).agg({"Price": ['min', 'max', 'first', 'last']})

#Plotting the Values

fig = go.Figure(data=[go.Candlestick(x=candlestick_data['date'],
                open=candlestick_data['Price']['first'],
                high=candlestick_data['Price']['max'],
                low=candlestick_data['Price']['min'],
                close=candlestick_data['Price']['last'])
                ])

fig.update_layout(xaxis_rangeslider_visible=False)

fig.show()
