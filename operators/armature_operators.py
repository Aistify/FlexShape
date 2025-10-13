import bpy

from ..common.functions import (
    OverwriteWarnOperator,
    get_meshes_from_selection,
    remove_duplicate_shapekey,
)


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
        return False

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
class FLEXSHAPE_OT_ArmatureOperatorBase(bpy.types.Operator):
    bl_options = {"REGISTER", "UNDO"}

    requires_source = True

    def execute(self, context):
        source_armature = context.scene.flexshape_armature_source

        if self.requires_source and source_armature is None:
            self.report({"ERROR"}, "No Source Armature Set")
            return {"CANCELLED"}

        armature_selection = [
            obj for obj in context.selected_objects if obj.type == "ARMATURE"
        ]

        if len(armature_selection) == 0:
            self.report({"ERROR"}, "No Armatures Selected")
            return {"CANCELLED"}

        self.process_armatures(context, source_armature, armature_selection)
        return {"FINISHED"}

    def process_armatures(self, context, source_armature, target_armatures):
        raise NotImplementedError


# noinspection PyPep8Naming
class FLEXSHAPE_OT_CopyPoseRelations(FLEXSHAPE_OT_ArmatureOperatorBase):
    bl_idname = "flexshape.copy_pose_relations"
    bl_label = "Copy Pose Relations"
    bl_description = "Copy Pose Relations From Source To Selected Armatures"

    requires_source = True

    def process_armatures(self, context, source_armature, target_armatures):
        source_pose_bones = source_armature.pose.bones
        for target_armature in target_armatures:
            copy_pose_relations(target_armature, source_pose_bones)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_CopyPoseTransforms(FLEXSHAPE_OT_ArmatureOperatorBase):
    bl_idname = "flexshape.copy_pose_transforms"
    bl_label = "Copy Pose Transforms"
    bl_description = "Copy Pose Transforms From Source To Selected Armatures"

    requires_source = True

    def process_armatures(self, context, source_armature, target_armatures):
        source_pose_bones = source_armature.pose.bones
        for target_armature in target_armatures:
            copy_pose_transforms(target_armature, source_pose_bones)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_ClearPoseTransforms(FLEXSHAPE_OT_ArmatureOperatorBase):
    bl_idname = "flexshape.clear_pose_transforms"
    bl_label = "Clear Pose Transforms"
    bl_description = "Clear Pose Transforms From Selected Armatures"

    requires_source = False

    # noinspection PyMethodMayBeStatic
    def process_armatures(self, context, _, target_armatures):
        for target_armature in target_armatures:
            clear_pose_transforms(context, target_armature)


# noinspection PyPep8Naming
class FLEXSHAPE_OT_SaveArmatureDeformAsShapekey(bpy.types.Operator):
    bl_idname = "flexshape.armature_save_as_shapekey"
    bl_label = "Save Armature Deform"
    bl_description = "Save Current Armature Deform as a Shapekey"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyTypeHints
    use_selection: bpy.props.BoolProperty(
        name="Use Selection",
        description="Process only selected mesh objects?",
        default=True,
    )

    # noinspection PyMethodMayBeStatic
    def _check_for_existing_shapekeys(self, target_objects, shapekey_name):
        return any(
            obj.data.shape_keys and shapekey_name in obj.data.shape_keys.key_blocks
            for obj in target_objects
        )

    # noinspection PyMethodMayBeStatic
    def _process_all_objects(self, target_objects, shapekey_name):
        for obj in target_objects:
            save_armature_deform_as_shapekey(obj, shapekey_name)

    def execute(self, context):
        shapekey_name = context.scene.flexshape_armature_shapekey_name

        if shapekey_name == "":
            if not context.scene.flexshape_armature_source:
                self.report({"ERROR"}, "Source Armature or Shapekey name was not found")
                return {"CANCELLED"}
            shapekey_name = context.scene.flexshape_armature_source.name

        target_objects = get_meshes_from_selection(self, context)
        if target_objects is None:
            return {"CANCELLED"}

        if self._check_for_existing_shapekeys(target_objects, shapekey_name):
            OverwriteWarnOperator.register_with_callback(
                lambda ctx: self._process_all_objects(target_objects, shapekey_name)
            )
            # noinspection PyUnresolvedReferences
            bpy.ops.flexshape.overwrite_dialogue("INVOKE_DEFAULT")
        else:
            self._process_all_objects(target_objects, shapekey_name)

        return {"FINISHED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_ArmatureQuickSave(FLEXSHAPE_OT_ArmatureOperatorBase):
    bl_idname = "flexshape.armature_quick_save"
    bl_label = "Quick Save Shape Key"
    bl_description = "Copy Relations -> Copy Transforms -> Save As Shape Key -> Clear Transforms For Selected Armatures"

    requires_source = True

    # noinspection PyMethodMayBeStatic
    def process_armatures(self, context, source_armature, target_armatures):
        shapekey_name = context.scene.flexshape_armature_shapekey_name

        quick_save_armature_as_shapekey(
            context, source_armature, target_armatures, shapekey_name
        )


# noinspection PyPep8Naming
class FLEXSHAPE_OT_ArmatureMassSave(FLEXSHAPE_OT_ArmatureOperatorBase):
    bl_idname = "flexshape.armature_mass_save"
    bl_label = "Mass Save Shape Key"
    bl_description = "For Each In List: Copy Relations -> Copy Transforms -> Save As Shape Key -> Clear Transforms For Selected Armatures"

    requires_source = False

    # noinspection PyMethodMayBeStatic
    def process_armatures(self, context, _, target_armatures):
        armature_list = context.scene.flexshape_armature_list

        for armature_list_item in armature_list:
            result = quick_save_armature_as_shapekey(
                context,
                armature_list_item.armature,
                target_armatures,
                armature_list_item.armature.name,
            )

            if not result:
                self.report(
                    {"WARNING"},
                    f"Failed to save shapekey for one or more armatures sources",
                )
                print(f"Failed to save shapekey for {armature_list_item.armature.name}")


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
