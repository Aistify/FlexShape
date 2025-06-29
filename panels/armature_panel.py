import bpy


class A1_FS_PT_ARMATURE_PANEL(bpy.types.Panel):
    bl_label = "FlexShape Armature Panel"
    bl_idname = "A1_FS_PT_ARMATURE_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        return False

    def draw(self, context):
        layout = self.layout

        armature_box = layout.box()

        armature_box.label(text="Armature Setup", icon="MOD_ARMATURE")
        armature_box.prop(
            context.scene,
            "a1_fs_armature_source",
            text="Source",
            icon="MOD_ARMATURE",
            emboss=True,
        )

        armature_box.label(text="Armature Operations", icon="POSE_HLT")
        armature_box.operator(
            "a1_fs.copy_pose_relations",
            text="Copy Relations To Selection",
            icon="BONE_DATA",
            emboss=True,
        )
        armature_box.operator(
            "a1_fs.copy_pose_transforms",
            text="Copy Transforms To Selection",
            icon="MOD_DATA_TRANSFER",
            emboss=True,
        )
        armature_box.operator(
            "a1_fs.clear_pose_transforms",
            text="Clear Selection Transforms",
            icon="REMOVE",
            emboss=True,
        )

        armature_box.label(text="Armature To Shape Key", icon="SHAPEKEY_DATA")
        armature_box.prop(
            context.scene,
            "a1_fs_armature_shapekey_name",
            text="Name",
            icon_value=0,
            emboss=True,
        )
        armature_box.operator(
            "a1_fs.armature_save_as_shapekey",
            text="Save (Selection)",
            icon="SHAPEKEY_DATA",
            emboss=True,
        ).use_selection = True
        armature_box.operator(
            "a1_fs.armature_save_as_shapekey",
            text="Save (Armature Children)",
            icon="SHAPEKEY_DATA",
            emboss=True,
        ).use_selection = False
