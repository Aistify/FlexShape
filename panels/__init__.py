import bpy
from .armature_panel import A1_FS_PT_ARMATURE_PANEL
from .blendshape_utils_panel import A1_FS_PT_BLENDSHAPE_UTILS_PANEL
from .lattice_panel import A1_FS_PT_LATTICE_PANEL
from .main_panel import A1_FS_PT_MAIN_PANEL
from .utils_panel import A1_FS_PT_UTILS_PANEL

classes = (
    A1_FS_PT_MAIN_PANEL,
    A1_FS_PT_ARMATURE_PANEL,
    A1_FS_PT_LATTICE_PANEL,
    A1_FS_PT_UTILS_PANEL,
    A1_FS_PT_BLENDSHAPE_UTILS_PANEL,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
