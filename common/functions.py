import bpy


def show_message_box(message="", title="Message Box", icon="INFO"):
    def draw(self, _):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def remove_duplicate_shapekey(obj, shapekey_name):
    if obj.data.shape_keys is not None:
        key_blocks = obj.data.shape_keys.key_blocks
        if shapekey_name in key_blocks:
            idx = key_blocks.find(shapekey_name)
            bpy.context.view_layer.objects.active = obj
            obj.active_shape_key_index = idx
            bpy.ops.object.shape_key_remove(all=False)


class OverwriteWarnOperator(bpy.types.Operator):
    bl_idname = "flexshape.overwrite_dialogue"
    bl_label = "Overwrite Confirmation"
    bl_options = {"INTERNAL"}

    # noinspection PyTypeHints
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
            bpy.utils.unregister_class(self.__class__)
            return {"FINISHED"}

        bpy.utils.unregister_class(self.__class__)
        return {"FINISHED"}

    def invoke(self, context, _):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, _):
        layout = self.layout
        layout.label(text="Shapekeys will be overwritten. Continue?")
        layout.prop(self, "choice", expand=True)

    def cancel(self, _):
        bpy.utils.unregister_class(self.__class__)
