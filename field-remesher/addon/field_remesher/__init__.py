bl_info = {
    "name": "Field Remesher (Instant-like)",
    "author": "Scaffold",
    "version": (0, 1, 2),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Field Remesher",
    "description": "Remesher estilo Instant Meshes com backend nativo opcional e fallback Quadriflow",
    "category": "Object",
}

import bpy

from .preferences import FieldRemesherPreferences
from .properties import FieldRemesherSettings, register_props, unregister_props
from .ui import (
    FIELDREMESHER_PT_panel,
    FIELDREMESHER_PT_presets_advanced,
    FIELDREMESHER_PT_comparison,
    FIELDREMESHER_PT_guides,
)
from .ops.remesh import FIELDREMESHER_OT_remesh
from .ops.preset_ops import (
    FIELDREMESHER_OT_save_preset,
    FIELDREMESHER_OT_reset_to_defaults,
    FIELDREMESHER_OT_add_guide,
    FIELDREMESHER_OT_clear_guides,
    FIELDREMESHER_OT_compare_stats,
)


CLASSES = (
    FieldRemesherPreferences,
    FieldRemesherSettings,
    FIELDREMESHER_OT_remesh,
    FIELDREMESHER_OT_save_preset,
    FIELDREMESHER_OT_reset_to_defaults,
    FIELDREMESHER_OT_add_guide,
    FIELDREMESHER_OT_clear_guides,
    FIELDREMESHER_OT_compare_stats,
    FIELDREMESHER_PT_panel,
    FIELDREMESHER_PT_presets_advanced,
    FIELDREMESHER_PT_comparison,
    FIELDREMESHER_PT_guides,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    register_props()


def unregister():
    unregister_props()
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
