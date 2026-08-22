import sqlite3
from pathlib import Path


GPKG = Path(
    "output/HRTK_Land_Data.gpkg"
)


KEEP = {
    "parcel_land_view_clean",
    "villages",
    "khewats",
    "owners",
    "ownerships",
    "parcels"
}


conn = sqlite3.connect(GPKG)

tables = conn.execute(
    """
    SELECT table_name
    FROM gpkg_contents
    """
).fetchall()


for (table,) in tables:

    if table not in KEEP and not table.startswith("gpkg_"):

        print(
            "Removing:",
            table
        )

        conn.execute(
            f'DROP TABLE IF EXISTS "{table}"'
        )


conn.commit()
conn.close()


print("GeoPackage cleaned")