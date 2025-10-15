import bpy
import numpy as np

from ..common.functions import get_meshes_from_selection


# noinspection PyPep8Naming
class FLEXSHAPE_OT_UtilsRemoveZeroShapekeys(bpy.types.Operator):
    bl_idname = "flexshape.utils_remove_empty_shapekeys"
    bl_label = "Remove Empty Shapekeys"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyTypeHints
    use_selection: bpy.props.BoolProperty(
        name="Use Selection",
        description="Process only selected mesh objects?",
        default=True,
    )

    # noinspection PyMethodMayBeStatic
    def _process_object(self, obj, threshold, prefixes_to_skip=None):
        if prefixes_to_skip is None:
            prefixes_to_skip = []

        shape_keys = obj.data.shape_keys.key_blocks
        num_vertices = len(obj.data.vertices)

        vertex_locations = np.empty(
            (len(shape_keys), num_vertices * 3), dtype=np.float32
        )

        for i, shape_key in enumerate(shape_keys):
            if shape_key == shape_key.relative_key:
                continue

            shape_key.data.foreach_get("co", vertex_locations[i])
            relative_data = np.empty(num_vertices * 3, dtype=np.float32)
            shape_key.relative_key.data.foreach_get("co", relative_data)

            vertex_locations[i] -= relative_data

        to_delete = np.all(np.abs(vertex_locations[1:]) < threshold, axis=1)

        names_to_delete = [
            sk.name
            for sk, delete in zip(shape_keys[1:], to_delete)
            if delete
            and not any(sk.name.startswith(prefix) for prefix in prefixes_to_skip)
        ]

        print(f"Deleted Shapekey from {obj.name}:")
        for name in names_to_delete:
            print(f"  - {name}")
            obj.shape_key_remove(obj.data.shape_keys.key_blocks[name])

        return len(names_to_delete)

    def _process_all_objects(self, context):
        total_deleted = 0

        if self.use_selection:
            target_objects = context.selected_objects
        else:
            active_obj = context.active_object
            if not active_obj:
                self.report({"ERROR"}, "No active object selected")
                return False
            if active_obj.type != "ARMATURE":
                self.report({"ERROR"}, "Active object must be an armature.")
                return False

            target_objects = active_obj.children

        for obj in target_objects:
            if obj.type != "MESH":
                continue

            if obj.data.shape_keys is None:
                continue

            threshold = context.scene.flexshape_utils_shapekey_threshold
            prefixes_to_skip = [
                prefix.strip()
                for prefix in context.scene.flexshape_utils_skip_prefix.split(",")
                if prefix.strip()
            ]

            deleted = self._process_object(obj, threshold, prefixes_to_skip)
            total_deleted += deleted

        if total_deleted > 0:
            self.report(
                {"INFO"},
                f"Deleted {total_deleted} Shapekeys across {len(target_objects)} objects",
            )
            return True
        else:
            self.report({"INFO"}, "No Shapekey were deleted")
            return True

    def execute(self, context):
        if not self._process_all_objects(context):
            return {"CANCELLED"}

        return {"FINISHED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_UtilsSetShapekey0(bpy.types.Operator):
    bl_idname = "flexshape.utils_set_shapekey_0"
    bl_label = "Set Shapekeys to 0"
    bl_description = "Set Selected Objects Shapekeys to 0"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyTypeHints
    use_selection: bpy.props.BoolProperty(
        name="Use Selection",
        description="Process only selected mesh objects?",
        default=True,
    )

    # noinspection PyTypeHints
    use_surface_deform_source: bpy.props.BoolProperty(
        name="Use Surface Deform Source",
        description="Process surface deform source?",
        default=False,
    )

    # noinspection PyMethodMayBeStatic
    def _set_shapekey_to_0(self, obj):
        if not obj.data.shape_keys:
            return
        for shapekey in obj.data.shape_keys.key_blocks[1:]:
            shapekey.value = 0.0

    def execute(self, context):
        if not self.use_surface_deform_source:
            target_objects = get_meshes_from_selection(self, context)
            if target_objects is None:
                return {"CANCELLED"}

            for obj in target_objects:
                self._set_shapekey_to_0(obj)
        else:
            surface_deform_source = context.scene.flexshape_surface_deform_source
            if surface_deform_source is None:
                self.report({"ERROR"}, "No Surface Deform Source Mesh set")
                return {"CANCELLED"}

            self._set_shapekey_to_0(surface_deform_source)

        return {"FINISHED"}


classes = (FLEXSHAPE_OT_UtilsRemoveZeroShapekeys, FLEXSHAPE_OT_UtilsSetShapekey0)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
