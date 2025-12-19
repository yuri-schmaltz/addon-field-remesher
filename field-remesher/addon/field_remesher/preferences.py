import bpy
from bpy.types import AddonPreferences
from bpy.props import EnumProperty, BoolProperty


class FieldRemesherPreferences(AddonPreferences):
    bl_idname = __package__

    backend: EnumProperty(
        name="Backend",
        items=[
            ("AUTO", "Auto", "Usa Instant Engine se disponível; senão Quadriflow"),
            ("INSTANT", "Instant Engine (nativo)", "Requer módulo nativo compilado"),
            ("QUADRIFLOW", "Quadriflow (fallback)", "Usa o remesher quad do Blender"),
        ],
        default="AUTO",
    )

    show_advanced: BoolProperty(
        name="Mostrar opções avançadas",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "backend")
        layout.prop(self, "show_advanced")
        layout.label(text="Obs.: Engine nativa exige compilar e copiar binários para addon/field_remesher/binaries/.")
