# But why tho

bl_info = {
    "name": "FlexShape",
    "author": "Aistify",
    "description": "v1.0 Release",
    "blender": (4, 2, 0),
    "version": (1, 0, 0),
    "location": "@Aistify",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "3D View",
}

import bpy
import bpy.utils.previews
from . import (
    panels,
    properties,
    operators,
    common,
)

addon_keymaps = {}
_icons = None


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    panels.register()
    properties.register()
    operators.register()
    common.register()


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    panels.unregister()
    properties.unregister()
    operators.unregister()
    common.unregister()

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
