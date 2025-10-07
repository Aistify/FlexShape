import bpy
from ..common.functions import show_message_box
from ..common.functions import remove_duplicate_shapekey
from ..common.functions import OverwriteWarnOperator


def save_lattice_as_shapekey(obj, shapekey_name, keep_lattice):
    if obj.modifiers is not None:
        for modifier in obj.modifiers:
            if modifier.type == "LATTICE" and modifier.name == "A1ST_LATTICE":
                remove_duplicate_shapekey(obj, shapekey_name)
                modifier.name = shapekey_name
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_apply_as_shapekey(
                    modifier=modifier.name, keep_modifier=keep_lattice
                )
                if keep_lattice:
                    modifier.name = "A1ST_LATTICE"

    return True


def remove_duplicate_lattice(obj):
    if obj.modifiers is not None:
        for modifier in obj.modifiers:
            if modifier.type == "LATTICE" and modifier.name == "A1ST_LATTICE":
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_remove(modifier=modifier.name)


def add_lattice(obj, source_lattice):
    lattice = obj.modifiers.new("A1ST_LATTICE", "LATTICE")
    lattice.object = source_lattice
    return True


def quick_save_lattice_as_shapekey(obj, source_lattice, shapekey_name=""):
    if shapekey_name == "":
        shapekey_name = source_lattice.name

    remove_duplicate_lattice(obj)
    add_lattice(obj, source_lattice)
    save_lattice_as_shapekey(obj, shapekey_name, False)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_AddLattice(bpy.types.Operator):
    bl_idname = "flexshape.add_lattice"
    bl_label = "add_lattice"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def _process_all_objects(self, context, source_lattice):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            remove_duplicate_lattice(obj)
            add_lattice(obj, source_lattice)

    def execute(self, context):
        source_lattice = context.scene.flexshape_lattice_source

        if source_lattice is None:
            show_message_box("Source Lattice was not found.")
            return {"CANCELLED"}

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
    def _process_all_objects(self, context, shapekey_name, remove_lattice):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            save_lattice_as_shapekey(obj, shapekey_name, remove_lattice)

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


# noinspection PyPep8Naming
class FLEXSHAPE_OT_LatticeQuickSave(bpy.types.Operator):
    bl_idname = "flexshape.lattice_quick_save"
    bl_label = "Quick Save Shape Key"
    bl_description = "Add Lattice -> Save As Shape Key"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        source_lattice = context.scene.flexshape_lattice_source
        shapekey_name = context.scene.flexshape_lattice_shapekey_name

        if source_lattice is None:
            show_message_box("Source Lattice was not found.")
            return {"CANCELLED"}

        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            quick_save_lattice_as_shapekey(obj, source_lattice, shapekey_name)

        return {"FINISHED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_LatticeMassSave(bpy.types.Operator):
    bl_idname = "flexshape.lattice_mass_save"
    bl_label = "Mass Save Shape Key"
    bl_description = "For Each In List: Add Lattice -> Save As Shape Key"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        active_obj = context.active_object
        selected_objects = [
            obj for obj in context.selected_objects if obj.type == "MESH"
        ]
        lattice_list = context.scene.flexshape_lattice_list

        for obj in selected_objects:
            for lattice_list_item in lattice_list:
                quick_save_lattice_as_shapekey(obj, lattice_list_item.lattice)

        for obj in selected_objects:
            obj.select_set(True)
        context.view_layer.objects.active = active_obj

        return {"FINISHED"}


classes = (
    FLEXSHAPE_OT_AddLattice,
    FLEXSHAPE_OT_RemoveLattice,
    FLEXSHAPE_OT_LatticeSaveAsShapekey,
    FLEXSHAPE_OT_LatticeQuickSave,
    FLEXSHAPE_OT_LatticeMassSave,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
