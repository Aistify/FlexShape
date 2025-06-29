import bpy


class A1_FS_PT_UTILS_PANEL(bpy.types.Panel):
    bl_label = "FlexShape Utils Panel"
    bl_idname = "A1_FS_PT_UTILS_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        return False

    def draw(self, context):
        layout = self.layout

        remove_zero_impact_shapekey_box = layout.box()
        remove_zero_impact_shapekey_box.label(
            text="Remove Zero Impact Shapekeys", icon="SHAPEKEY_DATA"
        )
        remove_zero_impact_shapekey_box.prop(
            context.scene,
            "a1_fs_utils_skip_prefix",
            text="Prefixes to Skip",
            icon_value=0,
            emboss=True,
        )
        remove_zero_impact_shapekey_box.prop(
            context.scene,
            "a1_fs_util_shapekey_threshold",
            text="Vertex Diff Threshold",
            icon_value=0,
            emboss=True,
        )
        remove_zero_impact_shapekey_box.operator(
            "a1_fs.utils_remove_zero_shapekeys",
            text="Remove from Selection",
            icon="SHAPEKEY_DATA",
            emboss=True,
        ).use_selection = True
        remove_zero_impact_shapekey_box.operator(
            "a1_fs.utils_remove_zero_shapekeys",
            text="Remove from Armature's Children",
            icon="SHAPEKEY_DATA",
            emboss=True,
        ).use_selection = False

        set_shapekey_to_zero_box = layout.box()
        set_shapekey_to_zero_box.label(text="Reset Shapekeys", icon="SHAPEKEY_DATA")
        set_shapekey_to_zero_box.operator(
            "a1_fs.utils_set_shapekey_0",
            text="Reset from Selection",
            icon="SHAPEKEY_DATA",
            emboss=True,
        ).use_selection = True
