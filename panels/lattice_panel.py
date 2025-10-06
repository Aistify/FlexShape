import bpy


# noinspection PyPep8Naming
class FLEXSHAPE_PT_lattice(bpy.types.Panel):
    bl_idname = "FLEXSHAPE_PT_lattice"
    bl_label = "Lattice"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FlexShape"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        lattice_box = layout.box()

        lattice_box.label(text="Lattice Setup", icon="MOD_LATTICE")
        lattice_box.prop(
            context.scene,
            "flexshape_lattice_source",
            text="Source",
            icon="MOD_LATTICE",
            emboss=True,
        )

        lattice_box.label(text="Lattice Operations", icon="MOD_LATTICE")
        lattice_box.operator(
            "flexshape.add_lattice",
            text="Add Lattice To Selection",
            icon="MODIFIER_ON",
            emboss=True,
        )
        lattice_box.operator(
            "flexshape.remove_lattice",
            text="Remove From Selection",
            icon="MODIFIER_OFF",
            emboss=True,
        )

        lattice_box.label(text="Lattice To Shape Key", icon="SHAPEKEY_DATA")
        lattice_box.prop(
            context.scene,
            "flexshape_lattice_auto_remove",
            text="Auto Remove After Save?",
            icon_value=0,
            emboss=True,
        )
        lattice_box.prop(
            context.scene,
            "flexshape_lattice_shapekey_name",
            text="Name",
            icon_value=0,
            emboss=True,
        )
        lattice_box.operator(
            "flexshape.lattice_save_as_shapekey",
            text="Save As Shape Key",
            icon="SHAPEKEY_DATA",
            emboss=True,
        )
