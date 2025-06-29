import bpy
from bpy.props import StringProperty, CollectionProperty


class A1_FS_LatticeItem(bpy.types.PropertyGroup):
    name: StringProperty()


def register():
    bpy.types.Scene.a1_fs_armature_source = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "ARMATURE",
    )
    bpy.types.Scene.a1_fs_armature_show_panel = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.a1_fs_armature_shapekey_name = bpy.props.StringProperty()

    bpy.types.Scene.a1_fs_lattice_source = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "LATTICE",
    )
    bpy.types.Scene.a1_fs_lattice_show_panel = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.a1_fs_lattice_shapekey_name = bpy.props.StringProperty()
    bpy.types.Scene.a1_fs_lattice_auto_remove = bpy.props.BoolProperty(default=True)
    bpy.utils.register_class(A1_FS_LatticeItem)
    bpy.types.Scene.a1_fs_lattice_list = CollectionProperty(type=A1_FS_LatticeItem)

    bpy.types.Scene.a1_fs_surface_deform_source = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "MESH",
    )
    bpy.types.Scene.a1_fs_surface_deform_show_panel = bpy.props.BoolProperty(
        default=False
    )
    bpy.types.Scene.a1_fs_surface_deform_shapekey_name = bpy.props.StringProperty()
    bpy.types.Scene.a1_fs_surface_deform_auto_remove = bpy.props.BoolProperty(
        default=True
    )

    bpy.types.Scene.a1_fs_utils_show_panel = bpy.props.BoolProperty(default=False)

    def update_skip_prefixes(self, context):
        skip_prefixes = [
            prefix.strip()
            for prefix in context.scene.a1_fs_utils_skip_prefix.split(",")
            if prefix.strip()
        ]
        return skip_prefixes

    bpy.types.Scene.a1_fs_utils_skip_prefix = bpy.props.StringProperty(
        default="vrc,=====", update=update_skip_prefixes
    )
    bpy.types.Scene.a1_fs_util_shapekey_threshold = bpy.props.FloatProperty(
        default=0.0001,
        precision=7,
    )

    bpy.types.Scene.a1_fs_json_file = bpy.props.StringProperty(
        subtype="FILE_PATH",
    )
    bpy.types.Scene.a1_fs_placeholder_face_mesh = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "MESH",
    )


def unregister():
    del bpy.types.Scene.a1_fs_armature_source
    del bpy.types.Scene.a1_fs_armature_show_panel
    del bpy.types.Scene.a1_fs_armature_shapekey_name

    del bpy.types.Scene.a1_fs_lattice_source
    del bpy.types.Scene.a1_fs_lattice_show_panel
    del bpy.types.Scene.a1_fs_lattice_shapekey_name
    del bpy.types.Scene.a1_fs_lattice_auto_remove
    bpy.utils.unregister_class(A1_FS_LatticeItem)
    del bpy.types.Scene.a1_fs_lattice_list

    del bpy.types.Scene.a1_fs_surface_deform_source
    del bpy.types.Scene.a1_fs_surface_deform_show_panel
    del bpy.types.Scene.a1_fs_surface_deform_shapekey_name
    del bpy.types.Scene.a1_fs_surface_deform_auto_remove

    del bpy.types.Scene.a1_fs_utils_show_panel
    del bpy.types.Scene.a1_fs_utils_skip_prefix
    del bpy.types.Scene.a1_fs_util_shapekey_threshold

    del bpy.types.Scene.a1_fs_placeholder_json_file
    del bpy.types.Scene.a1_fs_placeholder_face_mesh
