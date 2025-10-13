import bpy
from ..common.list_crud_operators import create_list_crud_operators

(
    FLEXSHAPE_UL_LatticeList,
    FLEXSHAPE_OT_AddLatticeToList,
    FLEXSHAPE_OT_RemoveLatticeFromList,
    FLEXSHAPE_OT_ClearLatticeList,
    FLEXSHAPE_OT_MoveLatticeUp,
    FLEXSHAPE_OT_MoveLatticeDown,
) = create_list_crud_operators(
    object_type="LATTICE",
    icon="LATTICE_DATA",
    id_prefix="lattice",
    list_prop="flexshape_lattice_list",
    index_prop="flexshape_lattice_list_index",
)


classes = (
    FLEXSHAPE_UL_LatticeList,
    FLEXSHAPE_OT_AddLatticeToList,
    FLEXSHAPE_OT_RemoveLatticeFromList,
    FLEXSHAPE_OT_ClearLatticeList,
    FLEXSHAPE_OT_MoveLatticeUp,
    FLEXSHAPE_OT_MoveLatticeDown,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
