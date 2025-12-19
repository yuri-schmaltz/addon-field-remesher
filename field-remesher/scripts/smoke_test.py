#!/usr/bin/env python3
"""
Smoke test: valida sintaxe básica dos módulos Python
compilando os arquivos sem executar imports completos.
"""
import py_compile
import sys
from pathlib import Path

ADDON_DIR = Path(__file__).parent.parent / "addon" / "field_remesher"

def test_syntax():
    """Compila todos os arquivos .py para verificar sintaxe."""
    errors = []
    
    py_files = list(ADDON_DIR.rglob("*.py"))
    
    for py_file in py_files:
        rel_path = py_file.relative_to(ADDON_DIR.parent)
        try:
            py_compile.compile(str(py_file), doraise=True, quiet=1)
            print(f"✓ {rel_path}")
        except py_compile.PyCompileError as e:
            errors.append(f"{rel_path}: {e}")
    
    if errors:
        print("\n❌ Erros de sintaxe:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print(f"\n✅ Todos os {len(py_files)} arquivos Python têm sintaxe válida!")
        sys.exit(0)

if __name__ == "__main__":
    test_syntax()
