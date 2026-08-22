import sqlite3
from pathlib import Path


GPKG = Path(
    "output/HRTK_Land_Data.gpkg"
)


REMOVE = [
    "parcel_geometry",
    "parcel_map_view",
    "parcel_land_view",
    "land_view",
]


conn = sqlite3.connect(GPKG)


for table in REMOVE:

    print(
        "Cleaning metadata:",
        table
    )

    conn.execute(
        """
        DELETE FROM gpkg_contents
        WHERE table_name = ?
        """,
        (table,)
    )


    conn.execute(
        """
        DELETE FROM gpkg_geometry_columns
        WHERE table_name = ?
        """,
        (table,)
    )


conn.commit()
conn.close()


print(
    "GeoPackage metadata fixed"
)