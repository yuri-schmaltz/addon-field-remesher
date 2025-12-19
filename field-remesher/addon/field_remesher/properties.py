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


class FieldRemesherSettings(PropertyGroup):
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
        name="Vertex Group (densidade)",
        description="Nome do Vertex Group (0..1) para controlar densidade (pleno na engine; limitado no fallback)",
        default="",
    )


def register_props():
    bpy.types.Scene.fieldremesher_settings = PointerProperty(type=FieldRemesherSettings)


def unregister_props():
    del bpy.types.Scene.fieldremesher_settings
