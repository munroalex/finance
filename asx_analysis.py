import requests, csv, os
from bs4 import BeautifulSoup
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
from pathlib import Path
import numpy as np


yf.pdr_override


def rsi_Func(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[: n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100.0 - 100.0 / (1.0 + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]  # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.0
        else:
            upval = 0.0
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        rsi[i] = 100.0 - 100.0 / (1.0 + rs)

    return rsi


def get_tickers():

    alphabet = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    tickers = []
    for i in alphabet:
        r = requests.get(
            "https://www.asx.com.au/asx/research/listedCompanies.do?coName=" + i
        )

        soup = BeautifulSoup(r.text, "lxml")

        table = soup.find("table", class_="contenttable")
        for row in table.findAll("tr")[2:]:
            ticker = row.findAll("td")[1].text
            tickers.append(ticker)
    print(" Got " + str(len(tickers)) + "tickers")
    with open("asx_tickers.csv", "w") as myfile:
        wr = csv.writer(myfile)
        wr.writerow(tickers)
    return tickers


get_tickers()


def get_historical_data():
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime.now()

    tickers = pd.read_csv("asx_tickers.csv")
    num = 1
    if not os.path.exists("stock_dfs"):
        os.makedirs("stock_dfs")
    print("Getting historical data.")
    for ticker in tickers:
        try:
            print(str(num) + ":" + ticker)
            df = pdr.get_data_yahoo(ticker + ".AX", start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df.to_csv("stock_dfs/{}.csv".format(ticker))
            num = num + 1
        except:
            pass


get_historical_data()


def add_indicators():
    folder = "stock_dfs"
    for ticker in Path(folder).glob("*.csv"):
        print("Adding indicators: " + str(ticker))
        df = pd.read_csv(ticker)
        try:
            df["200EMA"] = df.iloc[:, 6].ewm(span=200, adjust=False).mean()
            df["26EMA"] = df.iloc[:, 6].ewm(span=26, adjust=False).mean()
            df["12EMA"] = df.iloc[:, 6].ewm(span=12, adjust=False).mean()
            df["MACD"] = df["12EMA"] - df["26EMA"]
            df["SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()
            df["RSI"] = rsi_Func(df.iloc[:, 6])
            df["DV"] = df["Volume"] * df["Close"]
            df["DV15"] = df["DV"].ewm(span=15, adjust=False).mean()
            df["PCT_CHANGE"] = df["Adj Close"].pct_change() 
            df.to_csv("{}".format(ticker))
        except:
            pass


add_indicators()


def check_criteria():
    folder = "stock_dfs"
    num = 0
    for ticker in Path(folder).glob("*.csv"):
        df = pd.read_csv(ticker)
        df = df.tail()
        if len(df) != 0:
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df.loc[df["RSI"] < 30, "OVERSOLD"] = "True"
            df = df.drop(columns=["index", "Unnamed: 0"])
            df.dropna(subset=["OVERSOLD"], inplace=True)
            average_dv = df["DV"].mean()
            try:
                if df["OVERSOLD"].any():
                    if average_dv > 2186778:
                        if (df["MACD"] < 0).any():
                            if (df["DV15"] > average_dv).any():
                                print(ticker)
                                print(df)
                                num = num + 1
            except:
                pass
    print(num)


check_criteria()
