from pathlib import Path
import sqlite3
import pandas as pd


# HRTK demo database
DB = Path(
    "../Haryana-Revenue-Toolkit/demo/database/hrtk_demo.db"
)


OUTPUT = Path(
    "output"
)

OUTPUT.mkdir(
    exist_ok=True
)



def export_table(
    table_name
):

    """
    Export HRTK table to CSV.
    """

    conn = sqlite3.connect(
        DB
    )


    df = pd.read_sql_query(
        f"SELECT * FROM {table_name}",
        conn
    )


    conn.close()


    output_file = (
        OUTPUT /
        f"{table_name}.csv"
    )


    df.to_csv(
        output_file,
        index=False
    )


    print(
        "Exported:",
        output_file
    )



def main():

    tables = [
        "villages",
        "khewats",
        "owners",
        "ownerships",
        "parcels",
    ]


    for table in tables:

        export_table(
            table
        )


    print(
        "HRTK GIS export complete"
    )



if __name__ == "__main__":

    main()