import bpy


# noinspection PyPep8Naming
class FLEXSHAPE_UL_ArmatureList(bpy.types.UIList):
    def draw_item(self, _, layout, __, item, ___, ____, _____):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            if item.armature:
                layout.prop(
                    item.armature, "name", text="", emboss=False, icon="ARMATURE_DATA"
                )
            else:
                layout.label(text="", icon="ARMATURE_DATA")
        elif self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text="", icon="ARMATURE_DATA")


# noinspection PyPep8Naming
class FLEXSHAPE_OT_AddArmatureToList(bpy.types.Operator):
    bl_idname = "flexshape.add_armature_to_list"
    bl_label = "Add Selected Armatures"
    bl_description = "Add selected armatures to the list"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        armature_list = context.scene.flexshape_armature_list

        added_count = 0
        for obj in context.selected_objects:
            if obj.type != "ARMATURE":
                continue

            # Check if already in list
            if any(item.armature == obj for item in armature_list):
                continue

            item = armature_list.add()
            item.armature = obj
            added_count += 1

        if added_count > 0:
            context.scene.flexshape_armature_list_index = len(armature_list) - 1
            self.report({"INFO"}, f"Added {added_count} armature(s)")
        else:
            self.report({"WARNING"}, "No new armatures to add")

        return {"FINISHED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_RemoveArmatureFromList(bpy.types.Operator):
    bl_idname = "flexshape.remove_armature_from_list"
    bl_label = "Remove Armature"
    bl_description = "Remove selected armature from the list"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        armature_list = context.scene.flexshape_armature_list
        index = context.scene.flexshape_armature_list_index

        if 0 <= index < len(armature_list):
            armature_list.remove(index)
            context.scene.flexshape_armature_list_index = min(
                index, len(armature_list) - 1
            )
            return {"FINISHED"}

        return {"CANCELLED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_ClearArmatureList(bpy.types.Operator):
    bl_idname = "flexshape.clear_armature_list"
    bl_label = "Clear List"
    bl_description = "Remove all armatures from the list"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        context.scene.flexshape_armature_list.clear()
        context.scene.flexshape_armature_list_index = 0
        return {"FINISHED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_MoveArmatureUp(bpy.types.Operator):
    bl_idname = "flexshape.move_armature_up"
    bl_label = "Move Up"
    bl_description = "Move selected armature up in the list"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        armature_list = context.scene.flexshape_armature_list
        index = context.scene.flexshape_armature_list_index

        if index > 0:
            armature_list.move(index, index - 1)
            context.scene.flexshape_armature_list_index = index - 1
            return {"FINISHED"}

        return {"CANCELLED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_MoveArmatureDown(bpy.types.Operator):
    bl_idname = "flexshape.move_armature_down"
    bl_label = "Move Down"
    bl_description = "Move selected armature down in the list"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        armature_list = context.scene.flexshape_armature_list
        index = context.scene.flexshape_armature_list_index

        if index < len(armature_list) - 1:
            armature_list.move(index, index + 1)
            context.scene.flexshape_armature_list_index = index + 1
            return {"FINISHED"}

        return {"CANCELLED"}


classes = (
    FLEXSHAPE_UL_ArmatureList,
    FLEXSHAPE_OT_AddArmatureToList,
    FLEXSHAPE_OT_RemoveArmatureFromList,
    FLEXSHAPE_OT_ClearArmatureList,
    FLEXSHAPE_OT_MoveArmatureUp,
    FLEXSHAPE_OT_MoveArmatureDown,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
