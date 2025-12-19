import bpy
from bpy.types import Panel


class FIELDREMESHER_PT_panel(Panel):
    bl_label = "Field Remesher"
    bl_idname = "FIELDREMESHER_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Field Remesher"

    def draw(self, context):
        layout = self.layout
        s = context.scene.fieldremesher_settings

        col = layout.column(align=True)
        col.prop(s, "mode")

        if s.mode == "FACES":
            col.prop(s, "target_faces")
        elif s.mode == "EDGE":
            col.prop(s, "target_edge_length")
        else:
            col.prop(s, "target_ratio")

        box = layout.box()
        box.prop(s, "use_mesh_symmetry")
        box.prop(s, "use_preserve_sharp")
        box.prop(s, "use_preserve_boundary")
        box.prop(s, "preserve_attributes")
        box.prop(s, "smooth_normals")
        box.prop(s, "seed")

        box2 = layout.box()
        box2.prop(s, "keep_original")
        box2.prop(s, "transfer_uv")
        box2.prop(s, "transfer_vcol")

        layout.operator("fieldremesher.remesh", icon="MOD_REMESH")
