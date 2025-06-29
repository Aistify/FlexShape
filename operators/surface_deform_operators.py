import bpy
from ..common.functions import show_message_box
from ..common.functions import remove_duplicate_shapekey
from ..common.functions import OverwriteWarnOperator


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class A1_FS_OT_ADD_SURFACE_DEFORM(bpy.types.Operator):
    bl_idname = "a1_fs.add_surface_deform"
    bl_label = "add_surface_deform"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def _remove_duplicate_surface_deform(self, obj):
        if obj.modifiers is not None:
            for modifier in obj.modifiers:
                if (
                    modifier.type == "SURFACE_DEFORM"
                    and modifier.name == "A1ST_SURFACE_DEFORM"
                ):
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_remove(modifier=modifier.name)

    def _process_object(self, obj, source_surface_deform):
        surface_deform = obj.modifiers.new("A1ST_SURFACE_DEFORM", "SURFACE_DEFORM")
        surface_deform.target = source_surface_deform
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.surfacedeform_bind(modifier="A1ST_SURFACE_DEFORM")
        return True

    def _process_all_objects(self, context, source_surface_deform):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            self._remove_duplicate_surface_deform(obj)
            self._process_object(obj, source_surface_deform)

    def execute(self, context):
        source_surface_deform = context.scene.a1_fs_surface_deform_source

        if source_surface_deform is None:
            show_message_box("Source Surface Deform was not found.")
            return {"CANCELLED"}

        self._process_all_objects(context, source_surface_deform)

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class A1_FS_OT_REMOVE_SURFACE_DEFORM(bpy.types.Operator):
    bl_idname = "a1_fs.remove_surface_deform"
    bl_label = "remove_surface_deform"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def _process_object(self, obj):
        if obj.modifiers is not None:
            for modifier in obj.modifiers:
                if (
                    modifier.type == "SURFACE_DEFORM"
                    and modifier.name == "A1ST_SURFACE_DEFORM"
                ):
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_remove(modifier=modifier.name)
        return True

    def _process_all_objects(self, context):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            self._process_object(obj)

    def execute(self, context):
        self._process_all_objects(context)

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class A1_FS_OT_SURFACE_DEFORM_SAVE_AS_SHAPEKEY(bpy.types.Operator):
    bl_idname = "a1_fs.surface_deform_save_as_shapekey"
    bl_label = "surface_deform_save_as_shapekey"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def _check_for_existing_shapekeys(self, context, shapekey_name):
        return any(
            obj.type == "MESH"
            and obj.data.shape_keys
            and shapekey_name in obj.data.shape_keys.key_blocks
            for obj in context.selected_objects
        )

    def _process_object(self, obj, shapekey_name, remove_surface_deform):
        if obj.modifiers is not None:
            for modifier in obj.modifiers:
                if (
                    modifier.type == "SURFACE_DEFORM"
                    and modifier.name == "A1ST_SURFACE_DEFORM"
                ):
                    remove_duplicate_shapekey(obj, shapekey_name)
                    modifier.name = shapekey_name
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_apply_as_shapekey(
                        modifier=shapekey_name,
                        keep_modifier=not remove_surface_deform,
                    )

        return True

    def _process_all_objects(self, context, shapekey_name, remove_surface_deform):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            self._process_object(obj, shapekey_name, remove_surface_deform)

    def execute(self, context):
        shapekey_name = context.scene.a1_fs_surface_deform_shapekey_name
        remove_surface_deform = context.scene.a1_fs_surface_deform_auto_remove

        if shapekey_name == "":
            show_message_box("Shapekey Name was not set.")
            return {"CANCELLED"}

        if self._check_for_existing_shapekeys(context, shapekey_name):
            OverwriteWarnOperator.register_with_callback(
                lambda ctx: self._process_all_objects(
                    ctx, shapekey_name, remove_surface_deform
                )
            )
            bpy.ops.a1_fs.overwrite_dialogue("INVOKE_DEFAULT")
        else:
            self._process_all_objects(context, shapekey_name, remove_surface_deform)

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


classes = (
    A1_FS_OT_ADD_SURFACE_DEFORM,
    A1_FS_OT_REMOVE_SURFACE_DEFORM,
    A1_FS_OT_SURFACE_DEFORM_SAVE_AS_SHAPEKEY,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
