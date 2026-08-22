import sqlite3
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Polygon


GPKG = Path(
    "output/HRTK_Land_Data.gpkg"
)


# Demo parcel polygons
records = []


parcels = [
    (1, "101", "1"),
    (2, "101", "2"),
    (3, "102", "1"),
    (4, "102", "2"),
]


for parcel_id, rectangle, killa in parcels:

    x = parcel_id * 0.01

    polygon = Polygon([
        (x, 0),
        (x + 0.008, 0),
        (x + 0.008, 0.008),
        (x, 0.008),
        (x, 0)
    ])

    records.append(
        {
            "parcel_id": parcel_id,
            "rectangle": rectangle,
            "killa": killa,
            "geometry": polygon
        }
    )


gdf = gpd.GeoDataFrame(
    records,
    crs="EPSG:4326"
)


gdf.to_file(
    GPKG,
    layer="parcel_geometry",
    driver="GPKG"
)


print("Created parcel_geometry")
print("Records:", len(gdf))