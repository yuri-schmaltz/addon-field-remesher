import os
import re
import zipfile
import shutil
import argparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ADDON_DIR = os.path.join(ROOT, "addon", "field_remesher")
DIST_DIR = os.path.join(ROOT, "dist")
ZIP_PATH = os.path.join(DIST_DIR, "field_remesher_addon.zip")

RELATIVE_IMPORT_RE = re.compile(r"^\s*from\s+(\.+)")
BL_INFO_VERSION_RE = re.compile(r"version\s*:\s*\((\s*\d+\s*,\s*\d+\s*,\s*\d+\s*)\)")
MANIFEST_VERSION_RE = re.compile(r"^\s*version\s*=\s*\"(?P<ver>[^\"]+)\"\s*$")

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

def _extract_bl_info_version(addon_pkg_dir: str) -> str | None:
    """Extrai a versão do bl_info do __init__.py como string X.Y.Z.

    Procura por uma linha do tipo: "version": (x, y, z)
    """
    init_path = os.path.join(addon_pkg_dir, "__init__.py")
    try:
        with open(init_path, "r", encoding="utf-8") as f:
            text = f.read()
        m = BL_INFO_VERSION_RE.search(text)
        if not m:
            return None
        nums = m.group(1)
        parts = [p.strip() for p in nums.split(",")]
        if len(parts) != 3:
            return None
        major, minor, patch = (int(parts[0]), int(parts[1]), int(parts[2]))
        return f"{major}.{minor}.{patch}"
    except OSError:
        return None

def _sync_manifest_version(addon_pkg_dir: str, version_str: str) -> None:
    """Sincroniza a versão no blender_manifest.toml se existir.

    Substitui a linha 'version = "..."' pelo valor de version_str.
    """
    manifest_path = os.path.join(addon_pkg_dir, "blender_manifest.toml")
    if not os.path.exists(manifest_path):
        return
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = []
        changed = False
        for line in lines:
            if MANIFEST_VERSION_RE.match(line):
                new_lines.append(f"version = \"{version_str}\"\n")
                changed = True
            else:
                new_lines.append(line)
        if changed:
            with open(manifest_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
    except OSError:
        # não bloquear empacote caso não seja possível escrever
        pass

def _read_manifest_version(addon_pkg_dir: str) -> str | None:
    manifest_path = os.path.join(addon_pkg_dir, "blender_manifest.toml")
    if not os.path.exists(manifest_path):
        return None
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            for line in f:
                m = MANIFEST_VERSION_RE.match(line)
                if m:
                    return m.group("ver").strip()
    except OSError:
        return None
    return None

def main():
    parser = argparse.ArgumentParser(description="Package Field Remesher add-on")
    parser.add_argument("--strict", action="store_true", help="Falha se versão do manifesto divergir do bl_info")
    args = parser.parse_args()
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

    # Verificação de versão e sincronização
    ver = _extract_bl_info_version(dst_addon)
    if ver:
        current_manifest_ver = _read_manifest_version(dst_addon)
        if args.strict and current_manifest_ver is not None and current_manifest_ver != ver:
            print("Erro: Versão do manifesto (", current_manifest_ver, ") difere do bl_info (", ver, ")", sep="")
            print("Habilitado --strict, abortando.")
            raise SystemExit(2)
        # Se não for strict, sincroniza automaticamente
        _sync_manifest_version(dst_addon, ver)

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
