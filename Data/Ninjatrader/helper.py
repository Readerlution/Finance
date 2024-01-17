# %%
import polars as pl

# %%

def wrangle(csvfile):
    data = pl.read_csv(f"{csvfile}", has_header=False, separator=";")
    l1_cols = ["Level", "dtype", "Timestamp", "nano_ie7", "Price", "Volume"]
    l2_cols = ["Level", "dtype", "Timestamp", "nano_ie7", "Ops", "Position", "MarketMaker", "Price", "Volume"]
    df_l1 = data.filter(pl.col("column_1") == "L1").select(data.columns[:6])
    df_l2 = data.filter(pl.col("column_1") == "L2")

    df_l1.columns = l1_cols
    df_l2.columns = l2_cols
    df_l2.drop_in_place("MarketMaker")

    return [df_l1, df_l2]

# %%
import os

folder = r"D:\Finance\Data\Ninjatrader"
for f in os.listdir(folder+ "/replay_csv/CL 02-24"):
    inpath = folder + f"/replay_csv/CL 02-24/{f}"
    df_l1, df_l2 = wrangle(inpath)

    outpath = folder + f"/replay_feather/{f.rsplit('.')[0]}"
    df_l1.write_ipc(f"{outpath}_l1.arrow")
    df_l2.write_ipc(f"{outpath}_l2.arrow")
