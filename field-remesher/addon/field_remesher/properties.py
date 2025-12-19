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
        items=[
            ("FACES", "Faces", "Número alvo de faces (quads)"),
            ("EDGE", "Edge Length", "Comprimento alvo de aresta"),
            ("RATIO", "Ratio", "Razão relativa ao mesh atual"),
        ],
        default="FACES",
    )

    target_faces: IntProperty(name="Target Faces", default=4000, min=1)
    target_edge_length: FloatProperty(name="Target Edge Length", default=0.1, min=1e-7)
    target_ratio: FloatProperty(name="Target Ratio", default=1.0, min=0.0)

    use_mesh_symmetry: BoolProperty(name="Simetria", default=False)
    use_preserve_sharp: BoolProperty(name="Preservar sharp", default=True)
    use_preserve_boundary: BoolProperty(name="Preservar boundary", default=True)

    preserve_attributes: BoolProperty(name="Preservar atributos (quando possível)", default=False)
    smooth_normals: BoolProperty(name="Smooth normals", default=False)
    seed: IntProperty(name="Seed", default=0, min=0)

    keep_original: BoolProperty(name="Manter original", default=True)
    transfer_uv: BoolProperty(name="Transferir UV", default=True)
    transfer_vcol: BoolProperty(name="Transferir Color Attributes", default=True)

    density_vgroup: StringProperty(
        name="Vertex Group (densidade)",
        description="Nome do Vertex Group (0..1) para controlar densidade (pleno na engine; limitado no fallback)",
        default="",
    )


def register_props():
    bpy.types.Scene.fieldremesher_settings = PointerProperty(type=FieldRemesherSettings)


def unregister_props():
    del bpy.types.Scene.fieldremesher_settings
