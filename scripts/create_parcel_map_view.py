import geopandas as gpd
import pandas as pd
import sqlite3
from pathlib import Path


GPKG = Path(
    "output/HRTK_Land_Data.gpkg"
)


conn = sqlite3.connect(GPKG)


# Load geometry

geometry = gpd.read_file(
    GPKG,
    layer="parcel_geometry"
)


# Load parcel table

parcels = pd.read_sql_query(
    "SELECT * FROM parcels",
    conn
)


conn.close()



# Ensure same datatype

geometry["parcel_id"] = (
    geometry["parcel_id"]
    .astype(int)
)


parcels["id"] = (
    parcels["id"]
    .astype(int)
)



# Join geometry + parcel data

result = geometry.merge(
    parcels,
    left_on="parcel_id",
    right_on="id",
    how="left"
)



result.to_file(
    GPKG,
    layer="parcel_map_view",
    driver="GPKG"
)


print(
    "Created parcel_map_view"
)

print(
    "Records:",
    len(result)
)