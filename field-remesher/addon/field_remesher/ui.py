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

        # Seção: Densidade
        col = layout.column(align=True)
        col.label(text="Densidade do Mesh", icon='MESH_ICOSPHERE')
        col.prop(s, "mode", text="")

        # Campo condicional baseado no modo
        subcol = col.column(align=True)
        if s.mode == "FACES":
            subcol.prop(s, "target_faces")
            # Warning para valores extremos
            if s.target_faces > 50000:
                row = subcol.row()
                row.alert = True
                row.label(text="⚠ Atenção: pode demorar!", icon='ERROR')
        elif s.mode == "EDGE":
            subcol.prop(s, "target_edge_length")
        else:
            subcol.prop(s, "target_ratio")

        layout.separator()

        # Seção: Opções de Preservação
        box = layout.box()
        box.label(text="Opções de Preservação", icon='MOD_EDGESPLIT')
        box.prop(s, "use_mesh_symmetry")
        box.prop(s, "use_preserve_sharp")
        box.prop(s, "use_preserve_boundary")
        box.separator(factor=0.5)
        box.prop(s, "preserve_attributes")
        box.prop(s, "smooth_normals")
        
        # Seed em subrow com menor destaque
        row = box.row()
        row.scale_y = 0.8
        row.prop(s, "seed")

        layout.separator()

        # Seção: Pós-processamento
        box2 = layout.box()
        box2.label(text="Pós-processamento", icon='MODIFIER')
        box2.prop(s, "keep_original")
        
        # Subitens de transferência (com indent visual)
        col2 = box2.column(align=True)
        col2.active = s.preserve_attributes  # Desabilita se preserve_attributes=False
        col2.prop(s, "transfer_uv")
        col2.prop(s, "transfer_vcol")

        layout.separator()

        # Botão de ação (maior e destacado)
        row = layout.row()
        row.scale_y = 1.5
        row.operator("fieldremesher.remesh", icon='MOD_REMESH', text="Executar Remesh")
