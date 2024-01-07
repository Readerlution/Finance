# %%
from pykrx import stock
import numpy as np
import pandas as pd
import json
from datetime import datetime
import finplot as fplt
from io import StringIO
from time import time
import pyqtgraph as pg

with open("D:\Finance\Data\krx\KOSPI.json", "r") as f:
    ticker_dict = json.load(f)

with open("D:\Finance\Data\krx\KOSDAQ.json", "r") as f:
    ticker_dict.update(json.load(f))

# %%     Retreieve and set data
ticker = "하림"
df = stock.get_market_ohlcv(
    fromdate="20220102", 
    todate=datetime.today().strftime("%Y%m%d"), 
    ticker=ticker_dict[ticker],
    )
df["Range"] = df["고가"] - df["저가"]
df["RangePerVolume"] = (df["Range"] / df["거래량"]) * 100_000

df.index.name = "Date"

df.columns = ["Open", "High", "Low", "Close", "Volume", "Return", "Range", "RangePerVolume"]

# Mid
df["Mid"] = ((df["High"] + df["Low"]) / 2).round(2)

# Marker for increased RangePerVolume
rpv_up = df["RangePerVolume"].copy()
rpv_up.loc[rpv_up < rpv_up.shift()] = np.nan

# Mark extreme level of RangePerVolume
deciles = df["RangePerVolume"].quantile(np.linspace(0.1, 1.0, num=10))
extremes = df["RangePerVolume"].copy()
extremes.loc[extremes < deciles[0.9]] = np.nan

# %%   Plotting

# Create axes
ax, ax2, ax3 = fplt.create_plot(ticker, rows=3)

# Plot candle sticks
fplt.candlestick_ochl(df[["Open", "Close", "High", "Low"]], ax=ax)

# Volume on ax2
fplt.volume_ocv(df[["Open", "Close", "Volume"]], ax=ax2)

# Range per volume on ax3
fplt.volume_ocv(df[["Mid", "Close", "RangePerVolume"]], ax=ax3)
fplt.plot(rpv_up + 1, style="^", ax=ax3, color="#ea9134") # Marker for uptick
# Draw line for extreme level
fplt.add_line((df.index[0], deciles[0.9]), (df.index[-1], deciles[0.9]), color="#0000FF", ax=ax3)

ax3.setXLink(ax)  # Links ax3 to ax for scale

# %%    Additional functions
def place_line(x, y):
    pen=fplt._makepen(fplt.draw_line_color, style='.')
    ax.price_line = pg.InfiniteLine(angle=180, movable=False, pen=pen)
    x, = fplt._pdtime2index(ax, pd.Series([x])) # convert timestamp to x-index
    ax.price_line.setPos((x,0))
    ax.addItem(ax.price_line, ignoreBounds=True)

fplt.set_time_inspector(place_line, ax=ax, when='click')


# %%
fplt.show()


# %%
