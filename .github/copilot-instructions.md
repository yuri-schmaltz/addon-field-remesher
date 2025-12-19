# Copilot Instructions — Field Remesher (Blender Add-on)

Purpose: help AI agents contribute productively to this repo by capturing the project’s architecture, workflows, and conventions.

## Big Picture
- Add-on for Blender 3.6 LTS+ and 4.x providing Instant Meshes–style quad remeshing with Quadriflow fallback.
- High-level flow: UI panel → operator `FIELDREMESHER_OT_remesh` → backend selection (AUTO/INSTANT/QUADRIFLOW) → non-destructive duplicate → run backend → optional attribute transfer → finalize.
- Key entry points:
  - Register/bootstrapping: [field-remesher/addon/field_remesher/__init__.py](field-remesher/addon/field_remesher/__init__.py)
  - Operator: [field-remesher/addon/field_remesher/ops/remesh.py](field-remesher/addon/field_remesher/ops/remesh.py)
  - Backends: [field-remesher/addon/field_remesher/backend](field-remesher/addon/field_remesher/backend)
  - UI/Prefs/Props: [field-remesher/addon/field_remesher/ui.py](field-remesher/addon/field_remesher/ui.py), [field-remesher/addon/field_remesher/preferences.py](field-remesher/addon/field_remesher/preferences.py), [field-remesher/addon/field_remesher/properties.py](field-remesher/addon/field_remesher/properties.py)

## Backends
- Quadriflow (fallback): implemented via `bpy.ops.object.quadriflow_remesh` with robust View3D context override in [field-remesher/addon/field_remesher/backend/quadriflow_backend.py](field-remesher/addon/field_remesher/backend/quadriflow_backend.py) and [field-remesher/addon/field_remesher/util/context.py](field-remesher/addon/field_remesher/util/context.py).
- Instant Engine (native): scaffold only. Loader and platform binary path injection live in [field-remesher/addon/field_remesher/backend/instant_backend.py](field-remesher/addon/field_remesher/backend/instant_backend.py). Place compiled module in `addon/field_remesher/binaries/<platform>/`.
- Contract for native engine (pybind11): `instant_meshes_py.remesh(verts, faces, options, guides=None) -> (out_verts, out_faces, meta)` as documented in [field-remesher/SPEC.md](field-remesher/SPEC.md).

## Developer Workflows
- Package installable add-on zip:
  - Run: `python field-remesher/scripts/package_addon.py`
  - Output: `field-remesher/dist/field_remesher_addon.zip` (install in Blender Preferences → Add-ons → Install)
- Build native engine (optional; scaffold):
  - Prereqs: CMake, toolchain, upstream core as submodule `native/third_party/instant-meshes`.
  - Run: `python field-remesher/scripts/build_native.py --config Release`
  - Copy built `instant_meshes_py` to `field-remesher/addon/field_remesher/binaries/<platform>/` matching Blender’s Python ABI; see [field-remesher/COMPAT.md](field-remesher/COMPAT.md).
- Test in Blender:
  - Panel: View3D → Sidebar (N) → "Field Remesher".
  - Backend preference: set in Add-on Preferences (AUTO, INSTANT, QUADRIFLOW) [field-remesher/addon/field_remesher/preferences.py](field-remesher/addon/field_remesher/preferences.py).

## Conventions & Patterns
- Non-destructive by default: operator duplicates active mesh and optionally hides original; see `_dup_object()` and `keep_original` in [field-remesher/addon/field_remesher/ops/remesh.py](field-remesher/addon/field_remesher/ops/remesh.py).
- Context handling: use `get_view3d_override()` for ops requiring a View3D context; see [field-remesher/addon/field_remesher/util/context.py](field-remesher/addon/field_remesher/util/context.py).
- Attribute transfer: apply `DATA_TRANSFER` modifier, degrade gracefully across Blender versions; see [field-remesher/addon/field_remesher/util/transfer.py](field-remesher/addon/field_remesher/util/transfer.py).
- Properties/UI:
  - Modes: FACES/EDGE/RATIO with mapped params in [field-remesher/addon/field_remesher/properties.py](field-remesher/addon/field_remesher/properties.py) and [field-remesher/addon/field_remesher/ui.py](field-remesher/addon/field_remesher/ui.py).
  - Preferences include backend selector and advanced toggle in [field-remesher/addon/field_remesher/preferences.py](field-remesher/addon/field_remesher/preferences.py).
- Errors/reporting: catch exceptions in operator, report via Blender operator `report()` and return `CANCELLED` on failure.
- Language: UI/messages are in pt-BR; keep consistency for user-visible strings.

## Extending
- Add a new parameter:
  - Define in `FieldRemesherSettings` → expose in `ui.py` → plumb into backend kwargs in `quadriflow_backend.py` and/or native options dict.
- Add a new backend:
  - Create module under `backend/`, export in [field-remesher/addon/field_remesher/backend/__init__.py](field-remesher/addon/field_remesher/backend/__init__.py), add preference option, branch in operator decision.
- Native bindings:
  - CMake/pybind11 scaffold in [field-remesher/native](field-remesher/native) with example bindings in [field-remesher/native/src/bindings.cpp](field-remesher/native/src/bindings.cpp) and wrapper in [field-remesher/native/src/im_wrapper.cpp](field-remesher/native/src/im_wrapper.cpp).

## Compatibility
- Supported Blender: 3.6 LTS and 4.x. ABI-sensitive binaries must match Blender’s embedded Python version; see [field-remesher/COMPAT.md](field-remesher/COMPAT.md).

## References
- Project overview and roadmap: [field-remesher/README.md](field-remesher/README.md), [field-remesher/ROADMAP.md](field-remesher/ROADMAP.md), [field-remesher/SPEC.md](field-remesher/SPEC.md), [field-remesher/docs/PROJECT_STRUCTURE.md](field-remesher/docs/PROJECT_STRUCTURE.md)
