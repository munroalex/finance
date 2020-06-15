import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

# yahoo finance workaround
yf.pdr_override()

year = 2018
month = 1
day = 1

start = dt.datetime(year, month, day)
now = dt.datetime.now()


ticker = input("Enter Ticker: ")
csv_df = pd.read_csv("sp500_joined_closes.csv")
df = pdr.get_data_yahoo(ticker, start, now)

df["26EMA"] = df.iloc[:, 4].ewm(span=26, adjust=False).mean()

df["12EMA"] = df.iloc[:, 4].ewm(span=12, adjust=False).mean()

df["MACD"] = df["12EMA"] - df["26EMA"]
print(df.head)


plt.figure(figsize=[15, 10])
plt.grid(True)
plt.plot(df["Adj Close"], label="Price")
plt.plot(df["MACD"], label="MACD")

plt.legend(loc=2)
plt.show()
