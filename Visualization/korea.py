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
ticker = "삼성전자"
df = stock.get_market_ohlcv(
    fromdate="20220102", 
    todate=datetime.today().strftime("%Y%m%d"), 
    ticker=ticker_dict[ticker],
    )
df["Range"] = df["고가"] - df["저가"]
df["VolumePerRange"] = df["거래량"] / df["Range"]

df.index.name = "Date"

df.columns = ["Open", "High", "Low", "Close", "Volume", "Return", "Range", "VolumePerRange"]

# Mid
df["Mid"] = ((df["High"] + df["Low"]) / 2).round(2)



# Marker for increased VolumePerRange
vpr_up = df["VolumePerRange"].copy()
vpr_up.loc[vpr_up < vpr_up.shift()] = np.nan

# Mark extreme level of VolumePerRange
decile_vpr = df["VolumePerRange"].quantile(np.linspace(0.1, 1.0, num=10))
extreme_vpr = df["VolumePerRange"].copy()
extreme_vpr.loc[( extreme_vpr < decile_vpr[0.9] )|(extreme_vpr < extreme_vpr.shift())] = np.nan

# Marker for increased Volume
vol_up = df["Volume"].copy()
vol_up.loc[vol_up < vol_up.shift()] = np.nan

# Mark extreme level of Volume
decile_vol = df["Volume"].quantile(np.linspace(0.1, 1.0, num=10))
extreme_vol = df['Volume'].copy()
extreme_vol.loc[(extreme_vol < decile_vol[0.9])|(extreme_vol < extreme_vol.shift())] = np.nan

# Marker for increase in both VolumePerRange and Volume
all_markers = pd.concat([ vol_up, vpr_up , extreme_vol, extreme_vpr], axis=1).notna()
all_markers.columns = ["volup", "vprup", "volextreme", "vprextreme"]

# Make a series that satisfy the condition below
mark = (all_markers["volup"] & all_markers["vprup"] & 
    (all_markers["volextreme"] | all_markers["vprextreme"]))
reversals = df.copy() 
reversals.loc[mark==False] = np.nan

# TODO: Make gap markers


# %%   Plotting

# Create axes
ax, ax2, ax3 = fplt.create_plot(ticker, rows=3)

# Plot candle sticks
fplt.candlestick_ochl(df[["Open", "Close", "High", "Low"]], ax=ax)

# Volume on ax2
fplt.volume_ocv(df[["Open", "Close", "Volume"]], ax=ax2)
fplt.plot(vol_up + 1, style="^", ax=ax2, color="#ea9134") # Marker for uptick
fplt.plot(extreme_vol + 1, style="^", ax=ax2, color="#31eeee") # Marker for uptick extreme
# Draw line for extreme level
fplt.add_line((df.index[0], decile_vol[0.9]), (df.index[-1], decile_vol[0.9]), color="#0000FF", ax=ax2)

# Volume per range on ax3
fplt.volume_ocv(df[["Mid", "Close", "VolumePerRange"]], ax=ax3)
fplt.plot(vpr_up + 1, style="^", ax=ax3, color="#ea9134") # Marker for uptick
fplt.plot(extreme_vpr + 1, style="^", ax=ax3, color="#31eeee") # Marker for uptick extreme
# Draw line for extreme level
fplt.add_line((df.index[0], decile_vpr[0.9]), (df.index[-1], decile_vpr[0.9]), color="#0000FF", ax=ax3)

ax3.setXLink(ax)  # Links ax3 to ax for scale

# Mark reversal bars
reversal_marks = fplt.candlestick_ochl(reversals[["Open", "Close", "High", "Low"]], ax=ax)
reversal_marks.colors.update(dict(bull_body='#31eeee', bear_body='#31eeee'))

# %%
fplt.show()


# %%
