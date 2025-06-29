import bpy
from .armature_panel import A1_FS_PT_ARMATURE_PANEL
from .lattice_panel import A1_FS_PT_LATTICE_PANEL
from .surface_deform_panel import A1_FS_PT_SURFACE_DEFORM_PANEL
from .utils_panel import A1_FS_PT_UTILS_PANEL
from .blendshape_utils_panel import A1_FS_PT_BLENDSHAPE_UTILS_PANEL


class A1_FS_PT_MAIN_PANEL(bpy.types.Panel):
    bl_label = "FlexShape"
    bl_idname = "A1_FS_PT_MAIN_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FlexShape"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout

        layout.prop(
            context.scene,
            "a1_fs_armature_show_panel",
            text="Armature",
            icon_value=(5 if bpy.context.scene.a1_fs_armature_show_panel else 4),
            emboss=True,
        )

        if bpy.context.scene.a1_fs_armature_show_panel:
            A1_FS_PT_ARMATURE_PANEL.draw(self, context)

        layout.prop(
            context.scene,
            "a1_fs_lattice_show_panel",
            text="Lattice",
            icon_value=(5 if bpy.context.scene.a1_fs_lattice_show_panel else 4),
            emboss=True,
        )

        if bpy.context.scene.a1_fs_lattice_show_panel:
            A1_FS_PT_LATTICE_PANEL.draw(self, context)

        layout.prop(
            context.scene,
            "a1_fs_surface_deform_show_panel",
            text="Surface Deform",
            icon_value=(5 if bpy.context.scene.a1_fs_surface_deform_show_panel else 4),
            emboss=True,
        )

        if bpy.context.scene.a1_fs_surface_deform_show_panel:
            A1_FS_PT_SURFACE_DEFORM_PANEL.draw(self, context)

        layout.prop(
            context.scene,
            "a1_fs_utils_show_panel",
            text="Utils",
            icon_value=(5 if bpy.context.scene.a1_fs_utils_show_panel else 4),
            emboss=True,
        )

        if bpy.context.scene.a1_fs_utils_show_panel:
            A1_FS_PT_UTILS_PANEL.draw(self, context)

        # utils_dropdown_box = layout.box()
        # utils_dropdown_box.prop(
        #     context.scene,
        #     "a1_fs_utils_show_panel",
        #     text="Placeholder",
        #     icon_value=(5 if bpy.context.scene.a1_fs_utils_show_panel else 4),
        #     emboss=True,
        # )
        # A1_FS_PT_BLENDSHAPE_UTILS_PANEL.draw(self, context)
