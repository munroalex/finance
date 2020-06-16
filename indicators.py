import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def rsiFunc(prices, n=14):
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


df = pd.read_csv("stock_dfs/AAPL.csv")

df["200EMA"] = df.iloc[:, 6].ewm(span=200, adjust=False).mean()
df["26EMA"] = df.iloc[:, 6].ewm(span=26, adjust=False).mean()
df["12EMA"] = df.iloc[:, 6].ewm(span=12, adjust=False).mean()
df["MACD"] = df["12EMA"] - df["26EMA"]
df["RSI"] = rsiFunc(df.iloc[:, 6])

print(df.head)

plt.figure(figsize=[15, 10])
plt.grid(True)
plt.plot(df["Adj Close"], label="Price")
plt.plot(df["MACD"], label="MACD")
plt.plot(df["200EMA"], label="200EMA")
plt.plot(df["RSI"], label="RSI")

plt.legend(loc=2)
plt.show()
