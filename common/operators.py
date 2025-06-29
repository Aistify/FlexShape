import bpy


class A1_FS_OT_SELECT_JSON_FILE(bpy.types.Operator):
    bl_idname = "a1_fs.select_json_file"
    bl_label = "select_json_file"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={"HIDDEN"},
        maxlen=255,
    )

    def execute(self, context):
        context.scene.a1_fs_json_file = self.filepath
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


def register():
    bpy.utils.register_class(A1_FS_OT_SELECT_JSON_FILE)


def unregister():
    bpy.utils.unregister_class(A1_FS_OT_SELECT_JSON_FILE)
