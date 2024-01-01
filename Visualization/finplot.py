# %%
from pykrx import stock
import numpy as np
import pandas as pd
import json
from datetime import datetime
# import finplot as fplt
from io import StringIO
from time import time

with open("D:\Finance\Data\KOSPI.json", "r") as f:
    ticker_dict = json.load(f)

with open("D:\Finance\Data\KOSDAQ.json", "r") as f:
    ticker_dict.update(json.load(f))

# %%
ticker = "삼성전자"
df = stock.get_market_ohlcv("20220102", datetime.today().strftime("%Y%m%d"), ticker_dict[ticker])
df["Range"] = df["고가"] - df["저가"]
df["RangePerVolume"] = (df["Range"] / df["거래량"]) * 100_000

df.index.name = "Date"

df.columns = ["Open", "High", "Low", "Close", "Volume", "%Change", "Range", "RangePerVolume"]

# %%
# fplt.candlestick_ochl(df[["Open", "Close", "High", "Low"]])
# fplt.show()

# %%
