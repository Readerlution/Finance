# %%
import pandas as pd
import numpy as np

# %%
data = pd.read_csv("replay_csv/CL 02-24/20231215.csv", delimiter=";", header=None, names=range(1,10))

# %%
"""
L1 data types
Ask = 0
Bid = 1
Last = 2
DailyHigh = 3
DailyLow = 4
DailyVolume = 5
LastClose = 6
Opening = 7
OpenInterest = 8
Settlement = 9
Unknown = 10

L2 data types
Ask = 0
Bid = 1
Last = 2
DailyHigh = 3
DailyLow = 4
DailyVolume = 5
LastClose = 6
Opening = 7
OpenInterest = 8
Settlement = 9
Unknown = 10

L2 Cbi.Operation
Add = 0
Update = 1
Remove = 2
"""
# %%
l1_cols = ["Level", "dtype", "Timestamp", "offset", "Price", "Volume"]
l2_cols = ["Level", "dtype", "Timestamp", "offset", "Ops", "Position", "MarketMaker", "Price", "Volume"]
df_l1 = data.loc[data[1]=="L1"][range(1,7)]
df_l2 = data.loc[data[1]=="L2"]

df_l1.columns = l1_cols
df_l2.columns = l2_cols
df_l2.drop(columns="MarketMaker", inplace=True)

# %%
