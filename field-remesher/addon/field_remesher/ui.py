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
        prefs = context.preferences.addons[__package__.split(".")[0]].preferences
        obj = context.active_object

        # Seção: Presets (Onda 2)
        box_preset = layout.box()
        box_preset.label(text="Preset de Configuração", icon='PRESET')
        box_preset.prop(s, "preset_name", text="")
        
        layout.separator()

        # Seção: Densidade
        col = layout.column(align=True)
        col.label(text="Densidade do Mesh", icon='MESH_ICOSPHERE')
        col.prop(s, "mode", text="")

        # Campo condicional baseado no modo
        subcol = col.column(align=True)
        if s.mode == "FACES":
            subcol.prop(s, "target_faces")
            
            # Preview de densidade (Onda 2)
            if obj and obj.type == 'MESH':
                current_faces = len(obj.data.polygons)
                if current_faces > 0:
                    ratio = s.target_faces / current_faces
                    info_row = subcol.row()
                    info_row.scale_y = 0.7
                    info_row.alignment = 'CENTER'
                    if ratio < 0.5:
                        info_row.label(text=f"↓ Redução: {current_faces} → {s.target_faces} faces", icon='TRIA_DOWN')
                    elif ratio > 2.0:
                        info_row.label(text=f"↑ Aumento: {current_faces} → {s.target_faces} faces", icon='TRIA_UP')
                    else:
                        info_row.label(text=f"≈ Similar: {current_faces} → {s.target_faces} faces", icon='TRIA_RIGHT')
            
            # Warning para valores extremos
            if s.target_faces > 50000:
                row = subcol.row()
                row.alert = True
                row.label(text="⚠ Atenção: pode demorar!", icon='ERROR')
            
            # Validação: target > vertices do mesh (Onda 2)
            if obj and obj.type == 'MESH':
                vert_count = len(obj.data.vertices)
                if s.target_faces > vert_count * 2:
                    row = subcol.row()
                    row.alert = True
                    row.label(text=f"⚠ Alvo muito alto para {vert_count} vértices", icon='INFO')
                    
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
        
        # Density VGroup apenas se show_advanced (Onda 2)
        if prefs.show_advanced:
            box.separator(factor=0.5)
            box.prop(s, "density_vgroup", text="VGroup Densidade", icon='GROUP_VERTEX')

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
        
        # Toggle de comparação (Onda 3)
        if prefs.show_advanced:
            layout.separator(factor=0.5)
            layout.prop(s, "show_comparison", toggle=True, icon='VIEW_PERSPECTIVE')


class FIELDREMESHER_PT_presets_advanced(Panel):
    """Subpainel para gerenciamento avançado de presets (Onda 2)"""
    bl_label = "Gerenciar Presets"
    bl_idname = "FIELDREMESHER_PT_presets_advanced"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Field Remesher"
    bl_parent_id = "FIELDREMESHER_PT_panel"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        prefs = context.preferences.addons[__package__.split(".")[0]].preferences
        return prefs.show_advanced

    def draw(self, context):
        layout = self.layout
        s = context.scene.fieldremesher_settings
        
        box = layout.box()
        box.label(text="Ações de Preset", icon='PRESET')
        
        col = box.column(align=True)
        col.operator("fieldremesher.save_preset", text="Salvar Como...", icon='FILE_TICK')
        col.operator("fieldremesher.reset_defaults", text="Restaurar Padrões", icon='LOOP_BACK')
        
        layout.separator()
        
        # Info do preset atual
        info_box = layout.box()
        info_box.label(text="Preset Ativo:", icon='INFO')
        
        preset_info = {
            "CUSTOM": "Configuração manual personalizada",
            "ORGANIC": "Otimizado para formas orgânicas e personagens",
            "HARD_SURFACE": "Ideal para objetos mecânicos e arquitetura",
            "GAME_READY": "Densidade reduzida para aplicações em tempo real",
            "HIGH_DETAIL": "Máximo detalhe preservando características"
        }
        
        desc = preset_info.get(s.preset_name, "Desconhecido")
        col = info_box.column(align=True)
        col.scale_y = 0.8
        
        # Quebrar texto longo
        words = desc.split()
        line = ""
        for word in words:
            if len(line + word) < 35:
                line += word + " "
            else:
                col.label(text=line.strip())
                line = word + " "
        if line:
            col.label(text=line.strip())


