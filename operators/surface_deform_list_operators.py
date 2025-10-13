import bpy


# noinspection PyPep8Naming
class FLEXSHAPE_UL_SurfaceDeformShapekeyList(bpy.types.UIList):
    def draw_item(self, _, layout, __, item, ___, ____, _____, ______):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            layout.prop(item, "enabled", text="")
            layout.label(text=item.name, icon="SHAPEKEY_DATA")


# noinspection PyPep8Naming
class FLEXSHAPE_OT_LoadSourceShapekeys(bpy.types.Operator):
    bl_idname = "flexshape.load_source_shapekeys"
    bl_label = "Load Shapekeys"
    bl_description = "Load shapekeys from source mesh"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        source = context.scene.flexshape_surface_deform_source

        if source is None or source.type != "MESH":
            self.report({"WARNING"}, "No valid source mesh selected")
            return {"CANCELLED"}

        if not source.data.shape_keys:
            self.report({"WARNING"}, "Source mesh has no shapekeys")
            return {"CANCELLED"}

        context.scene.flexshape_surface_deform_shapekey_list.clear()

        for key in source.data.shape_keys.key_blocks:
            if key.name == "Basis":
                continue
            item = context.scene.flexshape_surface_deform_shapekey_list.add()
            item.name = key.name
            item.enabled = False

        self.report(
            {"INFO"},
            f"Loaded {len(context.scene.flexshape_surface_deform_shapekey_list)} shapekeys",
        )
        return {"FINISHED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_SelectAllShapekeys(bpy.types.Operator):
    bl_idname = "flexshape.select_all_shapekeys"
    bl_label = "Select All"
    bl_description = "Select all shapekeys"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        for item in context.scene.flexshape_surface_deform_shapekey_list:
            item.enabled = True
        return {"FINISHED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_DeselectAllShapekeys(bpy.types.Operator):
    bl_idname = "flexshape.deselect_all_shapekeys"
    bl_label = "Deselect All"
    bl_description = "Deselect all shapekeys"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        for item in context.scene.flexshape_surface_deform_shapekey_list:
            item.enabled = False
        return {"FINISHED"}


classes = (
    FLEXSHAPE_UL_SurfaceDeformShapekeyList,
    FLEXSHAPE_OT_LoadSourceShapekeys,
    FLEXSHAPE_OT_SelectAllShapekeys,
    FLEXSHAPE_OT_DeselectAllShapekeys,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
