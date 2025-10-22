import bpy


# noinspection PyPep8Naming
class FLEXSHAPE_PT_armature(bpy.types.Panel):
    bl_idname = "FLEXSHAPE_PT_armature"
    bl_label = "Armature"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FlexShape"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        armature_box = layout.box()

        armature_box.label(text="Armature Setup", icon="MOD_ARMATURE")
        armature_box.prop(
            context.scene,
            "flexshape_armature_source",
            text="Source",
            icon="MOD_ARMATURE",
            emboss=True,
        )

        armature_box.label(text="Armature Operations", icon="POSE_HLT")
        armature_box.operator(
            "flexshape.copy_pose_relations",
            text="Copy Relations to Selection",
            icon="BONE_DATA",
            emboss=True,
        )
        armature_box.operator(
            "flexshape.copy_pose_transforms",
            text="Copy Transforms to Selection",
            icon="MOD_DATA_TRANSFER",
            emboss=True,
        )
        armature_box.operator(
            "flexshape.clear_pose_transforms",
            text="Clear Selection Transforms",
            icon="REMOVE",
            emboss=True,
        )

        armature_box.label(text="Armature to Shapekey", icon="SHAPEKEY_DATA")
        armature_box.prop(
            context.scene,
            "flexshape_armature_shapekey_name",
            text="Name",
            icon_value=0,
            emboss=True,
        )
        armature_box.operator(
            "flexshape.armature_save_as_shapekey",
            text="Save (Selection)",
            icon="SHAPEKEY_DATA",
            emboss=True,
        ).use_selection = True
        armature_box.operator(
            "flexshape.armature_save_as_shapekey",
            text="Save (Armature Children)",
            icon="SHAPEKEY_DATA",
            emboss=True,
        ).use_selection = False
        armature_box.operator(
            "flexshape.armature_quick_save",
            text="Quick Save",
            icon="PLAY",
            emboss=True,
        )

        armature_box.label(text="Mass Armature to Shapekeys", icon="DOCUMENTS")
        row = armature_box.row()
        row.template_list(
            "FLEXSHAPE_UL_ArmatureList",
            "",
            context.scene,
            "flexshape_armature_list",
            context.scene,
            "flexshape_armature_list_index",
            rows=5,
        )

        col = row.column(align=True)
        col.operator("flexshape.add_armature_to_list", icon="ADD", text="")
        col.operator("flexshape.remove_armature_from_list", icon="REMOVE", text="")
        col.separator()
        col.operator("flexshape.move_armature_up", icon="TRIA_UP", text="")
        col.operator("flexshape.move_armature_down", icon="TRIA_DOWN", text="")
        col.separator()
        col.operator("flexshape.clear_armature_list", icon="X", text="")

        armature_box.operator(
            "flexshape.armature_mass_save",
            text="Quick Save List",
            icon="PLAY",
            emboss=True,
        )
