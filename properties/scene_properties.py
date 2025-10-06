import bpy


# noinspection PyNoneFunctionAssignment
def register():
    bpy.types.Scene.flexshape_armature_source = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "ARMATURE",
    )
    bpy.types.Scene.flexshape_armature_shapekey_name = bpy.props.StringProperty()

    bpy.types.Scene.flexshape_lattice_source = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "LATTICE",
    )
    bpy.types.Scene.flexshape_lattice_shapekey_name = bpy.props.StringProperty()
    bpy.types.Scene.flexshape_lattice_auto_remove = bpy.props.BoolProperty(default=True)

    bpy.types.Scene.flexshape_surface_deform_source = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "MESH",
    )
    bpy.types.Scene.flexshape_surface_deform_shapekey_name = bpy.props.StringProperty()
    bpy.types.Scene.flexshape_surface_deform_auto_remove = bpy.props.BoolProperty(
        default=True
    )

    # noinspection PyUnusedLocal
    def update_skip_prefixes(self, context):
        skip_prefixes = [
            prefix.strip()
            for prefix in context.scene.flexshape_utils_skip_prefix.split(",")
            if prefix.strip()
        ]
        return skip_prefixes

    # noinspection PyTypeChecker
    bpy.types.Scene.flexshape_utils_skip_prefix = bpy.props.StringProperty(
        default="vrc,=====", update=update_skip_prefixes
    )
    bpy.types.Scene.flexshape_utils_shapekey_threshold = bpy.props.FloatProperty(
        default=0.0001,
        precision=7,
    )

    bpy.types.Scene.flexshape_placeholder_json_file = bpy.props.StringProperty(
        subtype="FILE_PATH",
    )
    bpy.types.Scene.flexshape_placeholder_face_mesh = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "MESH",
    )


def unregister():
    del bpy.types.Scene.flexshape_armature_source
    del bpy.types.Scene.flexshape_armature_shapekey_name

    del bpy.types.Scene.flexshape_lattice_source
    del bpy.types.Scene.flexshape_lattice_shapekey_name
    del bpy.types.Scene.flexshape_lattice_auto_remove

    del bpy.types.Scene.flexshape_surface_deform_source
    del bpy.types.Scene.flexshape_surface_deform_shapekey_name
    del bpy.types.Scene.flexshape_surface_deform_auto_remove

    del bpy.types.Scene.flexshape_utils_skip_prefix
    del bpy.types.Scene.flexshape_utils_shapekey_threshold

    del bpy.types.Scene.flexshape_placeholder_json_file
    del bpy.types.Scene.flexshape_placeholder_face_mesh
