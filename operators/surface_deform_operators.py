import bpy

from ..common.functions import OverwriteWarnOperator
from ..common.functions import remove_duplicate_shapekey
from ..common.operators import FLEXSHAPE_OT_MeshSelectionOperatorBase

FLEXSHAPE_SURFACE_DEFORM_NAME = "FLEXSHAPE_SURFACE_DEFORM"


def add_surface_deform_and_bind(obj, source_surface_deform):
    surface_deform = obj.modifiers.new(FLEXSHAPE_SURFACE_DEFORM_NAME, "SURFACE_DEFORM")
    surface_deform.target = source_surface_deform
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.surfacedeform_bind(modifier=FLEXSHAPE_SURFACE_DEFORM_NAME)


def remove_flexshape_surface_deform(obj):
    if obj.modifiers is not None:
        for modifier in obj.modifiers:
            if (
                modifier.type == "SURFACE_DEFORM"
                and modifier.name == FLEXSHAPE_SURFACE_DEFORM_NAME
            ):
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_remove(modifier=modifier.name)


def save_surface_deform_as_shapekey(obj, shapekey_name, cleanup_modifier):
    if obj.modifiers is None:
        return False
    for modifier in obj.modifiers:
        if (
            modifier.type == "SURFACE_DEFORM"
            and modifier.name == FLEXSHAPE_SURFACE_DEFORM_NAME
        ):
            remove_duplicate_shapekey(obj, shapekey_name)
            modifier.name = shapekey_name
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_apply_as_shapekey(
                modifier=shapekey_name,
                keep_modifier=not cleanup_modifier,
            )
            if not cleanup_modifier:
                modifier.name = FLEXSHAPE_SURFACE_DEFORM_NAME
            return True
    return False


# noinspection PyPep8Naming
class FLEXSHAPE_OT_SurfaceDeformMeshSelectionOperatorBase(
    FLEXSHAPE_OT_MeshSelectionOperatorBase
):
    def process_objects(self, context, mesh_selection):
        source_surface_deform = context.scene.flexshape_surface_deform_source

        if source_surface_deform is None:
            self.report({"ERROR"}, "Surface Deform Source Mesh was not found")
            return {"CANCELLED"}

        if source_surface_deform in mesh_selection:
            mesh_selection.remove(source_surface_deform)

        if not mesh_selection:
            self.report({"ERROR"}, "No Meshes Selected")
            return {"CANCELLED"}

        self.process_meshes(context, mesh_selection, source_surface_deform)
        return {"FINISHED"}

    def process_meshes(self, context, mesh_selection, source_surface_deform):
        raise NotImplementedError


# noinspection PyPep8Naming
class FLEXSHAPE_OT_AddSurfaceDeform(
    FLEXSHAPE_OT_SurfaceDeformMeshSelectionOperatorBase
):
    bl_idname = "flexshape.add_surface_deform"
    bl_label = "Add Surface Deform"
    bl_description = "Add FlexShape Surface Deform to Selected Meshes"

    def process_meshes(self, context, mesh_selection, source_surface_deform):
        for obj in mesh_selection:
            remove_flexshape_surface_deform(obj)
            add_surface_deform_and_bind(obj, source_surface_deform)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_RemoveSurfaceDeform(FLEXSHAPE_OT_MeshSelectionOperatorBase):
    bl_idname = "flexshape.remove_surface_deform"
    bl_label = "Remove Surface Deform"
    bl_description = "Remove FlexShape Surface Deform from Selected Meshes"

    def process_objects(self, context, mesh_selection):
        for obj in mesh_selection:
            remove_flexshape_surface_deform(obj)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_SurfaceDeformSaveAsShapekey(FLEXSHAPE_OT_MeshSelectionOperatorBase):
    bl_idname = "flexshape.surface_deform_save_as_shapekey"
    bl_label = "Save Surface Deform as Shapekey"
    bl_description = "Save FlexShape Surface Deform to Selected Meshes as Shapekeys"

    # noinspection PyMethodMayBeStatic
    def _check_for_existing_shapekeys(self, context, shapekey_name):
        return any(
            obj.type == "MESH"
            and obj.data.shape_keys
            and shapekey_name in obj.data.shape_keys.key_blocks
            for obj in context.selected_objects
        )

    # noinspection PyMethodMayBeStatic
    def _process_all_objects(self, mesh_selection, shapekey_name, cleanup_modifier):
        for obj in mesh_selection:
            result = save_surface_deform_as_shapekey(
                obj, shapekey_name, cleanup_modifier
            )

            if not result:
                self.report(
                    {"WARNING"},
                    "Failed to save Shapekey for one or more objects",
                )
                print(f"Failed to save Shapekey for {obj.name}")

    def process_objects(self, context, mesh_selection):
        shapekey_name = context.scene.flexshape_surface_deform_shapekey_name
        cleanup_modifier = context.scene.flexshape_surface_deform_auto_remove

        if shapekey_name == "":
            self.report({"ERROR"}, "No Shapekey Name Set")
            return {"CANCELLED"}

        if self._check_for_existing_shapekeys(context, shapekey_name):
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
class FLEXSHAPE_OT_SurfaceDeformMassSave(
    FLEXSHAPE_OT_SurfaceDeformMeshSelectionOperatorBase
):
    bl_idname = "flexshape.surface_deform_mass_save"
    bl_label = "Mass Save Shapekey"
    bl_description = "For Each In List: Add Surface Deform -> Set Shapekey on Source -> Save as Shapekey"

    # noinspection PyMethodMayBeStatic
    def process_meshes(self, context, mesh_selection, source_surface_deform):
        shapekey_list = context.scene.flexshape_surface_deform_shapekey_list
        enabled_shapekeys = [item for item in shapekey_list if item.enabled]

        if enabled_shapekeys is None:
            self.report({"ERROR"}, "No Shapekeys selected")
            return {"CANCELLED"}

        original_values = {}
        for key_block in source_surface_deform.data.shape_keys.key_blocks:
            original_values[key_block.name] = key_block.value
            key_block.value = 0.0

        for obj in mesh_selection:
            remove_flexshape_surface_deform(obj)
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
            remove_flexshape_surface_deform(obj)

        for key_name, value in original_values.items():
            source_surface_deform.data.shape_keys.key_blocks[key_name].value = value

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
