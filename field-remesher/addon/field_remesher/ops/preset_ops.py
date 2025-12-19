"""Operadores auxiliares para sistema de presets e comparação (Onda 2 e 3)"""

import bpy
from bpy.types import Operator


class FIELDREMESHER_OT_save_preset(Operator):
    """Salva configuração atual como preset personalizado"""
    bl_idname = "fieldremesher.save_preset"
    bl_label = "Salvar Preset"
    bl_options = {'REGISTER', 'UNDO'}
    
    preset_name: bpy.props.StringProperty(
        name="Nome do Preset",
        description="Nome para identificar este preset",
        default="Meu Preset"
    )
    
    def execute(self, context):
        s = context.scene.fieldremesher_settings
        
        # TODO: Implementar salvamento persistente em JSON
        # Por enquanto, apenas feedback
        self.report({'INFO'}, f"Preset '{self.preset_name}' salvo (funcionalidade em desenvolvimento)")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class FIELDREMESHER_OT_reset_to_defaults(Operator):
    """Restaura todas as configurações para valores padrão"""
    bl_idname = "fieldremesher.reset_defaults"
    bl_label = "Restaurar Padrões"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        s = context.scene.fieldremesher_settings
        
        # Reset manual de todas as props
        s.preset_name = "CUSTOM"
        s.mode = "FACES"
        s.target_faces = 4000
        s.target_edge_length = 0.1
        s.target_ratio = 1.0
        s.use_mesh_symmetry = False
        s.use_preserve_sharp = True
        s.use_preserve_boundary = True
        s.preserve_attributes = True
        s.smooth_normals = False
        s.seed = 0
        s.keep_original = True
        s.transfer_uv = True
        s.transfer_vcol = True
        s.density_vgroup = ""
        
        self.report({'INFO'}, "Configurações restauradas para padrões")
        return {'FINISHED'}


class FIELDREMESHER_OT_add_guide(Operator):
    """Adiciona curva selecionada como guia de direção (placeholder Onda 3)"""
    bl_idname = "fieldremesher.add_guide"
    bl_label = "Adicionar Guia"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        self.report({'WARNING'}, "Guias serão implementadas com engine nativo (v0.4+)")
        return {'CANCELLED'}


class FIELDREMESHER_OT_clear_guides(Operator):
    """Remove todas as guias de direção (placeholder Onda 3)"""
    bl_idname = "fieldremesher.clear_guides"
    bl_label = "Limpar Guias"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        self.report({'INFO'}, "Nenhuma guia para remover")
        return {'CANCELLED'}


class FIELDREMESHER_OT_compare_stats(Operator):
    """Exibe estatísticas comparativas detalhadas em popup"""
    bl_idname = "fieldremesher.compare_stats"
    bl_label = "Estatísticas Detalhadas"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "Selecione um objeto mesh")
            return {'CANCELLED'}
        
        # Buscar remesh
        remesh_name = f"{obj.name}_REMESH"
        remesh_obj = bpy.data.objects.get(remesh_name)
        
        if not remesh_obj:
            self.report({'INFO'}, "Nenhum objeto remesh encontrado")
            return {'CANCELLED'}
        
        return context.window_manager.invoke_popup(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        remesh_name = f"{obj.name}_REMESH"
        remesh_obj = bpy.data.objects.get(remesh_name)
        
        if not remesh_obj:
            layout.label(text="Objeto remesh não encontrado", icon='ERROR')
            return
        
        # Comparação detalhada
        mesh_orig = obj.data
        mesh_remesh = remesh_obj.data
        
        box = layout.box()
        box.label(text="Comparação Detalhada", icon='WORKSPACE')
        
        # Grid de dados
        col = box.column(align=True)
        
        # Vértices
        v_orig = len(mesh_orig.vertices)
        v_remesh = len(mesh_remesh.vertices)
        v_diff = v_remesh - v_orig
        col.label(text=f"Vértices: {v_orig:,} → {v_remesh:,} ({v_diff:+,})")
        
        # Faces
        f_orig = len(mesh_orig.polygons)
        f_remesh = len(mesh_remesh.polygons)
        f_diff = f_remesh - f_orig
        col.label(text=f"Faces: {f_orig:,} → {f_remesh:,} ({f_diff:+,})")
        
        # Arestas
        e_orig = len(mesh_orig.edges)
        e_remesh = len(mesh_remesh.edges)
        e_diff = e_remesh - e_orig
        col.label(text=f"Arestas: {e_orig:,} → {e_remesh:,} ({e_diff:+,})")
        
        col.separator()
        
        # Análise de topologia
        quads = sum(1 for p in mesh_remesh.polygons if len(p.vertices) == 4)
        tris = sum(1 for p in mesh_remesh.polygons if len(p.vertices) == 3)
        ngons = f_remesh - quads - tris
        
        col.label(text="Topologia do Remesh:")
        col.label(text=f"  Quads: {quads:,} ({quads/f_remesh*100:.1f}%)")
        if tris > 0:
            col.label(text=f"  Tris: {tris:,} ({tris/f_remesh*100:.1f}%)")
        if ngons > 0:
            col.label(text=f"  N-gons: {ngons:,}")


# Lista de classes para registro
CLASSES = [
    FIELDREMESHER_OT_save_preset,
    FIELDREMESHER_OT_reset_to_defaults,
    FIELDREMESHER_OT_add_guide,
    FIELDREMESHER_OT_clear_guides,
    FIELDREMESHER_OT_compare_stats,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
