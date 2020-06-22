import requests
from bs4 import BeautifulSoup


def real_time_price(ticker):

    r = requests.get("https://finance.yahoo.com/quote/" + ticker + "/")

    soup = BeautifulSoup(r.text, "lxml")

    div = soup.find("div", class_="My(6px) Pos(r) smartphone_Mt(6px)")
    close_price = div.find("span").text
    if close_price == []:
        close_price = "999999"

    return close_price


for i in range(1, 4):
    close_price = real_time_price("TSLA")
    print(close_price)
