import bpy
from os.path import basename as os_path_basename


class A1_FS_PT_BLENDSHAPE_UTILS_PANEL(bpy.types.Panel):
    bl_label = "FlexShape Placeholder Panel"
    bl_idname = "A1_FS_PT_BLENDSHAPE_UTILS_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    # noinspection PyUnusedLocal
    @classmethod
    def poll(cls, context):
        return False

    def draw(self, context):
        layout = self.layout

        face_revert_shapekey_setup_box = layout.box()
        face_revert_shapekey_setup_box.label(
            text="Revert Shapekeys Setup", icon="SHAPEKEY_DATA"
        )
        face_revert_shapekey_setup_box.prop(
            context.scene,
            "a1_fs_surface_deform_source",
            text="Source",
            icon="MESH_DATA",
            emboss=True,
        )
        if context.scene.a1_fs_json_file:
            filename = os_path_basename(context.scene.a1_fs_json_file)
            face_revert_shapekey_setup_box.label(
                text=f"Loaded: {filename}", icon="CHECKMARK"
            )
        else:
            face_revert_shapekey_setup_box.label(text=f"No Files Loaded", icon="ERROR")
        face_revert_shapekey_setup_box.operator(
            "a1_fs.select_json_file", text="Select JSON File", icon="FILE_FOLDER"
        )

        # face_revert_shapekey_setup_box.prop(
        #     context.scene,
        #     "a1_fs_placeholder_generate_face_revert_shapekeys",
        #     text="Generate Reverts for Face Shapekeys",
        #     icon_value=0,
        #     emboss=True,
        # )
