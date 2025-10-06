import sys
import importlib

if "armature_operators" in locals():
    package_name = __package__

    submodules = [
        "armature_operators",
        "lattice_operators",
        "surface_deform_operators",
        "utils_operators",
    ]

    for submodule_name in submodules:
        full_module_name = f"{package_name}.{submodule_name}"
        if full_module_name in sys.modules:
            importlib.reload(sys.modules[full_module_name])
            print(f"    Reloaded: FlexShape operators.{submodule_name}")

from . import (
    armature_operators,
    lattice_operators,
    surface_deform_operators,
    utils_operators,
)


def register():
    armature_operators.register()
    lattice_operators.register()
    surface_deform_operators.register()
    utils_operators.register()


def unregister():
    armature_operators.unregister()
    lattice_operators.unregister()
    surface_deform_operators.unregister()
    utils_operators.unregister()
