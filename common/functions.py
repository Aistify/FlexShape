import bpy
import json
from typing import List, Dict


def show_message_box(message="", title="Message Box", icon="INFO"):
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


# Example usage
# read_blendshape_data_json("test.json")
