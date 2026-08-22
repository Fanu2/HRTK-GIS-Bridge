"""
Create Clean Parcel Land View

Purpose:
--------
Creates the user-facing QGIS layer from
parcel_land_view.

Removes technical database fields and keeps
only meaningful land information.
"""


import geopandas as gpd
from pathlib import Path
import subprocess


GPKG = Path(
    "output/HRTK_Land_Data.gpkg"
)


SOURCE_LAYER = "parcel_land_view"

OUTPUT_LAYER = "parcel_land_view_clean"



# -------------------------------------------------
# Load existing spatial intelligence layer
# -------------------------------------------------

gdf = gpd.read_file(
    GPKG,
    layer=SOURCE_LAYER
)



# -------------------------------------------------
# Select user-facing fields
# -------------------------------------------------

keep_fields = [

    "geometry",

    # Parcel
    "parcel_id",
    "rectangle",
    "killa",
    "kanal",
    "marla",
    "sarsai",

    # Khewat
    "khewat_no",
    "jamabandi_year",

    # Ownership
    "numerator",
    "denominator",

    # Owner
    "owner_code",
    "owner_name",
    "father_name",
    "address"

]


clean = gdf[
    [
        field
        for field in keep_fields
        if field in gdf.columns
    ]
]



# -------------------------------------------------
# Remove old output layer
# -------------------------------------------------

temp = Path(
    "output/temp_clean_land_view.gpkg"
)


if temp.exists():
    temp.unlink()



# -------------------------------------------------
# Write clean layer
# -------------------------------------------------

clean.to_file(
    temp,
    layer=OUTPUT_LAYER,
    driver="GPKG"
)



# -------------------------------------------------
# Replace layer in main GeoPackage
# -------------------------------------------------

subprocess.run(
    [
        "ogr2ogr",
        "-f",
        "GPKG",
        str(GPKG),
        str(temp),
        "-nln",
        OUTPUT_LAYER,
        "-overwrite"
    ],
    check=True
)



temp.unlink(
    missing_ok=True
)



print(
    "Created:",
    OUTPUT_LAYER
)

print(
    "Records:",
    len(clean)
)

print(
    "Fields:"
)

for field in clean.columns:
    print(
        " -",
        field
    )