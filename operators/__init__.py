import sys
import importlib

if "armature_operators" in locals():
    package_name = __package__

    submodules = [
        "armature_operators",
        "armature_list_operators",
        "lattice_operators",
        "lattice_list_operators",
        "surface_deform_operators",
        "surface_deform_list_operators",
        "utils_operators",
        "shapekey_revert_operators",
    ]

    for submodule_name in submodules:
        full_module_name = f"{package_name}.{submodule_name}"
        if full_module_name in sys.modules:
            importlib.reload(sys.modules[full_module_name])
            print(f"    Reloaded: FlexShape operators.{submodule_name}")

from . import (
    armature_operators,
    armature_list_operators,
    lattice_operators,
    lattice_list_operators,
    surface_deform_operators,
    surface_deform_list_operators,
    utils_operators,
    shapekey_revert_operators,
)


operators = (
    armature_operators,
    armature_list_operators,
    lattice_operators,
    lattice_list_operators,
    surface_deform_operators,
    surface_deform_list_operators,
    utils_operators,
    shapekey_revert_operators,
)


def register():
    for module in operators:
        module.register()


def unregister():
    for module in reversed(operators):
        module.unregister()
