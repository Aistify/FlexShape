import bpy


# noinspection PyPep8Naming
class FLEXSHAPE_UL_LatticeList(bpy.types.UIList):
    def draw_item(self, _, layout, __, item, ___, ____, _____):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            if item.lattice:
                layout.prop(
                    item.lattice, "name", text="", emboss=False, icon="LATTICE_DATA"
                )
            else:
                layout.label(text="", icon="LATTICE_DATA")
        elif self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text="", icon="LATTICE_DATA")


# noinspection PyPep8Naming
class FLEXSHAPE_OT_AddLatticeToList(bpy.types.Operator):
    bl_idname = "flexshape.add_lattice_to_list"
    bl_label = "Add Selected Lattices"
    bl_description = "Add selected lattices to the list"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        lattice_list = context.scene.flexshape_lattice_list

        added_count = 0
        for obj in context.selected_objects:
            if obj.type != "LATTICE":
                continue

            # Check if already in list
            if any(item.lattice == obj for item in lattice_list):
                continue

            item = lattice_list.add()
            item.lattice = obj
            added_count += 1

        if added_count > 0:
            context.scene.flexshape_lattice_list_index = len(lattice_list) - 1
            self.report({"INFO"}, f"Added {added_count} lattice(s)")
        else:
            self.report({"WARNING"}, "No new lattices to add")

        return {"FINISHED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_RemoveLatticeFromList(bpy.types.Operator):
    bl_idname = "flexshape.remove_lattice_from_list"
    bl_label = "Remove Lattice"
    bl_description = "Remove selected lattice from the list"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        lattice_list = context.scene.flexshape_lattice_list
        index = context.scene.flexshape_lattice_list_index

        if 0 <= index < len(lattice_list):
            lattice_list.remove(index)
            context.scene.flexshape_lattice_list_index = min(
                index, len(lattice_list) - 1
            )
            return {"FINISHED"}

        return {"CANCELLED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_ClearLatticeList(bpy.types.Operator):
    bl_idname = "flexshape.clear_lattice_list"
    bl_label = "Clear List"
    bl_description = "Remove all lattices from the list"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        context.scene.flexshape_lattice_list.clear()
        context.scene.flexshape_lattice_list_index = 0
        return {"FINISHED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_MoveLatticeUp(bpy.types.Operator):
    bl_idname = "flexshape.move_lattice_up"
    bl_label = "Move Up"
    bl_description = "Move selected lattice up in the list"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        lattice_list = context.scene.flexshape_lattice_list
        index = context.scene.flexshape_lattice_list_index

        if index > 0:
            lattice_list.move(index, index - 1)
            context.scene.flexshape_lattice_list_index = index - 1
            return {"FINISHED"}

        return {"CANCELLED"}


# noinspection PyPep8Naming
class FLEXSHAPE_OT_MoveLatticeDown(bpy.types.Operator):
    bl_idname = "flexshape.move_lattice_down"
    bl_label = "Move Down"
    bl_description = "Move selected lattice down in the list"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        lattice_list = context.scene.flexshape_lattice_list
        index = context.scene.flexshape_lattice_list_index

        if index < len(lattice_list) - 1:
            lattice_list.move(index, index + 1)
            context.scene.flexshape_lattice_list_index = index + 1
            return {"FINISHED"}

        return {"CANCELLED"}


classes = (
    FLEXSHAPE_UL_LatticeList,
    FLEXSHAPE_OT_AddLatticeToList,
    FLEXSHAPE_OT_RemoveLatticeFromList,
    FLEXSHAPE_OT_ClearLatticeList,
    FLEXSHAPE_OT_MoveLatticeUp,
    FLEXSHAPE_OT_MoveLatticeDown,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
