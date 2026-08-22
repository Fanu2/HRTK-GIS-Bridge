import sqlite3
from pathlib import Path


GPKG = Path(
    "output/HRTK_Land_Data.gpkg"
)


conn = sqlite3.connect(GPKG)

cur = conn.cursor()


cur.execute("""
DROP TABLE IF EXISTS parcel_khewat_map;
""")


cur.execute("""
CREATE TABLE parcel_khewat_map (

    id INTEGER PRIMARY KEY,

    parcel_id INTEGER NOT NULL,

    khewat_id TEXT NOT NULL,

    relationship_type TEXT,

    remarks TEXT

);
""")


rows = [

    (1, "6ff3e180-0bcc-4e53-b047-6a644e977804"),
    (2, "6ff3e180-0bcc-4e53-b047-6a644e977804"),
    (3, "b57636b0-8baa-4899-b05e-274d2dea0279"),
    (4, "b57636b0-8baa-4899-b05e-274d2dea0279"),

]


for parcel_id, khewat_id in rows:

    cur.execute(
        """
        INSERT INTO parcel_khewat_map
        (
            parcel_id,
            khewat_id,
            relationship_type,
            remarks
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            parcel_id,
            khewat_id,
            "demo",
            "GIS bridge mapping"
        )
    )


conn.commit()

conn.close()


print("Created parcel_khewat_map")
print("Records:", len(rows))