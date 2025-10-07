import bpy

from ..common.functions import OverwriteWarnOperator
from ..common.functions import remove_duplicate_shapekey
from ..common.functions import show_message_box


def copy_pose_relations(armature, source_pose_bones):
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


def copy_pose_transforms(armature, source_pose_bones):
    target_pose_bones = armature.pose.bones

    for source_bone in source_pose_bones:
        if source_bone.name in target_pose_bones:
            target_bone = target_pose_bones[source_bone.name]
            target_bone.matrix_basis = source_bone.matrix_basis.copy()


def clear_pose_transforms(context, target_armature):
    context.view_layer.objects.active = target_armature
    bpy.ops.object.mode_set(mode="POSE")
    bpy.ops.pose.select_all(action="SELECT")
    bpy.ops.pose.transforms_clear()
    bpy.ops.object.mode_set(mode="OBJECT")


def save_armature_deform_as_shapekey(obj, shapekey_name):
    armature_modifier = next(
        (modifier for modifier in obj.modifiers if modifier.type == "ARMATURE"), None
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


def quick_save_armature_as_shapekey(
    context, source_armature, target_armatures, shapekey_name=""
):
    if source_armature is None:
        show_message_box("Source Armature was not found.")
        return {"CANCELLED"}

    if shapekey_name == "":
        shapekey_name = source_armature.name

    source_pose_bones = source_armature.pose.bones

    for target_armature in target_armatures:
        if target_armature == source_armature:
            continue

        copy_pose_relations(target_armature, source_pose_bones)
        copy_pose_transforms(target_armature, source_pose_bones)
        target_objects = [
            child for child in target_armature.children if child.type == "MESH"
        ]
        for obj in target_objects:
            save_armature_deform_as_shapekey(obj, shapekey_name)
        clear_pose_transforms(context, target_armature)

    return True


# noinspection PyPep8Naming
class FLEXSHAPE_OT_CopyPoseRelations(bpy.types.Operator):
    bl_idname = "flexshape.copy_pose_relations"
    bl_label = "Copy Pose Relations"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, _):
        source_armature = bpy.context.scene.flexshape_armature_source

        if source_armature is None:
            show_message_box("Source Armature was not found.")
            return {"CANCELLED"}

        source_pose_bones = source_armature.pose.bones

        for target_armature in bpy.context.selected_objects:
            if target_armature.type != "ARMATURE":
                continue
            if target_armature == source_armature:
                continue

            copy_pose_relations(target_armature, source_pose_bones)

        return {"FINISHED"}

    def invoke(self, context, _):
        return self.execute(context)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_CopyPoseTransforms(bpy.types.Operator):
    bl_idname = "flexshape.copy_pose_transforms"
    bl_label = "Copy Pose Transforms"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        source_armature = context.scene.flexshape_armature_source

        if source_armature is None:
            show_message_box("Source Armature was not found.")
            return {"CANCELLED"}

        source_pose_bones = source_armature.pose.bones

        for target_armature in bpy.context.selected_objects:
            if target_armature.type != "ARMATURE":
                continue
            if target_armature == source_armature:
                continue

            copy_pose_transforms(target_armature, source_pose_bones)

        return {"FINISHED"}

    def invoke(self, context, _):
        return self.execute(context)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_ClearPoseTransforms(bpy.types.Operator):
    bl_idname = "flexshape.clear_pose_transforms"
    bl_label = "Clear Pose Transforms"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        original_active = context.active_object

        for target_armature in bpy.context.selected_objects:
            if target_armature.type != "ARMATURE":
                continue

            clear_pose_transforms(context, target_armature)

        context.view_layer.objects.active = original_active

        return {"FINISHED"}

    def invoke(self, context, _):
        return self.execute(context)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_SaveArmatureDeformAsShapekey(bpy.types.Operator):
    bl_idname = "flexshape.armature_save_as_shapekey"
    bl_label = "Save Armature Deform as Shapekey"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyTypeHints
    use_selection: bpy.props.BoolProperty(
        default=True,
    )

    # noinspection PyMethodMayBeStatic
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

            save_armature_deform_as_shapekey(obj, shapekey_name)

    def execute(self, context):
        shapekey_name = context.scene.flexshape_armature_shapekey_name
        active_obj = context.active_object
        selected_objects = [obj for obj in context.selected_objects]

        if shapekey_name == "":
            shapekey_name = context.scene.flexshape_armature_source.name

        if self._check_for_existing_shapekeys(context, shapekey_name):
            OverwriteWarnOperator.register_with_callback(
                lambda ctx: self._process_all_objects(ctx, shapekey_name)
            )
            # noinspection PyUnresolvedReferences
            bpy.ops.flexshape.overwrite_dialogue("INVOKE_DEFAULT")
        else:
            self._process_all_objects(context, shapekey_name)

        bpy.ops.object.select_all(action="DESELECT")
        for obj in selected_objects:
            obj.select_set(True)
        context.view_layer.objects.active = active_obj

        return {"FINISHED"}

    def invoke(self, context, _):
        return self.execute(context)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_ArmatureQuickSave(bpy.types.Operator):
    bl_idname = "flexshape.armature_quick_save"
    bl_label = "Quick Save Shape Key"
    bl_description = (
        "Copy Relations -> Copy Transforms -> Save As Shape Key -> Clear Transforms"
    )
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        active_obj = context.active_object
        selected_objects = [
            obj for obj in context.selected_objects if obj.type == "ARMATURE"
        ]

        shapekey_name = context.scene.flexshape_armature_shapekey_name
        source_armature = bpy.context.scene.flexshape_armature_source

        quick_save_armature_as_shapekey(
            context, source_armature, selected_objects, shapekey_name
        )

        for obj in selected_objects:
            obj.select_set(True)
        context.view_layer.objects.active = active_obj

        return {"FINISHED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_ArmatureMassSave(bpy.types.Operator):
    bl_idname = "flexshape.armature_mass_save"
    bl_label = "Mass Save Shape Key"
    bl_description = "For Each In List: Copy Relations -> Copy Transforms -> Save As Shape Key -> Clear Transforms"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        active_obj = context.active_object
        selected_objects = [
            obj for obj in context.selected_objects if obj.type == "ARMATURE"
        ]

        armature_list = context.scene.flexshape_armature_list

        for armature_list_item in armature_list:
            quick_save_armature_as_shapekey(
                context,
                armature_list_item.armature,
                selected_objects,
                armature_list_item.armature.name,
            )

        for obj in selected_objects:
            obj.select_set(True)
        context.view_layer.objects.active = active_obj

        return {"FINISHED"}


classes = (
    FLEXSHAPE_OT_CopyPoseRelations,
    FLEXSHAPE_OT_CopyPoseTransforms,
    FLEXSHAPE_OT_ClearPoseTransforms,
    FLEXSHAPE_OT_SaveArmatureDeformAsShapekey,
    FLEXSHAPE_OT_ArmatureQuickSave,
    FLEXSHAPE_OT_ArmatureMassSave,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
