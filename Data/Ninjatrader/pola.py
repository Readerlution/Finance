# %%
import polars as pl
path = r"D:\Finance\Data\Ninjatrader\parquet\ES09-19_l1.parquet"

lf = pl.scan_parquet(path)
columns_replace = ['timestamp', 'timeoffset(n)', 'price', 'volume']
replace_map = dict(zip(lf.columns, columns_replace))
lf = (
    lf.rename(replace_map)
    .sort('timestamp')
    .with_columns(pl.col("timestamp")
                  .dt.replace_time_zone("Asia/Seoul")
                  .dt.convert_time_zone("America/New_York"))
)

# %%
df_ohlcv = lf.group_by_dynamic("timestamp", every="150s").agg([
    pl.col("price").first().alias("open"),
    pl.col("price").max().alias("high"),
    pl.col("price").min().alias("low"),
    pl.col("price").last().alias("close"),
    pl.col("volume").sum().alias("volume")
]).filter(pl.col("timestamp").cast(pl.Time).is_between(pl.time(9,30), pl.time(16)))

# %%
assert lf.select('timestamp').is_sorted(), \
    f"Expected timestamp to be in sequential order but it does not match"

# %%
pd_df = df_ohlcv.to_pandas().set_index('timestamp')[['open','high','low','close','volume']]

# %%
import finplot as fplt
ax = fplt.create_plot("Chart")
fplt.candlestick_ochl(pd_df[["open", "close", "high", "low"]], ax=ax)
fplt.show()
# %%