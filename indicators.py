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


stock = input("Choose stock to test:")
df = pd.read_csv("stock_dfs/" + str(stock) + ".csv")

df["200EMA"] = df.iloc[:, 6].ewm(span=200, adjust=False).mean()
df["26EMA"] = df.iloc[:, 6].ewm(span=26, adjust=False).mean()
df["12EMA"] = df.iloc[:, 6].ewm(span=12, adjust=False).mean()
df["MACD"] = df["12EMA"] - df["26EMA"]
df["RSI"] = rsiFunc(df.iloc[:, 6])

position = 0
number = 0
percent_change = []
buy = 0
for i in df.index:
    close = df["Adj Close"][i]
    mcd = df["MACD"][i]
    rsi = df["RSI"][i]
    if mcd < 0:
        if rsi < 30:
            buy = close
            position = 1
            print("Buying at " + str(buy))

    elif mcd > 0:
        if position == 1:
            sell = close
            position = 0
            print("Selling at " + str(sell))
            change = ((sell / buy) - 1) * 100
            percent_change.append(change)
    if number == df["Adj Close"].count() - 1 and position == 1:
        position = 0
        sell = close
        print("Selling at " + str(sell))
        change = ((sell / buy) - 1) * 100
        percent_change.append(change)
    number += 1

print(percent_change)
print(sum(percent_change))

gains = 0
number_of_gains = 0
losses = 0
number_of_losses = 0
total_returns = 1

for i in percent_change:
    if i > 0:
        gains += i
        number_of_gains += 1
    else:
        losses += i
        number_of_losses += 1
    total_returns = total_returns * ((i / 100) + 1)

total_returns = round((total_returns - 1) * 100, 2)

print("Gains:" + str(gains))
print("Number of wins:" + str(number_of_gains))
print("Losses:" + str(losses))
print("Number of losers:" + str(number_of_losses))
print("Total Returns:" + str(total_returns))

if number_of_gains > 0:
    avgGain = gains / number_of_gains
    maxR = str(max(percent_change))
else:
    avgGain = 0
    maxR = "undefined"

if number_of_losses > 0:
    avgLoss = losses / number_of_losses
    maxL = str(min(percent_change))
    ratio = str(-avgGain / avgLoss)
else:
    avgLoss = 0
    maxL = "undefined"
    ratio = "inf"

if number_of_gains > 0 or number_of_losses > 0:
    battingAvg = number_of_gains / (number_of_gains + number_of_losses)
else:
    battingAvg = 0
weekly_returns = 

#ADD PERCENTAGE TAKE PROFIT AND STOP LOSS


print()
print(
    "Results for "
    + stock
    + " going back to "
    + str(df.index[0])
    + ", Sample size: "
    + str(number_of_gains + number_of_losses)
    + " trades"
)
print("Number of days: " + str(df["Adj Close"].count()))
print("Weekly returns: " + (str(df["Adj Close"].count()))
print("Batting Avg: " + str(battingAvg))
print("Gain/loss ratio: " + ratio)
print("Average Gain: " + str(avgGain))
print("Average Loss: " + str(avgLoss))
print("Max Return: " + maxR)
print("Max Loss: " + maxL)
print(
    "Total return over "
    + str(number_of_gains + number_of_losses)
    + " trades: "
    + str(total_returns)
    + "%"
)
# print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )
print()
""" plt.figure(figsize=[15, 10])
plt.grid(True)
plt.plot(df["Adj Close"], label="Price")
plt.plot(df["MACD"], label="MACD")
plt.plot(df["200EMA"], label="200EMA")
plt.plot(df["RSI"], label="RSI")

plt.legend(loc=2)
plt.show() """
