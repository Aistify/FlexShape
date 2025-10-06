import bpy
from ..common.functions import show_message_box
from ..common.functions import remove_duplicate_shapekey
from ..common.functions import OverwriteWarnOperator


# noinspection PyPep8Naming
class FLEXSHAPE_OT_AddLattice(bpy.types.Operator):
    bl_idname = "flexshape.add_lattice"
    bl_label = "add_lattice"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def _check_for_duplicates(self, context):
        return any(
            obj.type == "MESH"
            and any(
                mod.type == "LATTICE" and mod.name == "A1ST_LATTICE"
                for mod in obj.modifiers
            )
            for obj in context.selected_objects
        )

    # noinspection PyMethodMayBeStatic
    def _remove_duplicate_lattice(self, obj):
        if obj.modifiers is not None:
            for modifier in obj.modifiers:
                if modifier.type == "LATTICE" and modifier.name == "A1ST_LATTICE":
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_remove(modifier=modifier.name)

    # noinspection PyMethodMayBeStatic
    def _process_object(self, obj, source_lattice):
        lattice = obj.modifiers.new("A1ST_LATTICE", "LATTICE")
        lattice.object = source_lattice
        return True

    def _process_all_objects(self, context, source_lattice):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            self._remove_duplicate_lattice(obj)
            self._process_object(obj, source_lattice)

    def execute(self, context):
        source_lattice = context.scene.flexshape_lattice_source

        if source_lattice is None:
            show_message_box("Source Lattice was not found.")
            return {"CANCELLED"}

        if self._check_for_duplicates(context):
            OverwriteWarnOperator.register_with_callback(
                lambda ctx: self._process_all_objects(ctx, source_lattice)
            )
            # noinspection PyUnresolvedReferences
            bpy.ops.flexshape.overwrite_dialogue("INVOKE_DEFAULT")
        else:
            self._process_all_objects(context, source_lattice)

        return {"FINISHED"}

    def invoke(self, context, _):
        return self.execute(context)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_RemoveLattice(bpy.types.Operator):
    bl_idname = "flexshape.remove_lattice"
    bl_label = "remove_lattice"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def _process_object(self, obj):
        if obj.modifiers is not None:
            for modifier in obj.modifiers:
                if modifier.type == "LATTICE" and modifier.name == "A1ST_LATTICE":
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

    def invoke(self, context, _):
        return self.execute(context)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_LatticeSaveAsShapekey(bpy.types.Operator):
    bl_idname = "flexshape.lattice_save_as_shapekey"
    bl_label = "lattice_save_as_shapekey"
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
    def _process_object(self, obj, shapekey_name, remove_lattice):
        if obj.modifiers is not None:
            for modifier in obj.modifiers:
                if modifier.type == "LATTICE" and modifier.name == "A1ST_LATTICE":
                    remove_duplicate_shapekey(obj, shapekey_name)
                    modifier.name = shapekey_name
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_apply_as_shapekey(
                        modifier=modifier.name, keep_modifier=not remove_lattice
                    )
                    if not remove_lattice:
                        modifier.name = "A1ST_LATTICE"

        return True

    def _process_all_objects(self, context, shapekey_name, remove_lattice):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            self._process_object(obj, shapekey_name, remove_lattice)

    def execute(self, context):
        shapekey_name = context.scene.flexshape_lattice_shapekey_name
        remove_lattice = context.scene.flexshape_lattice_auto_remove

        if shapekey_name == "":
            shapekey_name = context.scene.flexshape_lattice_source.name

        if self._check_for_existing_shapekeys(context, shapekey_name):
            OverwriteWarnOperator.register_with_callback(
                lambda ctx: self._process_all_objects(
                    ctx, shapekey_name, remove_lattice
                )
            )
            # noinspection PyUnresolvedReferences
            bpy.ops.flexshape.overwrite_dialogue("INVOKE_DEFAULT")
        else:
            self._process_all_objects(context, shapekey_name, remove_lattice)

        return {"FINISHED"}

    def invoke(self, context, _):
        return self.execute(context)


classes = (
    FLEXSHAPE_OT_AddLattice,
    FLEXSHAPE_OT_RemoveLattice,
    FLEXSHAPE_OT_LatticeSaveAsShapekey,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
