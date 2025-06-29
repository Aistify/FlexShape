import bpy
from ..common.functions import show_message_box


class OverwriteWarnOperator(bpy.types.Operator):
    bl_idname = "a1_fs.overwrite_dialogue"
    bl_label = "Overwrite Confirmation"
    bl_options = {"INTERNAL"}

    choice: bpy.props.EnumProperty(
        items=[("YES", "Yes", "Overwrite"), ("NO", "No", "Skip")], default="NO"
    )

    callback_fn = None

    @classmethod
    def register_with_callback(cls, callback):
        cls.callback_fn = staticmethod(callback)
        bpy.utils.register_class(cls)

    def execute(self, context):
        if self.choice == "YES" and self.callback_fn:
            self.callback_fn(context)
        else:
            print("User clicked 'No'")

        bpy.utils.unregister_class(self.__class__)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Shapekeys will be overwritten. Continue?")
        layout.prop(self, "choice", expand=True)

    def cancel(self, context):
        print("Dialog cancelled")
        bpy.utils.unregister_class(self.__class__)


class A1_FS_OT_ADD_LATTICE(bpy.types.Operator):
    bl_idname = "a1_fs.add_lattice"
    bl_label = "add_lattice"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def _check_for_duplicates(self, context):
        return any(
            obj.type == "MESH"
            and any(
                mod.type == "LATTICE" and mod.name == "A1ST_LATTICE"
                for mod in obj.modifiers
            )
            for obj in context.selected_objects
        )

    def _remove_duplicate_lattice(self, obj):
        if obj.modifiers is not None:
            for modifier in obj.modifiers:
                if modifier.type == "LATTICE" and modifier.name == "A1ST_LATTICE":
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_remove(modifier=modifier.name)

    def _process_object(self, obj, source_lattice):
        lattice = obj.modifiers.new("A1ST_LATTICE", "LATTICE")
        lattice.object = source_lattice
        return True

    def _process_all_objects(self, context, source_lattice):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            self._remove_duplicate_lattice(obj)
            self._process_object(obj, source_lattice)

    def execute(self, context):
        source_lattice = context.scene.a1_fs_lattice_source

        if source_lattice is None:
            show_message_box("Source Lattice was not found.")
            return {"CANCELLED"}

        if self._check_for_duplicates(context):
            OverwriteWarnOperator.register_with_callback(
                lambda ctx: self._process_all_objects(ctx, source_lattice)
            )
            bpy.ops.a1_fs.overwrite_dialogue("INVOKE_DEFAULT")
        else:
            self._process_all_objects(context, source_lattice)

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class A1_FS_OT_REMOVE_LATTICE(bpy.types.Operator):
    bl_idname = "a1_fs.remove_lattice"
    bl_label = "remove_lattice"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def _process_object(self, obj):
        if obj.modifiers is not None:
            for modifier in obj.modifiers:
                if modifier.type == "LATTICE" and modifier.name == "A1ST_LATTICE":
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_remove(modifier=modifier.name)
        return True

    def _process_all_objects(self, context):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            self._process_object(obj)

    def execute(self, context):
        self._process_all_objects(context)

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class A1_FS_OT_LATTICE_SAVE_AS_SHAPEKEY(bpy.types.Operator):
    bl_idname = "a1_fs.lattice_save_as_shapekey"
    bl_label = "lattice_save_as_shapekey"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def _check_for_existing_shapekeys(self, context, shapekey_name):
        return any(
            obj.type == "MESH"
            and obj.data.shape_keys
            and shapekey_name in obj.data.shape_keys.key_blocks
            for obj in context.selected_objects
        )

    def _remove_duplicate_shapekey(self, obj, shapekey_name):
        if obj.data.shape_keys is not None:
            key_blocks = obj.data.shape_keys.key_blocks
            if shapekey_name in key_blocks:
                idx = key_blocks.find(shapekey_name)
                bpy.context.view_layer.objects.active = obj
                obj.active_shape_key_index = idx
                bpy.ops.object.shape_key_remove(all=False)

    def _process_object(self, obj, shapekey_name, remove_lattice):
        if obj.modifiers is not None:
            for modifier in obj.modifiers:
                if modifier.type == "LATTICE" and modifier.name == "A1ST_LATTICE":
                    self._remove_duplicate_shapekey(obj, shapekey_name)
                    modifier.name = shapekey_name
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_apply_as_shapekey(
                        modifier=modifier.name, keep_modifier=not remove_lattice
                    )
                    if not remove_lattice:
                        modifier.name = "A1ST_LATTICE"

        return True

    def _process_all_objects(self, context, shapekey_name, remove_lattice):
        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue

            self._process_object(obj, shapekey_name, remove_lattice)

    def execute(self, context):
        shapekey_name = context.scene.a1_fs_lattice_shapekey_name
        remove_lattice = context.scene.a1_fs_lattice_auto_remove

        if shapekey_name == "":
            shapekey_name = context.scene.a1_fs_lattice_source.name

        if self._check_for_existing_shapekeys(context, shapekey_name):
            OverwriteWarnOperator.register_with_callback(
                lambda ctx: self._process_all_objects(
                    ctx, shapekey_name, remove_lattice
                )
            )
            bpy.ops.a1_fs.overwrite_dialogue("INVOKE_DEFAULT")
        else:
            self._process_all_objects(context, shapekey_name, remove_lattice)

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


classes = (
    A1_FS_OT_ADD_LATTICE,
    A1_FS_OT_REMOVE_LATTICE,
    A1_FS_OT_LATTICE_SAVE_AS_SHAPEKEY,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
