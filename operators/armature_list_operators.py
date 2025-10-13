import bpy

from ..common.list_crud_operators import create_list_crud_operators


(
    FLEXSHAPE_UL_ArmatureList,
    FLEXSHAPE_OT_AddArmatureToList,
    FLEXSHAPE_OT_RemoveArmatureFromList,
    FLEXSHAPE_OT_ClearArmatureList,
    FLEXSHAPE_OT_MoveArmatureUp,
    FLEXSHAPE_OT_MoveArmatureDown,
) = create_list_crud_operators(
    object_type="ARMATURE",
    icon="ARMATURE_DATA",
    id_prefix="armature",
    list_prop="flexshape_armature_list",
    index_prop="flexshape_armature_list_index",
)


classes = (
    FLEXSHAPE_UL_ArmatureList,
    FLEXSHAPE_OT_AddArmatureToList,
    FLEXSHAPE_OT_RemoveArmatureFromList,
    FLEXSHAPE_OT_ClearArmatureList,
    FLEXSHAPE_OT_MoveArmatureUp,
    FLEXSHAPE_OT_MoveArmatureDown,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
