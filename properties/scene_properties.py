import bpy


def _update_skip_prefixes(_, context):
    __ = [
        prefix.strip()
        for prefix in context.scene.flexshape_utils_skip_prefix.split(",")
        if prefix.strip()
    ]


def _update_source_shapekeys(_, context):
    if context.scene.flexshape_surface_deform_source:
        try:
            # noinspection PyUnresolvedReferences
            bpy.ops.flexshape.load_source_shapekeys()
        except Exception as e:
            print(f"Error loading Shapekey: {e}")
    else:
        context.scene.flexshape_surface_deform_shapekey_list.clear()


# noinspection PyPep8Naming, PyTypeHints
class FLEXSHAPE_ArmatureListItem(bpy.types.PropertyGroup):
    armature: bpy.props.PointerProperty(
        name="Armature",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "ARMATURE",
    )


# noinspection PyPep8Naming, PyTypeHints
class FLEXSHAPE_LatticeListItem(bpy.types.PropertyGroup):
    lattice: bpy.props.PointerProperty(
        name="Lattice",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "LATTICE",
    )


# noinspection PyPep8Naming, PyTypeHints
class FLEXSHAPE_SurfaceDeformShapekeyItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Shapekey Name")
    enabled: bpy.props.BoolProperty(name="Enabled", default=False)


# noinspection PyPep8Naming, PyTypeHints
class FLEXSHAPE_BlendShapeItem(bpy.types.PropertyGroup):
    blend_name: bpy.props.StringProperty(name="Blend Name")
    blend_index: bpy.props.IntProperty(name="Blend Index")
    blend_value: bpy.props.FloatProperty(name="Blend Value")


# noinspection PyPep8Naming, PyTypeHints
class FLEXSHAPE_BlendCategoryItem(bpy.types.PropertyGroup):
    category_name: bpy.props.StringProperty(name="Category Name")
    blendshapes: bpy.props.CollectionProperty(type=FLEXSHAPE_BlendShapeItem)


property_groups = (
    FLEXSHAPE_ArmatureListItem,
    FLEXSHAPE_LatticeListItem,
    FLEXSHAPE_SurfaceDeformShapekeyItem,
    FLEXSHAPE_BlendShapeItem,
    FLEXSHAPE_BlendCategoryItem,
)


ARMATURE_PROPS = {
    "flexshape_armature_source": bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "ARMATURE",
    ),
    "flexshape_armature_shapekey_name": bpy.props.StringProperty(),
    "flexshape_armature_list": bpy.props.CollectionProperty(
        type=FLEXSHAPE_ArmatureListItem
    ),
    "flexshape_armature_list_index": bpy.props.IntProperty(default=0),
}


LATTICE_PROPS = {
    "flexshape_lattice_source": bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "LATTICE",
    ),
    "flexshape_lattice_shapekey_name": bpy.props.StringProperty(),
    "flexshape_lattice_auto_remove": bpy.props.BoolProperty(default=True),
    "flexshape_lattice_list": bpy.props.CollectionProperty(
        type=FLEXSHAPE_LatticeListItem
    ),
    "flexshape_lattice_list_index": bpy.props.IntProperty(default=0),
}


SURFACE_DEFORM_PROPS = {
    "flexshape_surface_deform_source": bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "MESH",
        update=_update_source_shapekeys,
    ),
    "flexshape_surface_deform_shapekey_name": bpy.props.StringProperty(),
    "flexshape_surface_deform_auto_remove": bpy.props.BoolProperty(default=True),
    "flexshape_surface_deform_shapekey_list": bpy.props.CollectionProperty(
        type=FLEXSHAPE_SurfaceDeformShapekeyItem
    ),
    "flexshape_surface_deform_shapekey_list_index": bpy.props.IntProperty(default=0),
}


UTILS_PROPS = {
    "flexshape_utils_skip_prefix": bpy.props.StringProperty(
        default="vrc,=====",
        update=_update_skip_prefixes,
    ),
    "flexshape_utils_shapekey_threshold": bpy.props.FloatProperty(
        default=0.0001,
        precision=7,
    ),
}


SHAPEKEY_REVERT_PROPS = {
    "flexshape_shapekey_revert_target": bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "MESH",
    ),
    "flexshape_shapekey_revert_json_file": bpy.props.StringProperty(
        subtype="FILE_PATH",
    ),
    "flexshape_shapekey_revert_delimiter": bpy.props.StringProperty(
        default="-----",
    ),
    "flexshape_shapekey_revert_category_list": bpy.props.CollectionProperty(
        type=FLEXSHAPE_BlendCategoryItem
    ),
    "flexshape_shapekey_revert_category_list_index": bpy.props.IntProperty(default=0),
}

PLACEHOLDER_PROPS = {
    "flexshape_placeholder_face_mesh": bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "MESH",
    ),
}


scene_properties = {
    **ARMATURE_PROPS,
    **LATTICE_PROPS,
    **SURFACE_DEFORM_PROPS,
    **UTILS_PROPS,
    **PLACEHOLDER_PROPS,
    **SHAPEKEY_REVERT_PROPS,
}


def register():
    for cls in property_groups:
        bpy.utils.register_class(cls)

    for prop_name, prop_value in scene_properties.items():
        setattr(bpy.types.Scene, prop_name, prop_value)


def unregister():
    for prop_name in scene_properties.keys():
        delattr(bpy.types.Scene, prop_name)

    for cls in reversed(property_groups):
        bpy.utils.unregister_class(cls)
