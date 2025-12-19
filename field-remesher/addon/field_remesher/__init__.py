bl_info = {
    "name": "Field Remesher (Instant-like)",
    "author": "Scaffold",
    "version": (0, 1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Field Remesher",
    "description": "Remesher estilo Instant Meshes com backend nativo opcional e fallback Quadriflow",
    "category": "Object",
}

import bpy

from .preferences import FieldRemesherPreferences
from .properties import FieldRemesherSettings, register_props, unregister_props
from .ui import FIELDREMESHER_PT_panel
from .ops.remesh import FIELDREMESHER_OT_remesh


CLASSES = (
    FieldRemesherPreferences,
    FieldRemesherSettings,
    FIELDREMESHER_OT_remesh,
    FIELDREMESHER_PT_panel,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    register_props()


def unregister():
    unregister_props()
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
