import xarray as xr
import os
import shutil
import pandas as pd
#import fsspec

S3_ZARR_PATH = "s3://aodn-cloud-optimised/model_sea_level_anomaly_gridded_realtime.zarr"
LOCAL_ZARR_DIR= "gsla_90days.zarr"
LOCAL_PARQUET_PATH = "gsla_90days.parquet"
STORAGE_OPTION= {"anon": True}
TIME_RANGE= ("2011-09-01", "2011-12-12")

def load_zarr_metadata():
    print("Loading zarr metadata from S3:")
    #fs = fsspec.filesystem("s3", anon=True)
    ds = xr.open_zarr(S3_ZARR_PATH, storage_options={"anon": True}, consolidated=False)
    print("Dataset info:", ds)
    print("Variables:", list(ds.data_vars))
    print("Coordinates:", list(ds.coords))
    print("Time range:", ds.TIME.values.min(), "→", ds.TIME.values.max())
    return ds

def download_subset(ds):
    print(f"\n Selecting time range {TIME_RANGE}...")
    subset= ds.sel(TIME=slice(*TIME_RANGE))
    print("Shape of GSLA:", subset['GSLA'].shape)

    print(f"\n Saving to local Zarr folder: {LOCAL_ZARR_DIR}/")
    if os.path.exists(LOCAL_ZARR_DIR):
        shutil.rmtree(LOCAL_ZARR_DIR)
    subset.to_zarr(LOCAL_ZARR_DIR, mode="w")
    print("Zarr saved to local Zarr folder")

def check_local_zarr():
    print("\n Checking Zarr data locally...")
    ds = xr.open_zarr(LOCAL_ZARR_DIR)
    print(ds)

    #Dataset Summary
    gsla = ds['GSLA']
    print("GSLA mean:", float(gsla.mean().values))
    print("GSLA std:", float(gsla.std().values))
    print("GSLA median:", float(gsla.median().values))
    print("GSLA min:", float(gsla.min().values))
    print("GSLA max:", float(gsla.max().values))

    #Convert the entire 90-day dataset to a DataFrame for inspection
    print("\nConverting full GSLA dataset to DataFrame for inspection...")
    df = gsla.to_dataframe().reset_index()
    print("\n Sample 10 rows:")
    print(df.head(10))

    print(f"\n DataFrame shape: {df.shape[0]} rows × {df.shape[1]} columns")

def convert_to_parquet():
    print(f"\n Converting Zarr to Parquet (full 3 years)...")
    ds = xr.open_zarr(LOCAL_ZARR_DIR)

    df = ds[['GSLA']].to_dataframe().reset_index()

    #Ensure TIME is in datetime64[us] format
    if 'TIME' in df.columns:
        df = df[df["TIME"].notnull()]
        df = df[(df["TIME"] > '2011-09-01') & (df["TIME"] < '2011-12-12')]
        df["TIME"] = pd.to_datetime(df["TIME"]).astype('datetime64[us]')

    print("DataFrame shape before saving:", df.shape)
    df.to_parquet(LOCAL_PARQUET_PATH, index=False)
    print(f"Parquet file saved to: {LOCAL_PARQUET_PATH}")
    print("Size:", os.path.getsize(LOCAL_PARQUET_PATH) / 1e6, "MB")

def list_all_time():
    ds = xr.open_zarr(LOCAL_ZARR_DIR)
    time_values = ds['TIME'].values

    print(f"Tổng số thời điểm: {len(time_values)}")
    print("Danh ¡sách các TIME có trong Zarr:")
    for i, t in enumerate(time_values):
        print(f"{i+1}: {t}")


if __name__ == "__main__":
    ds = load_zarr_metadata()
    download_subset(ds)
    check_local_zarr()
    convert_to_parquet()
    list_all_time()



