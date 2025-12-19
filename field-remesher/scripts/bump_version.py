#!/usr/bin/env python3
"""
Script para bump de versão automatizado.
Atualiza __init__.py, blender_manifest.toml e CHANGELOG.md.
"""
import argparse
import re
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
INIT_PY = ROOT / "addon" / "field_remesher" / "__init__.py"
MANIFEST_TOML = ROOT / "addon" / "field_remesher" / "blender_manifest.toml"
CHANGELOG_MD = ROOT / "CHANGELOG.md"

def parse_version(version_str):
    """Converte string X.Y.Z em tupla (X, Y, Z)."""
    parts = version_str.split(".")
    if len(parts) != 3:
        raise ValueError(f"Versão inválida: {version_str}. Use formato X.Y.Z")
    return tuple(int(p) for p in parts)

def version_to_str(version_tuple):
    """Converte tupla (X, Y, Z) em string X.Y.Z."""
    return ".".join(str(v) for v in version_tuple)

def bump_version(current, bump_type):
    """Incrementa versão baseado no tipo (major, minor, patch)."""
    major, minor, patch = current
    if bump_type == "major":
        return (major + 1, 0, 0)
    elif bump_type == "minor":
        return (major, minor + 1, 0)
    elif bump_type == "patch":
        return (major, minor, patch + 1)
    else:
        raise ValueError(f"Tipo inválido: {bump_type}")

def update_init_py(new_version):
    """Atualiza bl_info['version'] no __init__.py."""
    content = INIT_PY.read_text(encoding="utf-8")
    pattern = r'"version":\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)'
    replacement = f'"version": {new_version}'
    new_content = re.sub(pattern, replacement, content)
    INIT_PY.write_text(new_content, encoding="utf-8")
    print(f"✓ {INIT_PY.relative_to(ROOT)}")

def update_manifest_toml(new_version_str):
    """Atualiza version no blender_manifest.toml."""
    content = MANIFEST_TOML.read_text(encoding="utf-8")
    pattern = r'version\s*=\s*"[^"]+"'
    replacement = f'version = "{new_version_str}"'
    new_content = re.sub(pattern, replacement, content)
    MANIFEST_TOML.write_text(new_content, encoding="utf-8")
    print(f"✓ {MANIFEST_TOML.relative_to(ROOT)}")

def update_changelog(new_version_str):
    """Adiciona entrada no CHANGELOG.md."""
    content = CHANGELOG_MD.read_text(encoding="utf-8")
    
    date_str = datetime.now().strftime("%B %Y")  # Ex: "Dezembro 2025"
    new_section = f"""## v{new_version_str} — [Descrição] ({date_str})

### 🎯 Mudanças
- TODO: Descrever mudanças principais

"""
    
    # Insere após o título principal
    lines = content.split("\n")
    insert_idx = 2  # Após "# Changelog" e linha vazia
    lines.insert(insert_idx, new_section)
    
    CHANGELOG_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"✓ {CHANGELOG_MD.relative_to(ROOT)} (nova seção adicionada)")

def main():
    parser = argparse.ArgumentParser(description="Bump de versão do add-on")
    parser.add_argument("bump_type", choices=["major", "minor", "patch"], 
                       help="Tipo de bump: major (X.0.0), minor (0.Y.0), patch (0.0.Z)")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Mostra mudanças sem aplicar")
    
    args = parser.parse_args()
    
    # Lê versão atual do __init__.py
    content = INIT_PY.read_text(encoding="utf-8")
    match = re.search(r'"version":\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', content)
    if not match:
        print("❌ Não foi possível encontrar versão em __init__.py")
        sys.exit(1)
    
    current_version = tuple(int(match.group(i)) for i in range(1, 4))
    current_str = version_to_str(current_version)
    
    # Calcula nova versão
    new_version = bump_version(current_version, args.bump_type)
    new_str = version_to_str(new_version)
    
    print(f"\n📦 Bump de Versão: {current_str} → {new_str}\n")
    
    if args.dry_run:
        print("🔍 Modo dry-run: nenhuma alteração será feita\n")
        print(f"Atualizaria:")
        print(f"  - {INIT_PY.relative_to(ROOT)}")
        print(f"  - {MANIFEST_TOML.relative_to(ROOT)}")
        print(f"  - {CHANGELOG_MD.relative_to(ROOT)}")
    else:
        update_init_py(new_version)
        update_manifest_toml(new_str)
        update_changelog(new_str)
        print(f"\n✅ Versão atualizada para {new_str}")
        print(f"\nPróximos passos:")
        print(f"  1. Edite {CHANGELOG_MD.name} para descrever mudanças")
        print(f"  2. git add {INIT_PY.relative_to(ROOT)} {MANIFEST_TOML.relative_to(ROOT)} {CHANGELOG_MD.relative_to(ROOT)}")
        print(f"  3. git commit -m 'chore: bump version to {new_str}'")
        print(f"  4. git tag -a v{new_str} -m 'Release v{new_str}'")
        print(f"  5. git push origin main --tags")

if __name__ == "__main__":
    main()
