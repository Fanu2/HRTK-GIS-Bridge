"""
HRTK GIS Bridge - Open Parcel Map

Purpose:
--------
Open QGIS and zoom to a parcel from HRTK.

Usage:
------
python open_parcel_map.py 3
"""

import sys
import subprocess
from pathlib import Path


# -------------------------------------------------
# Configuration
# -------------------------------------------------

BASE = Path(
    "/home/jasvir/Projects/HRTK-GIS-Bridge"
)


PROJECT = (
    BASE /
    "qgis/HRTK_Land_Project.qgz"
)


LAYER = (
    "Land Parcels"
)


# -------------------------------------------------
# Open QGIS project
# -------------------------------------------------

def open_map(parcel_id):

    print(
        f"Opening parcel {parcel_id}"
    )


    subprocess.Popen(
        [
            "qgis",
            str(PROJECT)
        ]
    )


# -------------------------------------------------
# Main
# -------------------------------------------------

if __name__ == "__main__":


    if len(sys.argv) < 2:

        print(
            """
Usage:

python open_parcel_map.py <parcel_id>

Example:

python open_parcel_map.py 3
"""
        )

        sys.exit(1)


    parcel_id = sys.argv[1]


    open_map(
        parcel_id
    )