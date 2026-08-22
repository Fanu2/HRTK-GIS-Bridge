from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsRelation,
)

from pathlib import Path


PROJECT = QgsProject.instance()


BASE = Path(
    "/home/jasvir/Projects/HRTK-GIS-Bridge"
)


GPKG = str(
    BASE /
    "output/HRTK_Land_Data.gpkg"
)


OUTPUT = str(
    BASE /
    "qgis/HRTK_Land_Project.qgz"
)



# ---------------------------------
# Reset project
# ---------------------------------

PROJECT.clear()


root = PROJECT.layerTreeRoot()


group = root.addGroup(
    "HRTK Revenue Data"
)



# ---------------------------------
# Load layers
# ---------------------------------

layers = {

    "Villages": "villages",

    "Khewats": "khewats",

    "Owners": "owners",

    "Ownership": "ownerships",

    "Parcels": "parcels",

    "⭐ Land View": "land_view",

}



created = {}



for name, table in layers.items():


    uri = (
        f"{GPKG}|layername={table}"
    )


    layer = QgsVectorLayer(
        uri,
        name,
        "ogr"
    )


    if not layer.isValid():

        print(
            "FAILED:",
            table
        )

        continue



    PROJECT.addMapLayer(
        layer,
        False
    )


    group.addLayer(
        layer
    )


    created[table] = layer


    print(
        "Loaded:",
        name
    )



# ---------------------------------
# Relations
# ---------------------------------


def add_relation(
    relation_id,
    name,
    parent,
    child,
    parent_field,
    child_field
):


    relation = QgsRelation()


    relation.setId(
        relation_id
    )


    relation.setName(
        name
    )


    relation.setReferencedLayer(
        created[parent].id()
    )


    relation.setReferencingLayer(
        created[child].id()
    )


    relation.addFieldPair(
        child_field,
        parent_field
    )


    PROJECT.relationManager().addRelation(
        relation
    )


    print(
        "Relation:",
        name
    )



if (
    "khewats" in created
    and "ownerships" in created
):

    add_relation(
        "khewat_ownership",
        "Khewat Ownership",
        "khewats",
        "ownerships",
        "id",
        "khewat_id"
    )



if (
    "owners" in created
    and "ownerships" in created
):

    add_relation(
        "owner_ownership",
        "Owner Ownership",
        "owners",
        "ownerships",
        "id",
        "owner_id"
    )



# ---------------------------------
# Save
# ---------------------------------

PROJECT.write(
    OUTPUT
)


print("")
print(
    "Created:",
    OUTPUT
)