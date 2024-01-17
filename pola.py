# %%
import polars as pl
path = r"D:\Finance\Data\Ninjatrader\replay_feather\CL\20231215_l1.arrow"

df = pl.read_ipc(path)
# %%
df = df.filter(pl.col("dtype") == 2)
df = df.drop(["dtype", "Level"])

# %%
df = df.with_columns(pl.col("Timestamp").cast(pl.Utf8).str.to_datetime('%Y%m%d%H%M%S'))

# %%
assert df["Timestamp"].shift().le(df["Timestamp"]).sum() == (len(df)-1), \
    f"Expected Timestamp to be in sequential order but it does not match"

# %%
df_ohlcv = df.set_sorted("Timestamp").group_by_dynamic("Timestamp", every="150s").agg([
    pl.col("Price").first().alias("open"),
    pl.col("Price").max().alias("high"),
    pl.col("Price").min().alias("low"),
    pl.col("Price").last().alias("close"),
    pl.col("Volume").sum().alias("volume")
])
# %%

# %%
pd_df = df_ohlcv.to_pandas().set_index('Timestamp')[['open','high','low','close','volume']]

# %%
import finplot as fplt

# %%

ax = fplt.create_plot("Crude Oil")
fplt.candlestick_ochl(pd_df[["open", "close", "high", "low"]], ax=ax)
# %%
fplt.show()
# %%
