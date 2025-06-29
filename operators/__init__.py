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
