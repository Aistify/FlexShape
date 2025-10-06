import bpy


# noinspection PyPep8Naming
class FLEXSHAPE_OT_SelectJsonFile(bpy.types.Operator):
    bl_idname = "flexshape.select_json_file"
    bl_label = "select_json_file"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyTypeHints
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    # noinspection PyTypeHints
    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={"HIDDEN"},
        maxlen=255,
    )

    def execute(self, context):
        context.scene.flexshape_placeholder_json_file = self.filepath
        return {"FINISHED"}

    def invoke(self, context, _):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


def register():
    bpy.utils.register_class(FLEXSHAPE_OT_SelectJsonFile)


def unregister():
    bpy.utils.unregister_class(FLEXSHAPE_OT_SelectJsonFile)
