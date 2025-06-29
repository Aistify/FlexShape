import bpy
from ..common.functions import show_message_box
from ..common.functions import remove_duplicate_shapekey
from ..common.functions import OverwriteWarnOperator


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class A1_FS_OT_COPY_POSE_RELATIONS(bpy.types.Operator):
    bl_idname = "a1_fs.copy_pose_relations"
    bl_label = "copy_pose_relations"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def _copy_pose_relations(self, armature, source_pose_bones):
        target_pose_bones = armature.pose.bones

        for source_bone in source_pose_bones:
            if source_bone.name in target_pose_bones:
                target_bone = target_pose_bones[source_bone.name]

                target_bone.bone.use_relative_parent = source_pose_bones[
                    source_bone.name
                ].bone.use_relative_parent
                target_bone.bone.use_local_location = source_pose_bones[
                    source_bone.name
                ].bone.use_local_location
                target_bone.bone.use_inherit_rotation = source_pose_bones[
                    source_bone.name
                ].bone.use_inherit_rotation
                target_bone.bone.inherit_scale = source_pose_bones[
                    source_bone.name
                ].bone.inherit_scale

    def execute(self, context):
        source_armature = bpy.context.scene.a1_fs_armature_source

        if source_armature is None:
            show_message_box("Source Armature was not found.")
            return {"CANCELLED"}

        source_pose_bones = source_armature.pose.bones

        for target_armature in bpy.context.selected_objects:
            if target_armature.type != "ARMATURE":
                continue
            if target_armature == source_armature:
                continue

            self._copy_pose_relations(target_armature, source_pose_bones)

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class A1_FS_OT_COPY_POSE_TRANSFORMS(bpy.types.Operator):
    bl_idname = "a1_fs.copy_pose_transforms"
    bl_label = "copy_pose_transforms"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def _copy_pose_transforms(self, armature, source_pose_bones):
        target_pose_bones = armature.pose.bones

        for source_bone in source_pose_bones:
            if source_bone.name in target_pose_bones:
                target_bone = target_pose_bones[source_bone.name]
                target_bone.matrix_basis = source_bone.matrix_basis.copy()

    def execute(self, context):
        source_armature = context.scene.a1_fs_armature_source

        if source_armature is None:
            show_message_box("Source Armature was not found.")
            return {"CANCELLED"}

        source_pose_bones = source_armature.pose.bones

        for target_armature in bpy.context.selected_objects:
            if target_armature.type != "ARMATURE":
                continue
            if target_armature == source_armature:
                continue

            self._copy_pose_transforms(target_armature, source_pose_bones)

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class A1_FS_OT_CLEAR_POSE_TRANSFORMS(bpy.types.Operator):
    bl_idname = "a1_fs.clear_pose_transforms"
    bl_label = "clear_pose_transforms"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def execute(self, context):
        selection = bpy.context.selected_objects
        original_active = context.active_object

        for obj in selection:
            if obj.type == "ARMATURE":
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode="POSE")
                bpy.ops.pose.select_all(action="SELECT")
                bpy.ops.pose.transforms_clear()
                bpy.ops.object.mode_set(mode="OBJECT")

        context.view_layer.objects.active = original_active

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class A1_FS_OT_ARMATURE_SAVE_AS_SHAPEKEY(bpy.types.Operator):
    bl_idname = "a1_fs.armature_save_as_shapekey"
    bl_label = "armature_save_as_shapekey"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    use_selection: bpy.props.BoolProperty(
        default=True,
    )

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0):
            cls.poll_message_set("")
        return True

    def _check_for_existing_shapekeys(self, context, shapekey_name):
        def __get_meshes():
            for obj in context.selected_objects:
                if obj.type == "MESH":
                    yield obj
                elif obj.type == "ARMATURE":
                    for child in obj.children:
                        if child.type == "MESH":
                            yield child

        return any(
            obj.data.shape_keys and shapekey_name in obj.data.shape_keys.key_blocks
            for obj in __get_meshes()
        )

    def _process_object(self, obj, shapekey_name):
        armature_modifier = next(
            (m for m in obj.modifiers if m.type == "ARMATURE"), None
        )

        if not armature_modifier:
            return False

        remove_duplicate_shapekey(obj, shapekey_name)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply_as_shapekey(
            keep_modifier=True, modifier=armature_modifier.name
        )

        if shapekey_name:
            key_list = obj.data.shape_keys.key_blocks
            key_list[-1].name = shapekey_name

        return True

    def _process_all_objects(self, context, shapekey_name):
        target_objects = []

        if self.use_selection:
            target_objects = context.selected_objects
        else:
            for armature in context.selected_objects:
                if armature.type == "ARMATURE":
                    target_objects.extend(armature.children)

        for obj in target_objects:
            if obj.type != "MESH":
                continue

            self._process_object(obj, shapekey_name)

    def execute(self, context):
        shapekey_name = context.scene.a1_fs_armature_shapekey_name
        active_obj = context.active_object
        selected_objects = [obj for obj in context.selected_objects]

        if shapekey_name == "":
            shapekey_name = context.scene.a1_fs_armature_source.name

        if self._check_for_existing_shapekeys(context, shapekey_name):
            OverwriteWarnOperator.register_with_callback(
                lambda ctx: self._process_all_objects(ctx, shapekey_name)
            )
            bpy.ops.a1_fs.overwrite_dialogue("INVOKE_DEFAULT")
        else:
            self._process_all_objects(context, shapekey_name)

        bpy.ops.object.select_all(action="DESELECT")
        for obj in selected_objects:
            obj.select_set(True)
        context.view_layer.objects.active = active_obj

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


classes = (
    A1_FS_OT_COPY_POSE_RELATIONS,
    A1_FS_OT_COPY_POSE_TRANSFORMS,
    A1_FS_OT_CLEAR_POSE_TRANSFORMS,
    A1_FS_OT_ARMATURE_SAVE_AS_SHAPEKEY,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
