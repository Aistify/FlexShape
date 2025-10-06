import sys
import importlib

if "properties" in locals():
    package_name = __package__

    submodules = [
        "scene_properties",
    ]

    for submodule_name in submodules:
        full_module_name = f"{package_name}.{submodule_name}"
        if full_module_name in sys.modules:
            importlib.reload(sys.modules[full_module_name])
            print(f"    Reloaded: common.{submodule_name}")

from . import scene_properties


def register():
    scene_properties.register()


def unregister():
    scene_properties.unregister()
