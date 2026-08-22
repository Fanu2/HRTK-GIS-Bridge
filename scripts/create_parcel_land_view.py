"""
Create HRTK Parcel Land View

Purpose:
--------
Creates a GIS-ready spatial layer by combining:

parcel_geometry
        |
        v
parcels
        |
        v
parcel_khewat_map
        |
        v
khewats
        |
        v
ownerships
        |
        v
owners


Output:
-------
parcel_land_view

This layer is intended for QGIS display.

Design rule:
------------
HRTK core database remains unchanged.
All GIS relationships are handled in HRTK-GIS-Bridge.
"""


import geopandas as gpd
import pandas as pd
import sqlite3
from pathlib import Path
import subprocess



# -------------------------------------------------
# Configuration
# -------------------------------------------------

GPKG = Path(
    "output/HRTK_Land_Data.gpkg"
)

OUTPUT_LAYER = "parcel_land_view"

TEMP_GPKG = Path(
    "output/temp_parcel_land_view.gpkg"
)



# -------------------------------------------------
# Load spatial layer
#
# parcel_geometry is the only table containing
# actual map geometry.
# -------------------------------------------------

geometry = gpd.read_file(
    GPKG,
    layer="parcel_geometry"
)



# -------------------------------------------------
# Load attribute tables
# -------------------------------------------------

conn = sqlite3.connect(
    GPKG
)


try:

    parcels = pd.read_sql_query(
        "SELECT * FROM parcels",
        conn
    )


    parcel_khewat = pd.read_sql_query(
        "SELECT * FROM parcel_khewat_map",
        conn
    )


    khewats = pd.read_sql_query(
        "SELECT * FROM khewats",
        conn
    )


    ownerships = pd.read_sql_query(
        "SELECT * FROM ownerships",
        conn
    )


    owners = pd.read_sql_query(
        "SELECT * FROM owners",
        conn
    )

finally:

    conn.close()



# -------------------------------------------------
# Normalize relationship keys
#
# SQLite is flexible with types.
# Pandas merge requires matching types.
# -------------------------------------------------

geometry["parcel_id"] = (
    geometry["parcel_id"].astype(int)
)


parcels["id"] = (
    parcels["id"].astype(int)
)


parcel_khewat["parcel_id"] = (
    parcel_khewat["parcel_id"].astype(int)
)


parcel_khewat["khewat_id"] = (
    parcel_khewat["khewat_id"].astype(str)
)


khewats["id"] = (
    khewats["id"].astype(str)
)


ownerships["khewat_id"] = (
    ownerships["khewat_id"].astype(str)
)


ownerships["owner_id"] = (
    ownerships["owner_id"].astype(int)
)


owners["id"] = (
    owners["id"].astype(int)
)



# -------------------------------------------------
# Build land intelligence view
# -------------------------------------------------

# Geometry + parcel details

result = geometry.merge(
    parcels,
    left_on="parcel_id",
    right_on="id",
    how="left",
    suffixes=("", "_parcel")
)



# Parcel -> Khewat bridge

result = result.merge(
    parcel_khewat,
    on="parcel_id",
    how="left"
)



# Khewat information

result = result.merge(
    khewats,
    left_on="khewat_id",
    right_on="id",
    how="left",
    suffixes=("", "_khewat")
)



# Khewat -> Ownership

result = result.merge(
    ownerships,
    on="khewat_id",
    how="left",
    suffixes=("", "_ownership")
)



# Ownership -> Owner

result = result.merge(
    owners,
    left_on="owner_id",
    right_on="id",
    how="left",
    suffixes=("", "_owner")
)



# -------------------------------------------------
# Cleanup generated fields
# -------------------------------------------------

result = result.reset_index(drop=True)


if "fid" in result.columns:

    result = result.drop(
        columns=["fid"]
    )



# -------------------------------------------------
# Remove previous temporary output
# -------------------------------------------------

if TEMP_GPKG.exists():

    TEMP_GPKG.unlink()



# -------------------------------------------------
# Write new layer
# -------------------------------------------------

result.to_file(
    TEMP_GPKG,
    layer=OUTPUT_LAYER,
    driver="GPKG"
)



# -------------------------------------------------
# Replace existing layer in main GeoPackage
#
# GDAL handles GeoPackage metadata correctly.
# -------------------------------------------------

subprocess.run(
    [
        "ogr2ogr",
        "-f",
        "GPKG",
        str(GPKG),
        str(TEMP_GPKG),
        "-nln",
        OUTPUT_LAYER,
        "-overwrite"
    ],
    check=True
)



# -------------------------------------------------
# Remove temporary file
# -------------------------------------------------

TEMP_GPKG.unlink(
    missing_ok=True
)



# -------------------------------------------------
# Report result
# -------------------------------------------------

print(
    "Created:",
    OUTPUT_LAYER
)

print(
    "Records:",
    len(result)
)

print(
    "Columns:"
)

for column in result.columns:

    print(
        " -",
        column
    )