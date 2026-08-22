from pathlib import Path
import sqlite3

import pandas as pd
import geopandas as gpd



DB = Path(
    "../Haryana-Revenue-Toolkit/demo/database/hrtk_demo.db"
)


OUTPUT = Path(
    "output"
)

OUTPUT.mkdir(
    exist_ok=True
)


GPKG = OUTPUT / "HRTK_Land_Data.gpkg"



def read_table(
    table_name
):

    conn = sqlite3.connect(
        DB
    )

    df = pd.read_sql_query(
        f"SELECT * FROM {table_name}",
        conn
    )

    conn.close()

    return df



def export_csv(
    table_name
):

    df = read_table(
        table_name
    )

    df.to_csv(
        OUTPUT / f"{table_name}.csv",
        index=False
    )

    print(
        "CSV:",
        table_name
    )



def export_geopackage():

    """
    Create QGIS compatible package.

    Current HRTK database has
    revenue attributes only.
    Geometry will be added later.
    """


    tables = [
        "villages",
        "khewats",
        "owners",
        "ownerships",
        "parcels",
    ]


    if GPKG.exists():

        GPKG.unlink()



    for table in tables:

        df = read_table(
            table
        )


        gdf = gpd.GeoDataFrame(
            df
        )


        gdf.to_file(
            GPKG,
            layer=table,
            driver="GPKG"
        )


        print(
            "GPKG:",
            table
        )



def main():


    for table in [
        "villages",
        "khewats",
        "owners",
        "ownerships",
        "parcels",
    ]:

        export_csv(
            table
        )


    export_geopackage()


    print(
        "HRTK GIS export complete"
    )



if __name__ == "__main__":

    main()