import sqlite3
from pathlib import Path
import geopandas as gpd


GPKG = Path(
    "output/HRTK_Land_Data.gpkg"
)


TEMP_DB = Path(
    "output/land_view.db"
)


# Read GeoPackage tables
conn = sqlite3.connect(
    GPKG
)


query = """

SELECT

    p.id AS parcel_id,

    p.rectangle,

    p.killa,

    p.kanal,

    p.marla,

    p.sarsai,

    k.khewat_no,

    k.jamabandi_year,

    v.name AS village,

    v.tehsil,

    v.district,

    o.owner_name,

    o.father_name,

    ow.numerator,

    ow.denominator


FROM parcels p


LEFT JOIN ownerships ow
    ON 1=1


LEFT JOIN khewats k
    ON k.id = ow.khewat_id


LEFT JOIN owners o
    ON o.id = ow.owner_id


LEFT JOIN villages v
    ON v.id = k.village_id

"""


df = gpd.GeoDataFrame(
    gpd.pd.read_sql(
        query,
        conn
    )
)


conn.close()



# Write non spatial table into GeoPackage

df.to_file(
    GPKG,
    layer="land_view",
    driver="GPKG"
)


print(
    "Created: land_view"
)

print(
    "Records:",
    len(df)
)