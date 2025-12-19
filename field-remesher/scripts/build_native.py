"""Build helper (scaffold)

Este script NÃO garante build completo do engine, pois depende do upstream em `native/third_party/instant-meshes`
e de alterações para produzir uma lib core. Use como ponto de partida.

Uso (exemplo):
  python scripts/build_native.py --config Release

Depois copie o binário resultante para:
  addon/field_remesher/binaries/<platform>/
"""

import os
import argparse
import subprocess
import platform
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NATIVE_DIR = os.path.join(ROOT, "native")
BUILD_DIR = os.path.join(NATIVE_DIR, "build")


def run(cmd, cwd=None):
    print(">", " ".join(cmd))
    subprocess.check_call(cmd, cwd=cwd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="Release")
    args = ap.parse_args()

    os.makedirs(BUILD_DIR, exist_ok=True)

    run(["cmake", ".."], cwd=BUILD_DIR)
    run(["cmake", "--build", ".", "--config", args.config], cwd=BUILD_DIR)

    print("Build concluído. Localize o artefato 'instant_meshes_py' no diretório de build.")
    print("Copie para addon/field_remesher/binaries/<platform>/ conforme seu ambiente.")

if __name__ == "__main__":
    main()
