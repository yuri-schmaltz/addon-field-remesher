"""Backend nativo (engine) — stub

Quando o módulo nativo estiver disponível (pybind11), ele deve ser colocado em:
`addon/field_remesher/binaries/<platform>/`.

Este arquivo detecta e carrega o módulo em runtime.
"""

import os
import sys
import platform


def _platform_tag():
    sysname = platform.system().lower()
    arch = platform.machine().lower()
    if sysname.startswith("darwin"):
        sysname = "macos"
    return f"{sysname}-{arch}"


def _inject_binaries_path():
    here = os.path.dirname(__file__)
    addon_root = os.path.abspath(os.path.join(here, ".."))
    bin_dir = os.path.join(addon_root, "binaries", _platform_tag())
    if os.path.isdir(bin_dir) and bin_dir not in sys.path:
        sys.path.insert(0, bin_dir)
    return bin_dir


def is_available():
    _inject_binaries_path()
    try:
        import instant_meshes_py  # noqa: F401
        return True
    except Exception:
        return False


def run_instant_engine(obj, settings, guides=None):
    """Executa engine nativa (quando implementada)."""
    _inject_binaries_path()
    import instant_meshes_py

    raise NotImplementedError(
        "Engine nativa ainda não implementada neste scaffold. "
        "Implemente native/ + bindings e atualize este backend."
    )
