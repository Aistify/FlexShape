import bpy


class A1_FS_PT_LATTICE_PANEL(bpy.types.Panel):
    bl_label = "FlexShape Lattice Panel"
    bl_idname = "A1_FS_PT_LATTICE_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        return False

    def draw(self, context):
        layout = self.layout

        lattice_box = layout.box()

        lattice_box.label(text="Lattice Setup", icon="MOD_LATTICE")
        lattice_box.prop(
            context.scene,
            "a1_fs_lattice_source",
            text="Source",
            icon="MOD_LATTICE",
            emboss=True,
        )

        lattice_box.label(text="Lattice Operations", icon="MOD_LATTICE")
        lattice_box.operator(
            "a1_fs.add_lattice",
            text="Add Lattice To Selection",
            icon="MODIFIER_ON",
            emboss=True,
        )
        lattice_box.operator(
            "a1_fs.remove_lattice",
            text="Remove From Selection",
            icon="MODIFIER_OFF",
            emboss=True,
        )

        lattice_box.label(text="Lattice To Shape Key", icon="SHAPEKEY_DATA")
        lattice_box.prop(
            context.scene,
            "a1_fs_lattice_auto_remove",
            text="Auto Remove After Save?",
            icon_value=0,
            emboss=True,
        )
        lattice_box.prop(
            context.scene,
            "a1_fs_lattice_shapekey_name",
            text="Name",
            icon_value=0,
            emboss=True,
        )
        lattice_box.operator(
            "a1_fs.lattice_save_as_shapekey",
            text="Save As Shape Key",
            icon="SHAPEKEY_DATA",
            emboss=True,
        )
