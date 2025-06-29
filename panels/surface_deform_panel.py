import bpy


class A1_FS_PT_SURFACE_DEFORM_PANEL(bpy.types.Panel):
    bl_label = "FlexShape Surface Deform Panel"
    bl_idname = "A1_FS_PT_SURFACE_DEFORM_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    # noinspection PyUnusedLocal
    @classmethod
    def poll(cls, context):
        return False

    def draw(self, context):
        layout = self.layout

        surface_deform_box = layout.box()

        surface_deform_box.label(
            text="Surface Deform Setup",
            icon="MOD_SUBSURF",
        )
        surface_deform_box.prop(
            context.scene,
            "a1_fs_surface_deform_source",
            text="Source",
            icon="MESH_DATA",
            emboss=True,
        )
        surface_deform_box.operator(
            "a1_fs.utils_set_shapekey_0",
            text="Set Source Shapekeys to 0",
            icon="SHAPEKEY_DATA",
            emboss=True,
        ).use_selection = False

        surface_deform_box.label(
            text="Surface Deform Operations",
            icon="MOD_SUBSURF",
        )
        surface_deform_box.operator(
            "a1_fs.add_surface_deform",
            text="Add Surface Deform To Selection",
            icon="ADD",
            emboss=True,
        )
        surface_deform_box.operator(
            "a1_fs.remove_surface_deform",
            text="Remove From Selection",
            icon="REMOVE",
            emboss=True,
        )

        surface_deform_box.label(
            text="Save Surface Deform To Shape Key", icon="SHAPEKEY_DATA"
        )
        surface_deform_box.prop(
            context.scene,
            "a1_fs_surface_deform_shapekey_name",
            text="Name",
            icon="SHAPEKEY_DATA",
            emboss=True,
        )
        surface_deform_box.prop(
            context.scene,
            "a1_fs_surface_deform_auto_remove",
            text="Auto Remove After Save?",
            icon_value=0,
            emboss=True,
        )
        surface_deform_box.operator(
            "a1_fs.surface_deform_save_as_shapekey",
            text="Save As Shape Key",
            icon="SHAPEKEY_DATA",
            emboss=True,
        )
