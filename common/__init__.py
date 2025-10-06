import sys
import importlib

if "operators" in locals():
    package_name = __package__

    submodules = [
        "operators",
    ]

    for submodule_name in submodules:
        full_module_name = f"{package_name}.{submodule_name}"
        if full_module_name in sys.modules:
            importlib.reload(sys.modules[full_module_name])
            print(f"    Reloaded: FlexShape common.{submodule_name}")

from . import (
    operators,
)


def register():
    operators.register()


def unregister():
    operators.unregister()