class FIELDREMESHER_PT_comparison(Panel):
    """Painel de comparação lado a lado (Onda 3)"""
    bl_label = "Comparação Original vs Remesh"
    bl_idname = "FIELDREMESHER_PT_comparison"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Field Remesher"
    bl_parent_id = "FIELDREMESHER_PT_panel"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        s = context.scene.fieldremesher_settings
        prefs = context.preferences.addons[__package__.split(".")[0]].preferences
        return prefs.show_advanced and s.show_comparison

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            layout.label(text="Selecione um objeto mesh", icon='INFO')
            return
        
        # Buscar objeto remeshado (padrão: nome + "_REMESH")
        remesh_name = f"{obj.name}_REMESH"
        remesh_obj = bpy.data.objects.get(remesh_name)
        
        if not remesh_obj:
            # Tentar encontrar último criado com sufixo
            for o in bpy.data.objects:
                if o.type == 'MESH' and "_REMESH" in o.name:
                    remesh_obj = o
                    break
        
        # Grid de comparação
        box = layout.box()
        box.label(text="Estatísticas Comparativas", icon='WORKSPACE')
        
        # Headers
        split = box.split(factor=0.4)
        col_label = split.column()
        col_label.label(text="")
        split_values = split.split(factor=0.5)
        col_orig = split_values.column()
        col_orig.label(text="Original", icon='MESH_DATA')
        col_remesh = split_values.column()
        col_remesh.label(text="Remesh", icon='MOD_REMESH')
        
        box.separator(factor=0.3)
        
        # Linhas de dados
        mesh_orig = obj.data
        verts_orig = len(mesh_orig.vertices)
        faces_orig = len(mesh_orig.polygons)
        edges_orig = len(mesh_orig.edges)
        
        if remesh_obj and remesh_obj.type == 'MESH':
            mesh_remesh = remesh_obj.data
            verts_remesh = len(mesh_remesh.vertices)
            faces_remesh = len(mesh_remesh.polygons)
            edges_remesh = len(mesh_remesh.edges)
        else:
            verts_remesh = faces_remesh = edges_remesh = 0
        
        # Vértices
        self._draw_stat_row(box, "Vértices", verts_orig, verts_remesh)
        # Faces
        self._draw_stat_row(box, "Faces", faces_orig, faces_remesh)
        # Arestas
        self._draw_stat_row(box, "Arestas", edges_orig, edges_remesh)
        
        box.separator(factor=0.5)
        
        # Ações
        if remesh_obj:
            row = box.row(align=True)
            row.operator("object.select_pattern", text="Selecionar Ambos", icon='RESTRICT_SELECT_OFF').pattern = f"*{obj.name.split('_')[0]}*"
            
            row2 = box.row(align=True)
            row2.operator("fieldremesher.compare_stats", text="Estatísticas Detalhadas", icon='GRAPH')
            
            row3 = box.row(align=True)
            op = row3.operator("object.hide_view_set", text="Toggle Original", icon='HIDE_OFF')
            op.unselected = False
    
    def _draw_stat_row(self, layout, label, val_orig, val_remesh):
        """Desenha uma linha de estatística comparativa"""
        split = layout.split(factor=0.4)
        
        col_label = split.column()
        col_label.label(text=label)
        
        split_values = split.split(factor=0.5)
        
        col_orig = split_values.column()
        col_orig.alignment = 'RIGHT'
        col_orig.label(text=f"{val_orig:,}")
        
        col_remesh = split_values.column()
        col_remesh.alignment = 'RIGHT'
        if val_remesh > 0:
            # Calcular diferença percentual
            diff = ((val_remesh - val_orig) / val_orig) * 100 if val_orig > 0 else 0
            if abs(diff) < 5:
                col_remesh.label(text=f"{val_remesh:,} (≈)")
            elif diff > 0:
                col_remesh.label(text=f"{val_remesh:,} (+{diff:.0f}%)", icon='TRIA_UP')
            else:
                col_remesh.label(text=f"{val_remesh:,} ({diff:.0f}%)", icon='TRIA_DOWN')
        else:
            col_remesh.label(text="—", icon='QUESTION')


class FIELDREMESHER_PT_guides(Panel):
    """Painel secundário para Guias (Onda 3 - estrutura futura)"""
    bl_label = "Guias de Direção"
    bl_idname = "FIELDREMESHER_PT_guides"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Field Remesher"
    bl_parent_id = "FIELDREMESHER_PT_panel"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        prefs = context.preferences.addons[__package__.split(".")[0]].preferences
        # Apenas mostrar quando engine nativo estiver disponível
        from ..backend import instant_available
        return prefs.show_advanced and instant_available()

    def draw(self, context):
        layout = self.layout
        
        # Placeholder para funcionalidade futura
        box = layout.box()
        box.label(text="🚧 Em Desenvolvimento", icon='INFO')
        box.label(text="Guias de direção via curves")
        box.label(text="serão implementadas com")
        box.label(text="engine nativo (v0.4+)")
        
        layout.separator()
        
        # UI preparatória
        layout.label(text="Adicionar Guia:", icon='CURVE_DATA')
        row = layout.row(align=True)
        row.enabled = False  # Desabilitado até implementar
        row.operator("fieldremesher.add_guide", text="Da Seleção", icon='PLUS')
        row.operator("fieldremesher.clear_guides", text="Limpar", icon='X')
