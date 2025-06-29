import bpy
import json
from typing import List, Dict


def show_message_box(message="", title="Message Box", icon="INFO"):
    # noinspection PyUnusedLocal
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


class BlendShape:
    def __init__(self, blendName: str, blendIndex: int, blendValue: float):
        self.blendName = blendName
        self.blendIndex = blendIndex
        self.blendValue = blendValue


class BlendCategory:
    def __init__(self, blendshapes: List[BlendShape] = None):
        self.blendshapes = blendshapes or []


def read_blendshape_data_json(json_file) -> Dict[str, BlendCategory]:
    with open(json_file, "r", encoding="utf-8") as file:
        blendshape_data = json.load(file)

    categories: Dict[str, BlendCategory] = {}

    for blend_shape in blendshape_data["blendShapeDataList"]:
        blend_shape_data = BlendShape(
            blendName=blend_shape["blendName"],
            blendIndex=blend_shape["blendIndex"],
            blendValue=blend_shape["blendValue"],
        )

        identifier = blend_shape_data.blendName.split("_")[0]

        if identifier not in categories:
            categories[identifier] = BlendCategory()
        categories[identifier].blendshapes.append(blend_shape_data)

    # Debug
    # for identifier, category in categories.items():
    #     if len(category.blendshapes) > 1:
    #         print(f"Category: {identifier}")
    #         # for blendshape in category.blendshapes:
    #         #     print(f"  {blendshape}")

    return categories


def remove_duplicate_shapekey(obj, shapekey_name):
    if obj.data.shape_keys is not None:
        key_blocks = obj.data.shape_keys.key_blocks
        if shapekey_name in key_blocks:
            idx = key_blocks.find(shapekey_name)
            bpy.context.view_layer.objects.active = obj
            obj.active_shape_key_index = idx
            bpy.ops.object.shape_key_remove(all=False)


# noinspection PyUnusedLocal
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
            bpy.utils.unregister_class(self.__class__)
            return {"FINISHED"}

        bpy.utils.unregister_class(self.__class__)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Shapekeys will be overwritten. Continue?")
        layout.prop(self, "choice", expand=True)

    def cancel(self, context):
        bpy.utils.unregister_class(self.__class__)
