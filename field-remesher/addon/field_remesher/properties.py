import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    PointerProperty,
    EnumProperty,
    IntProperty,
    FloatProperty,
    BoolProperty,
    StringProperty,
)


def update_preset(self, context):
    """Callback quando preset é alterado"""
    preset = self.preset_name
    
    if preset == "ORGANIC":
        self.mode = "FACES"
        self.target_faces = 5000
        self.use_mesh_symmetry = False
        self.use_preserve_sharp = False
        self.use_preserve_boundary = True
        self.preserve_attributes = True
        self.smooth_normals = True
    elif preset == "HARD_SURFACE":
        self.mode = "FACES"
        self.target_faces = 8000
        self.use_mesh_symmetry = True
        self.use_preserve_sharp = True
        self.use_preserve_boundary = True
        self.preserve_attributes = True
        self.smooth_normals = False
    elif preset == "GAME_READY":
        self.mode = "FACES"
        self.target_faces = 2000
        self.use_mesh_symmetry = False
        self.use_preserve_sharp = False
        self.use_preserve_boundary = True
        self.preserve_attributes = True
        self.smooth_normals = True
    elif preset == "HIGH_DETAIL":
        self.mode = "EDGE"
        self.target_edge_length = 0.05
        self.use_mesh_symmetry = False
        self.use_preserve_sharp = True
        self.use_preserve_boundary = True
        self.preserve_attributes = True
        self.smooth_normals = True
    # CUSTOM não muda nada


class FieldRemesherSettings(PropertyGroup):
    preset_name: EnumProperty(
        name="Preset",
        description="Configurações pré-definidas para casos comuns",
        items=[
            ("CUSTOM", "Personalizado", "Configuração manual", 'PREFERENCES', 0),
            ("ORGANIC", "Orgânico", "Otimizado para personagens e formas suaves", 'SURFACE_NSURFACE', 1),
            ("HARD_SURFACE", "Hard Surface", "Otimizado para objetos mecânicos e arquitetura", 'MESH_CUBE', 2),
            ("GAME_READY", "Game-Ready", "Baixa densidade para jogos e tempo real", 'GAME', 3),
            ("HIGH_DETAIL", "Alta Definição", "Máximo detalhe preservando features", 'MESH_ICOSPHERE', 4),
        ],
        default="CUSTOM",
        update=update_preset
    )
    mode: EnumProperty(
        name="Modo",
        description="Define como a densidade do mesh será controlada",
        items=[
            ("FACES", "Faces", "Número alvo de faces (quads)"),
            ("EDGE", "Comprimento de Aresta", "Comprimento médio alvo das arestas"),
            ("RATIO", "Proporção", "Razão relativa ao número de faces atual"),
        ],
        default="FACES",
    )

    target_faces: IntProperty(
        name="Faces Alvo",
        description="Número aproximado de faces quads no resultado (valores altos podem demorar)",
        default=4000,
        min=1,
        soft_max=50000
    )
    
    target_edge_length: FloatProperty(
        name="Comprimento de Aresta",
        description="Tamanho médio das arestas em unidades Blender",
        default=0.1,
        min=1e-7,
        soft_min=0.001,
        soft_max=1.0,
        precision=4
    )
    
    target_ratio: FloatProperty(
        name="Proporção",
        description="Fator multiplicador de faces (1.0 = mesmo número, 0.5 = metade)",
        default=1.0,
        min=0.01,
        soft_max=2.0,
        precision=2
    )

    use_mesh_symmetry: BoolProperty(
        name="Simetria",
        description="Preserva simetria no eixo X (requer que o mesh já seja simétrico)",
        default=False
    )
    
    use_preserve_sharp: BoolProperty(
        name="Preservar Sharp",
        description="Mantém arestas marcadas como 'sharp' no resultado",
        default=True
    )
    
    use_preserve_boundary: BoolProperty(
        name="Preservar Contorno",
        description="Mantém o contorno externo do mesh sem alterações",
        default=True
    )

    preserve_attributes: BoolProperty(
        name="Preservar Atributos",
        description="Transfere materiais, UVs e cores para o novo mesh (via Data Transfer)",
        default=True
    )
    
    smooth_normals: BoolProperty(
        name="Suavizar Normais",
        description="Aplica sombreamento suave (Shade Smooth) ao resultado",
        default=False
    )
    
    seed: IntProperty(
        name="Semente Aleatória",
        description="Seed de aleatoriedade (0 = não determinístico, >0 = reproduzível)",
        default=0,
        min=0,
        soft_max=9999
    )

    keep_original: BoolProperty(
        name="Manter Original",
        description="Mantém o mesh original oculto (não-destrutivo)",
        default=True
    )
    
    transfer_uv: BoolProperty(
        name="Transferir UV",
        description="Transfere coordenadas UV do original (requer 'Preservar Atributos')",
        default=True
    )
    
    transfer_vcol: BoolProperty(
        name="Transferir Cores",
        description="Transfere Color Attributes do original (requer 'Preservar Atributos')",
        default=True
    )

    density_vgroup: StringProperty(
        name="Grupo de Vértices (Densidade)",
        description="Nome do Vertex Group para densidade adaptativa (0=baixa, 1=alta). Funcionalidade completa apenas com engine nativo",
        default="",
        maxlen=64
    )
    
    # Configurações de histórico/comparação (Onda 3)
    show_comparison: BoolProperty(
        name="Mostrar Comparação",
        description="Exibe painel de comparação lado a lado entre original e remesh",
        default=False
    )
    
    last_config_hash: StringProperty(
        name="Hash da Última Config",
        description="Hash interno para detectar mudanças de configuração",
        default="",
        options={'HIDDEN'}
    )


def register_props():
    bpy.types.Scene.fieldremesher_settings = PointerProperty(type=FieldRemesherSettings)


def unregister_props():
    del bpy.types.Scene.fieldremesher_settings
