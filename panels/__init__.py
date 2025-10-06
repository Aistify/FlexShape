import sys
import importlib

if "armature_panel" in locals():
    package_name = __package__

    submodules = [
        "armature_panel",
        "lattice_panel",
        "surface_deform_panel",
        "blendshape_utils_panel",
        "utils_panel",
    ]

    for submodule_name in submodules:
        full_module_name = f"{package_name}.{submodule_name}"
        if full_module_name in sys.modules:
            importlib.reload(sys.modules[full_module_name])
            print(f"    Reloaded: FlexShape panels.{submodule_name}")

import bpy
from .armature_panel import FLEXSHAPE_PT_armature
from .lattice_panel import FLEXSHAPE_PT_lattice
from .surface_deform_panel import FLEXSHAPE_PT_surface_deform
from .blendshape_utils_panel import FLEXSHAPE_PT_blendshape_utils
from .utils_panel import FLEXSHAPE_PT_utils

classes = (
    FLEXSHAPE_PT_armature,
    FLEXSHAPE_PT_lattice,
    FLEXSHAPE_PT_surface_deform,
    FLEXSHAPE_PT_blendshape_utils,
    FLEXSHAPE_PT_utils,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
