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


# noinspection PyPep8Naming
class FLEXSHAPE_OT_MeshSelectionOperatorBase(bpy.types.Operator):
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        mesh_selection = [obj for obj in context.selected_objects if obj.type == "MESH"]

        if not mesh_selection:
            self.report({"ERROR"}, "No Meshes selected")
            return {"CANCELLED"}

        self.process_objects(context, mesh_selection)
        return {"FINISHED"}

    def process_objects(self, context, mesh_selection):
        raise NotImplementedError


classes = (
    FLEXSHAPE_OT_SelectJsonFile,
    FLEXSHAPE_OT_MeshSelectionOperatorBase,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
