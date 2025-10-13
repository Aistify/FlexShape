import bpy


def create_list_crud_operators(object_type, icon, id_prefix, list_prop, index_prop):
    ui_list_class_name = f"FLEXSHAPE_UL_{id_prefix.title()}List"

    class ObjectList(bpy.types.UIList):
        bl_idname = ui_list_class_name

        def draw_item(self, _, layout, __, item, ___, ____, _____, ______):
            if self.layout_type in {"DEFAULT", "COMPACT"}:
                obj_attr = id_prefix
                obj = getattr(item, obj_attr)
                if obj:
                    layout.prop(obj, "name", text="", emboss=False, icon=icon)
                else:
                    layout.label(text="", icon=icon)

    class AddToList(bpy.types.Operator):
        bl_idname = f"flexshape.add_{id_prefix}_to_list"
        bl_label = f"Add Selected {object_type.title()}s"
        bl_description = f"Add selected {id_prefix}s to the list"
        bl_options = {"REGISTER", "UNDO"}

        def execute(self, context):
            obj_list = getattr(context.scene, list_prop)
            obj_attr = id_prefix

            added_count = 0
            for obj in context.selected_objects:
                if obj.type != object_type:
                    continue

                if any(getattr(item, obj_attr) == obj for item in obj_list):
                    continue

                item = obj_list.add()
                setattr(item, obj_attr, obj)
                added_count += 1

            if added_count > 0:
                setattr(context.scene, index_prop, len(obj_list) - 1)
                self.report({"INFO"}, f"Added {added_count} {id_prefix}(s)")
            else:
                self.report({"WARNING"}, f"No new {id_prefix}s to add")

            return {"FINISHED"}

    class RemoveFromList(bpy.types.Operator):
        bl_idname = f"flexshape.remove_{id_prefix}_from_list"
        bl_label = f"Remove {object_type.title()}"
        bl_description = f"Remove selected {id_prefix} from the list"
        bl_options = {"REGISTER", "UNDO"}

        # noinspection PyMethodMayBeStatic
        def execute(self, context):
            obj_list = getattr(context.scene, list_prop)
            index = getattr(context.scene, index_prop)

            if 0 <= index < len(obj_list):
                obj_list.remove(index)
                setattr(context.scene, index_prop, min(index, len(obj_list) - 1))
                return {"FINISHED"}

            return {"CANCELLED"}

    class ClearList(bpy.types.Operator):
        bl_idname = f"flexshape.clear_{id_prefix}_list"
        bl_label = "Clear List"
        bl_description = f"Remove all {id_prefix}s from the list"
        bl_options = {"REGISTER", "UNDO"}

        # noinspection PyMethodMayBeStatic
        def execute(self, context):
            getattr(context.scene, list_prop).clear()
            setattr(context.scene, index_prop, 0)
            return {"FINISHED"}

    class MoveUp(bpy.types.Operator):
        bl_idname = f"flexshape.move_{id_prefix}_up"
        bl_label = "Move Up"
        bl_description = f"Move selected {id_prefix} up in the list"
        bl_options = {"REGISTER", "UNDO"}

        # noinspection PyMethodMayBeStatic
        def execute(self, context):
            obj_list = getattr(context.scene, list_prop)
            index = getattr(context.scene, index_prop)

            if index > 0:
                obj_list.move(index, index - 1)
                setattr(context.scene, index_prop, index - 1)
                return {"FINISHED"}

            return {"CANCELLED"}

    class MoveDown(bpy.types.Operator):
        bl_idname = f"flexshape.move_{id_prefix}_down"
        bl_label = "Move Down"
        bl_description = f"Move selected {id_prefix} down in the list"
        bl_options = {"REGISTER", "UNDO"}

        # noinspection PyMethodMayBeStatic
        def execute(self, context):
            obj_list = getattr(context.scene, list_prop)
            index = getattr(context.scene, index_prop)

            if index < len(obj_list) - 1:
                obj_list.move(index, index + 1)
                setattr(context.scene, index_prop, index + 1)
                return {"FINISHED"}

            return {"CANCELLED"}

    return ObjectList, AddToList, RemoveFromList, ClearList, MoveUp, MoveDown
