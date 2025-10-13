import bpy


# noinspection PyPep8Naming
class FLEXSHAPE_PT_surface_deform(bpy.types.Panel):
    bl_idname = "FLEXSHAPE_PT_surface_deform"
    bl_label = "Surface Deform"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FlexShape"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        surface_deform_box = layout.box()

        surface_deform_box.label(
            text="Surface Deform Setup",
            icon="MOD_SUBSURF",
        )
        surface_deform_box.prop(
            context.scene,
            "flexshape_surface_deform_source",
            text="Source",
            icon="MESH_DATA",
            emboss=True,
        )
        surface_deform_box.operator(
            "flexshape.utils_set_shapekey_0",
            text="Set Source Shapekeys to 0",
            icon="SHAPEKEY_DATA",
            emboss=True,
        ).use_surface_deform_source = True

        surface_deform_box.label(
            text="Surface Deform Operations",
            icon="MOD_SUBSURF",
        )
        surface_deform_box.operator(
            "flexshape.add_surface_deform",
            text="Add Surface Deform To Selection",
            icon="ADD",
            emboss=True,
        )
        surface_deform_box.operator(
            "flexshape.remove_surface_deform",
            text="Remove From Selection",
            icon="REMOVE",
            emboss=True,
        )

        surface_deform_box.label(
            text="Save Surface Deform To Shape Key", icon="SHAPEKEY_DATA"
        )
        surface_deform_box.prop(
            context.scene,
            "flexshape_surface_deform_shapekey_name",
            text="Name",
            icon="SHAPEKEY_DATA",
            emboss=True,
        )
        surface_deform_box.prop(
            context.scene,
            "flexshape_surface_deform_auto_remove",
            text="Auto Remove After Save?",
            icon_value=0,
            emboss=True,
        )
        surface_deform_box.operator(
            "flexshape.surface_deform_save_as_shapekey",
            text="Save As Shape Key",
            icon="SHAPEKEY_DATA",
            emboss=True,
        )

        surface_deform_box.label(
            text="Mass Copy Shapekeys with Surface Deforms",
            icon="MOD_SUBSURF",
        )
        row = surface_deform_box.row()
        row.template_list(
            "FLEXSHAPE_UL_SurfaceDeformShapekeyList",
            "",
            context.scene,
            "flexshape_surface_deform_shapekey_list",
            context.scene,
            "flexshape_surface_deform_shapekey_list_index",
            rows=5,
        )

        col = row.column(align=True)
        col.operator("flexshape.select_all_shapekeys", icon="CHECKBOX_HLT", text="")
        col.operator("flexshape.deselect_all_shapekeys", icon="CHECKBOX_DEHLT", text="")
        surface_deform_box.operator(
            "flexshape.load_source_shapekeys",
            text="Reload Shapekeys from Source",
            icon="FILE_REFRESH",
            emboss=True,
        )
        surface_deform_box.operator(
            "flexshape.surface_deform_mass_save",
            text="Save Selected Shapekeys To Selection",
            icon="PLAY",
            emboss=True,
        )
