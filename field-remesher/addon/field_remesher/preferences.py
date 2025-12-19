import bpy
from bpy.types import AddonPreferences
from bpy.props import EnumProperty, BoolProperty


class FieldRemesherPreferences(AddonPreferences):
    bl_idname = __package__

    backend: EnumProperty(
        name="Backend de Remesh",
        description="Escolha o motor de remesh a ser utilizado",
        items=[
            ("AUTO", "Automático", "Usa Instant Engine se disponível; caso contrário usa Quadriflow"),
            ("INSTANT", "Instant Engine (Nativo)", "Motor nativo de alta performance (requer compilação)"),
            ("QUADRIFLOW", "Quadriflow (Integrado)", "Motor quad integrado ao Blender (sempre disponível)"),
        ],
        default="AUTO",
    )

    show_advanced: BoolProperty(
        name="Mostrar Opções Avançadas",
        description="Exibe configurações adicionais para usuários experientes",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        
        # Box: Configuração de Backend
        box = layout.box()
        box.label(text="Configuração de Backend", icon='SETTINGS')
        box.prop(self, "backend", text="")
        
        # Ajuda contextual para backend INSTANT
        if self.backend == "INSTANT":
            col = box.column(align=True)
            col.separator(factor=0.5)
            row = col.row()
            row.alert = True
            row.label(text="⚠ Requer módulo nativo compilado", icon='INFO')
            
            col2 = col.column(align=True)
            col2.scale_y = 0.8
            col2.label(text="Localização esperada:")
            col2.label(text="addon/field_remesher/binaries/<plataforma>/")
        
        layout.separator()
        
        # Box: Opções Avançadas
        box2 = layout.box()
        box2.prop(self, "show_advanced", icon='PREFERENCES')
        
        if self.show_advanced:
            col = box2.column(align=True)
            col.separator(factor=0.5)
            col.label(text="[Opções avançadas serão adicionadas futuramente]", icon='INFO')
