import bpy

from ..common.operators import FLEXSHAPE_OT_MeshSelectionOperatorBase
from ..common.functions import remove_duplicate_shapekey
from ..common.functions import OverwriteWarnOperator


FLEXSHAPE_LATTICE_NAME = "FLEXSHAPE_LATTICE"


def add_flexshape_lattice(obj, source_lattice):
    lattice = obj.modifiers.new(FLEXSHAPE_LATTICE_NAME, "LATTICE")
    lattice.object = source_lattice


def remove_flexshape_lattice(obj):
    if obj.modifiers is not None:
        for modifier in obj.modifiers:
            if modifier.type == "LATTICE" and modifier.name == FLEXSHAPE_LATTICE_NAME:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_remove(modifier=modifier.name)


def save_lattice_as_shapekey(obj, shapekey_name, cleanup_modifier):
    if obj.modifiers is not None:
        for modifier in obj.modifiers:
            if modifier.type == "LATTICE" and modifier.name == FLEXSHAPE_LATTICE_NAME:
                remove_duplicate_shapekey(obj, shapekey_name)
                modifier.name = shapekey_name
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_apply_as_shapekey(
                    modifier=modifier.name, keep_modifier=cleanup_modifier
                )
                if cleanup_modifier:
                    modifier.name = FLEXSHAPE_LATTICE_NAME
                return True
    return False


def quick_save_lattice_as_shapekey(obj, source_lattice, shapekey_name=""):
    if shapekey_name == "":
        if source_lattice is None:
            return False
        shapekey_name = source_lattice.name

    remove_flexshape_lattice(obj)
    add_flexshape_lattice(obj, source_lattice)
    save_lattice_as_shapekey(obj, shapekey_name, False)
    return True


# noinspection PyPep8Naming
class FLEXSHAPE_OT_AddLattice(FLEXSHAPE_OT_MeshSelectionOperatorBase):
    bl_idname = "flexshape.add_lattice"
    bl_label = "Add Lattice"
    bl_description = "Add FlexShape Lattice to Selected Meshes"

    def process_objects(self, context, mesh_selection):
        source_lattice = context.scene.flexshape_lattice_source

        if source_lattice is None:
            self.report({"ERROR"}, "No Source Lattice set")
            return {"CANCELLED"}

        for obj in mesh_selection:
            remove_flexshape_lattice(obj)
            add_flexshape_lattice(obj, source_lattice)

        return {"FINISHED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_RemoveLattice(FLEXSHAPE_OT_MeshSelectionOperatorBase):
    bl_idname = "flexshape.remove_lattice"
    bl_label = "Remove Lattice"
    bl_description = "Remove FlexShape Lattice Modifier from Selected Meshes"

    def process_objects(self, context, mesh_selection):
        for obj in mesh_selection:
            remove_flexshape_lattice(obj)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_LatticeSaveAsShapekey(FLEXSHAPE_OT_MeshSelectionOperatorBase):
    bl_idname = "flexshape.lattice_save_as_shapekey"
    bl_label = "Save Lattice as Shapekey"
    bl_description = "Save FlexShape Lattice Modifier as Shapekey to Selected Meshes"

    # noinspection PyMethodMayBeStatic
    def _check_for_existing_shapekeys(self, target_objects, shapekey_name):
        return any(
            obj.data.shape_keys and shapekey_name in obj.data.shape_keys.key_blocks
            for obj in target_objects
        )

    # noinspection PyMethodMayBeStatic
    def _process_all_objects(self, selected_objects, shapekey_name, cleanup_modifier):
        for obj in selected_objects:
            result = save_lattice_as_shapekey(obj, shapekey_name, cleanup_modifier)

            if not result:
                self.report(
                    {"WARNING"},
                    "Failed to save Shapekey for one or more objects",
                )
                print(f"Failed to save Shapekey for {obj.name}")

    def process_objects(self, context, mesh_selection):
        cleanup_modifier = context.scene.flexshape_lattice_auto_remove

        shapekey_name = context.scene.flexshape_lattice_shapekey_name
        if shapekey_name == "":
            if not context.scene.flexshape_lattice_source:
                self.report({"ERROR"}, "Source Lattice or Shapekey Name was not found")
                return {"CANCELLED"}
            shapekey_name = context.scene.flexshape_lattice_source.name

        if self._check_for_existing_shapekeys(mesh_selection, shapekey_name):
            OverwriteWarnOperator.register_with_callback(
                lambda _: self._process_all_objects(
                    mesh_selection, shapekey_name, cleanup_modifier
                )
            )
            # noinspection PyUnresolvedReferences
            bpy.ops.flexshape.overwrite_dialogue("INVOKE_DEFAULT")
        else:
            self._process_all_objects(mesh_selection, shapekey_name, cleanup_modifier)

        return {"FINISHED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_LatticeQuickSave(FLEXSHAPE_OT_MeshSelectionOperatorBase):
    bl_idname = "flexshape.lattice_quick_save"
    bl_label = "Quick Save Shapekey"
    bl_description = "Add Lattice -> Save as Shapekey"

    # noinspection PyMethodMayBeStatic
    def process_objects(self, context, mesh_selection):
        source_lattice = context.scene.flexshape_lattice_source
        shapekey_name = context.scene.flexshape_lattice_shapekey_name

        if source_lattice is None:
            self.report({"ERROR"}, "Source Lattice was not found")
            return {"CANCELLED"}

        for obj in mesh_selection:
            result = quick_save_lattice_as_shapekey(
                obj, source_lattice.lattice, shapekey_name
            )

            if not result:
                self.report(
                    {"WARNING"},
                    "Failed to save Shapekey for one or more objects",
                )
                print(f"Failed to save Shapekey for {obj.name}")

        return {"FINISHED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_LatticeMassSave(FLEXSHAPE_OT_MeshSelectionOperatorBase):
    bl_idname = "flexshape.lattice_mass_save"
    bl_label = "Mass Save Shapekey"
    bl_description = "For Each in List: Add Lattice -> Save as Shapekey"

    # noinspection PyMethodMayBeStatic
    def process_objects(self, context, mesh_selection):
        lattice_list = context.scene.flexshape_lattice_list

        if len(lattice_list) == 0:
            self.report({"ERROR"}, "No Lattices Set")
            return {"CANCELLED"}

        for obj in mesh_selection:
            for lattice_list_item in lattice_list:
                result = quick_save_lattice_as_shapekey(obj, lattice_list_item.lattice)

                if not result:
                    self.report(
                        {"WARNING"},
                        "Failed to save Shapekey for one or more objects",
                    )
                    print(f"Failed to save Shapekey for {obj.name}")

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
