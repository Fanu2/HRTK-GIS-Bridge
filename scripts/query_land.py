"""
HRTK GIS Bridge - Land Query Tool

Purpose:
--------
Read-only search interface for HRTK_Land_Data.gpkg.

Queries:
--------
owner <name>
khewat <number>
parcel <id>

Examples:
---------
python scripts/query_land.py owner "Jasvir Singh"

python scripts/query_land.py khewat 42

python scripts/query_land.py parcel 3
"""


import sqlite3
import sys
from pathlib import Path


# -------------------------------------------------
# Configuration
# -------------------------------------------------

GPKG = Path(
    "output/HRTK_Land_Data.gpkg"
)


TABLE = "parcel_land_view_clean"



# -------------------------------------------------
# Database connection
# -------------------------------------------------

def connect():

    return sqlite3.connect(
        GPKG
    )



# -------------------------------------------------
# Formatting helpers
# -------------------------------------------------

def format_share(
    numerator,
    denominator
):

    if not denominator:

        return "N/A"


    percent = (
        numerator / denominator * 100
    )


    return (
        f"{int(numerator)}/{int(denominator)} "
        f"({percent:.0f}%)"
    )



def print_header(title):

    print()
    print(title)
    print("=" * len(title))



# -------------------------------------------------
# Owner search
# -------------------------------------------------

def search_owner(name):

    conn = connect()


    rows = conn.execute(
        f"""
        SELECT
            owner_name,
            khewat_no,
            parcel_id,
            numerator,
            denominator,
            rectangle,
            killa,
            kanal,
            marla,
            sarsai

        FROM {TABLE}

        WHERE owner_name LIKE ?

        ORDER BY parcel_id
        """,
        (
            f"%{name}%",
        )
    ).fetchall()


    conn.close()


    print_header(
        "OWNER SEARCH"
    )


    if not rows:

        print(
            "No records found"
        )
        return



    for row in rows:

        (
            owner,
            khewat,
            parcel,
            numerator,
            denominator,
            rectangle,
            killa,
            kanal,
            marla,
            sarsai

        ) = row



        print(
            f"""
Owner:
  {owner}

Parcel:
  {parcel}

Khewat:
  {khewat}

Share:
  {format_share(
        numerator,
        denominator
    )}

Land:
  Rectangle {rectangle}
  Killa {killa}
  {kanal} Kanal {marla} Marla {sarsai} Sarsai

--------------------
"""
        )



# -------------------------------------------------
# Khewat search
# -------------------------------------------------

def search_khewat(number):

    conn = connect()


    rows = conn.execute(
        f"""
        SELECT
            owner_name,
            khewat_no,
            parcel_id,
            numerator,
            denominator

        FROM {TABLE}

        WHERE khewat_no = ?

        ORDER BY parcel_id
        """,
        (
            number,
        )
    ).fetchall()


    conn.close()


    print_header(
        "KHEWAT SEARCH"
    )


    if not rows:

        print(
            "No records found"
        )

        return



    print(
        f"""
Khewat:
  {number}
"""
    )


    print(
        "Owners:"
    )


    print(
        "--------"
    )


    owners_seen = set()


    parcels_seen = set()



    for row in rows:


        (
            owner,
            khewat,
            parcel,
            numerator,
            denominator

        ) = row



        if owner not in owners_seen:


            print(
                f"""
Owner:
  {owner}

Share:
  {format_share(
        numerator,
        denominator
    )}

--------------------
"""
            )


            owners_seen.add(
                owner
            )


        parcels_seen.add(
            parcel
        )



    print(
        "\nParcels:"
    )


    print(
        "--------"
    )


    for parcel in sorted(
        parcels_seen
    ):

        print(
            f"Parcel: {parcel}"
        )


# -------------------------------------------------
# Parcel search
# -------------------------------------------------

def search_parcel(parcel_id):

    conn = connect()


    rows = conn.execute(
        f"""
        SELECT
            parcel_id,
            rectangle,
            killa,
            kanal,
            marla,
            sarsai,
            khewat_no,
            owner_name,
            numerator,
            denominator

        FROM {TABLE}

        WHERE parcel_id = ?

        """,
        (
            parcel_id,
        )
    ).fetchall()


    conn.close()


    print_header(
        "PARCEL SEARCH"
    )


    if not rows:

        print(
            "Parcel not found"
        )

        return



    first = rows[0]


    (
        parcel,
        rectangle,
        killa,
        kanal,
        marla,
        sarsai,
        khewat,
        _,
        _,
        _

    ) = first



    print(
        f"""
Parcel:
  {parcel}

Rectangle:
  {rectangle}

Killa:
  {killa}

Area:
  {kanal} Kanal
  {marla} Marla
  {sarsai} Sarsai

Khewat:
  {khewat}

Owners:
--------
"""
    )


    for row in rows:


        (
            _,
            _,
            _,
            _,
            _,
            _,
            _,
            owner,
            numerator,
            denominator

        ) = row


        print(
            f"""
Owner:
  {owner}

Share:
  {format_share(
        numerator,
        denominator
    )}

--------------------
"""
        )



# -------------------------------------------------
# Command line interface
# -------------------------------------------------

def show_help():

    print(
        """
Usage:

python query_land.py owner "name"

python query_land.py khewat 42

python query_land.py parcel 3
"""
    )



if __name__ == "__main__":


    if len(sys.argv) < 3:

        show_help()
        sys.exit(1)



    command = sys.argv[1]

    value = sys.argv[2]



    if command == "owner":

        search_owner(value)


    elif command == "khewat":

        search_khewat(value)


    elif command == "parcel":

        search_parcel(value)


    else:

        print(
            "Unknown command:",
            command
        )

        show_help()