import os
import re
import zipfile
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ADDON_DIR = os.path.join(ROOT, "addon", "field_remesher")
DIST_DIR = os.path.join(ROOT, "dist")
ZIP_PATH = os.path.join(DIST_DIR, "field_remesher_addon.zip")

RELATIVE_IMPORT_RE = re.compile(r"^\s*from\s+(\.+)")

def _validate_relative_imports(addon_pkg_dir: str) -> None:
    """Valida imports relativos contra a profundidade das pastas.

    Regra: para cada arquivo Python em field_remesher, o número de pontos em
    "from ..foo import bar" menos 1 não pode exceder a profundidade do arquivo
    relativa à raiz do pacote (field_remesher).

    Ex.: field_remesher/ui.py (profundidade 0) NÃO pode usar "from ..backend".
         field_remesher/ops/remesh.py (profundidade 1) pode usar "from ..backend".
    """
    errors = []
    root = addon_pkg_dir
    for base, _, files in os.walk(root):
        for fn in files:
            if not fn.endswith('.py'):
                continue
            full = os.path.join(base, fn)
            rel_dir = os.path.relpath(base, root)
            depth = 0 if rel_dir == os.curdir else len(rel_dir.split(os.sep))

            try:
                with open(full, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, start=1):
                        m = RELATIVE_IMPORT_RE.match(line)
                        if not m:
                            continue
                        dots = len(m.group(1))
                        # número máximo de pontos permitido = depth + 1
                        # pois 'from .x import y' (1 ponto) é sempre ok na própria pasta
                        if (dots - 1) > depth:
                            rel_file = os.path.relpath(full, root)
                            errors.append(f"{rel_file}:{i}: uso inválido de import relativo ('{m.group(1)}') para profundidade {depth}")
            except OSError:
                # arquivinho inacessível: continua e deixa zip acusar depois
                continue

    if errors:
        print("Falha na validação de imports relativos (field_remesher):")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)

def main():
    os.makedirs(DIST_DIR, exist_ok=True)

    # O zip instalável do Blender deve conter uma pasta de addon no root do zip.
    temp_root = os.path.join(DIST_DIR, "_tmp_addon")
    if os.path.exists(temp_root):
        shutil.rmtree(temp_root)
    os.makedirs(temp_root, exist_ok=True)

    dst_addon = os.path.join(temp_root, "field_remesher")
    shutil.copytree(ADDON_DIR, dst_addon)

    # Validação estática de imports relativos antes de zipar
    _validate_relative_imports(dst_addon)

    # cria zip
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(temp_root):
            for fn in files:
                full = os.path.join(base, fn)
                rel = os.path.relpath(full, temp_root)
                z.write(full, rel)

    shutil.rmtree(temp_root)
    print("OK:", ZIP_PATH)

if __name__ == "__main__":
    main()
