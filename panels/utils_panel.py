import bpy


# noinspection PyPep8Naming
class FLEXSHAPE_PT_utils(bpy.types.Panel):
    bl_idname = "FLEXSHAPE_PT_utils"
    bl_label = "Utils"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FlexShape"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        remove_zero_impact_shapekey_box = layout.box()
        remove_zero_impact_shapekey_box.label(
            text="Remove Zero Impact Shapekeys", icon="SHAPEKEY_DATA"
        )
        remove_zero_impact_shapekey_box.prop(
            context.scene,
            "flexshape_utils_skip_prefix",
            text="Prefixes to Skip",
            icon_value=0,
            emboss=True,
        )
        remove_zero_impact_shapekey_box.prop(
            context.scene,
            "flexshape_utils_shapekey_threshold",
            text="Vertex Diff Threshold",
            icon_value=0,
            emboss=True,
        )
        remove_zero_impact_shapekey_box.operator(
            "flexshape.utils_remove_zero_shapekeys",
            text="Remove from Selection",
            icon="SHAPEKEY_DATA",
            emboss=True,
        ).use_selection = True
        remove_zero_impact_shapekey_box.operator(
            "flexshape.utils_remove_zero_shapekeys",
            text="Remove from Armature Children",
            icon="SHAPEKEY_DATA",
            emboss=True,
        ).use_selection = False

        set_shapekey_to_zero_box = layout.box()
        set_shapekey_to_zero_box.label(text="Reset Shapekeys", icon="SHAPEKEY_DATA")
        set_shapekey_to_zero_box.operator(
            "flexshape.utils_set_shapekey_0",
            text="Reset from Selection",
            icon="SHAPEKEY_DATA",
            emboss=True,
        ).use_selection = True
