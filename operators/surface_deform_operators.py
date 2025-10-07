import bpy
from ..common.functions import show_message_box
from ..common.functions import remove_duplicate_shapekey
from ..common.functions import OverwriteWarnOperator


def remove_duplicate_surface_deform(obj):
    if obj.modifiers is not None:
        for modifier in obj.modifiers:
            if (
                modifier.type == "SURFACE_DEFORM"
                and modifier.name == "A1ST_SURFACE_DEFORM"
            ):
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_remove(modifier=modifier.name)
    return True


def add_surface_deform_and_bind(obj, source_surface_deform):
    surface_deform = obj.modifiers.new("A1ST_SURFACE_DEFORM", "SURFACE_DEFORM")
    surface_deform.target = source_surface_deform
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.surfacedeform_bind(modifier="A1ST_SURFACE_DEFORM")
    return True


def remove_surface_deform(obj):
    if obj.modifiers is not None:
        for modifier in obj.modifiers:
            if (
                modifier.type == "SURFACE_DEFORM"
                and modifier.name == "A1ST_SURFACE_DEFORM"
            ):
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_remove(modifier=modifier.name)
    return True


def save_surface_deform_as_shapekey(obj, shapekey_name, cleanup_modifier):
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
                    keep_modifier=not cleanup_modifier,
                )
                if not cleanup_modifier:
                    modifier.name = "A1ST_SURFACE_DEFORM"

    return True


# noinspection PyPep8Naming
class FLEXSHAPE_OT_AddSurfaceDeform(bpy.types.Operator):
    bl_idname = "flexshape.add_surface_deform"
    bl_label = "add_surface_deform"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def _process_all_objects(self, context, source_surface_deform):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            remove_duplicate_surface_deform(obj)
            add_surface_deform_and_bind(obj, source_surface_deform)

    def execute(self, context):
        source_surface_deform = context.scene.flexshape_surface_deform_source

        if source_surface_deform is None:
            show_message_box("Source Surface Deform was not found.")
            return {"CANCELLED"}

        self._process_all_objects(context, source_surface_deform)

        return {"FINISHED"}

    def invoke(self, context, _):
        return self.execute(context)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_RemoveSurfaceDeform(bpy.types.Operator):
    bl_idname = "flexshape.remove_surface_deform"
    bl_label = "remove_surface_deform"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def _process_all_objects(self, context):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            remove_surface_deform(obj)

    def execute(self, context):
        self._process_all_objects(context)

        return {"FINISHED"}

    def invoke(self, context, _):
        return self.execute(context)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_SurfaceDeformSaveAsShapekey(bpy.types.Operator):
    bl_idname = "flexshape.surface_deform_save_as_shapekey"
    bl_label = "surface_deform_save_as_shapekey"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def _check_for_existing_shapekeys(self, context, shapekey_name):
        return any(
            obj.type == "MESH"
            and obj.data.shape_keys
            and shapekey_name in obj.data.shape_keys.key_blocks
            for obj in context.selected_objects
        )

    # noinspection PyMethodMayBeStatic
    def _process_all_objects(self, context, shapekey_name, cleanup_modifier):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            save_surface_deform_as_shapekey(obj, shapekey_name, cleanup_modifier)

    def execute(self, context):
        shapekey_name = context.scene.flexshape_surface_deform_shapekey_name
        cleanup_modifier = context.scene.flexshape_surface_deform_auto_remove

        if shapekey_name == "":
            show_message_box("Shapekey Name was not set.")
            return {"CANCELLED"}

        if self._check_for_existing_shapekeys(context, shapekey_name):
            OverwriteWarnOperator.register_with_callback(
                lambda ctx: self._process_all_objects(
                    ctx, shapekey_name, cleanup_modifier
                )
            )
            # noinspection PyUnresolvedReferences
            bpy.ops.flexshape.overwrite_dialogue("INVOKE_DEFAULT")
        else:
            self._process_all_objects(context, shapekey_name, cleanup_modifier)

        return {"FINISHED"}

    def invoke(self, context, _):
        return self.execute(context)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_SurfaceDeformMassSave(bpy.types.Operator):
    bl_idname = "flexshape.surface_deform_mass_save"
    bl_label = "Mass Save Shape Key"
    bl_description = "For Each In List: Add Surface Deform -> Set Shapekey on Source -> Save As Shape Key"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        active_obj = context.active_object
        selected_objects = [
            obj for obj in context.selected_objects if obj.type == "MESH"
        ]
        original_values = {}
        source_surface_deform = context.scene.flexshape_surface_deform_source
        shapekey_list = context.scene.flexshape_surface_deform_shapekey_list
        enabled_shapekeys = [item for item in shapekey_list if item.enabled]

        for key_block in source_surface_deform.data.shape_keys.key_blocks:
            original_values[key_block.name] = key_block.value
            key_block.value = 0.0

        for obj in selected_objects:
            remove_duplicate_surface_deform(obj)
            add_surface_deform_and_bind(obj, source_surface_deform)
            for shapekey_item in enabled_shapekeys:
                source_surface_deform.data.shape_keys.key_blocks[
                    shapekey_item.name
                ].value = 1.0
                context.view_layer.update()
                save_surface_deform_as_shapekey(obj, shapekey_item.name, False)
                source_surface_deform.data.shape_keys.key_blocks[
                    shapekey_item.name
                ].value = 0.0
            remove_surface_deform(obj)

        for key_name, value in original_values.items():
            source_surface_deform.data.shape_keys.key_blocks[key_name].value = value

        for obj in selected_objects:
            obj.select_set(True)
        context.view_layer.objects.active = active_obj

        return {"FINISHED"}


classes = (
    FLEXSHAPE_OT_AddSurfaceDeform,
    FLEXSHAPE_OT_RemoveSurfaceDeform,
    FLEXSHAPE_OT_SurfaceDeformSaveAsShapekey,
    FLEXSHAPE_OT_SurfaceDeformMassSave,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
