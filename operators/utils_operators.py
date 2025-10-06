import bpy
import numpy as np
from ..common.functions import show_message_box


# noinspection PyPep8Naming
class FLEXSHAPE_OT_UtilsRemoveZeroShapekeys(bpy.types.Operator):
    bl_idname = "flexshape.utils_remove_zero_shapekeys"
    bl_label = "utils_remove_zero_shapekeys"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyTypeHints
    use_selection: bpy.props.BoolProperty(
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

        print(f"Deleted shape keys from {obj.name}:")
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
                show_message_box("No active object selected.")
                return {"CANCELLED"}
            if active_obj.type != "ARMATURE":
                show_message_box("Active object must be an armature.")
                return {"CANCELLED"}

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
                f"Deleted {total_deleted} shape keys across {len(target_objects)} objects",
            )
            return {"FINISHED"}
        else:
            self.report({"INFO"}, "No shape keys were deleted")
            return {"FINISHED"}

    def execute(self, context):
        self._process_all_objects(context)

        return {"FINISHED"}

    def invoke(self, context, _):
        return self.execute(context)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_UtilsSetShapekey0(bpy.types.Operator):
    bl_idname = "flexshape.utils_set_shapekey_0"
    bl_label = "utils_set_shapekey_0"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyTypeHints
    use_selection: bpy.props.BoolProperty(
        default=True,
    )

    # noinspection PyMethodMayBeStatic
    def _process_object(self, obj):
        for shapekey in obj.data.shape_keys.key_blocks[1:]:
            shapekey.value = 0.0

        return True

    def _process_all_objects(self, context):
        if self.use_selection:
            target_objects = context.selected_objects
        else:
            target_objects = [context.scene.flexshape_surface_deform_source]

        for obj in target_objects:
            if obj.type != "MESH":
                continue

            if obj.data.shape_keys is None:
                continue

            self._process_object(obj)

    def execute(self, context):
        self._process_all_objects(context)

        return {"FINISHED"}

    def invoke(self, context, _):
        return self.execute(context)


classes = (FLEXSHAPE_OT_UtilsRemoveZeroShapekeys, FLEXSHAPE_OT_UtilsSetShapekey0)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
