import bpy
from os.path import basename as os_path_basename


# noinspection PyPep8Naming
class FLEXSHAPE_PT_blendshape_utils(bpy.types.Panel):
    bl_idname = "FLEXSHAPE_PT_blendshape_utils"
    bl_label = "Misc Utils"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FlexShape"
    bl_options = {"DEFAULT_CLOSED"}

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
            "flexshape_surface_deform_source",
            text="Source",
            icon="MESH_DATA",
            emboss=True,
        )
        if context.scene.flexshape_placeholder_json_file:
            filename = os_path_basename(context.scene.flexshape_placeholder_json_file)
            face_revert_shapekey_setup_box.label(
                text=f"Loaded: {filename}", icon="CHECKMARK"
            )
        else:
            face_revert_shapekey_setup_box.label(text=f"No Files Loaded", icon="ERROR")
        face_revert_shapekey_setup_box.operator(
            "flexshape.select_json_file", text="Select JSON File", icon="FILE_FOLDER"
        )

        # face_revert_shapekey_setup_box.prop(
        #     context.scene,
        #     "flexshape_placeholder_generate_face_revert_shapekeys",
        #     text="Generate Reverts for Face Shapekeys",
        #     icon_value=0,
        #     emboss=True,
        # )
