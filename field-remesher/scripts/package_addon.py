import os
import zipfile
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ADDON_DIR = os.path.join(ROOT, "addon", "field_remesher")
DIST_DIR = os.path.join(ROOT, "dist")
ZIP_PATH = os.path.join(DIST_DIR, "field_remesher_addon.zip")

def main():
    os.makedirs(DIST_DIR, exist_ok=True)

    # O zip instalável do Blender deve conter uma pasta de addon no root do zip.
    temp_root = os.path.join(DIST_DIR, "_tmp_addon")
    if os.path.exists(temp_root):
        shutil.rmtree(temp_root)
    os.makedirs(temp_root, exist_ok=True)

    dst_addon = os.path.join(temp_root, "field_remesher")
    shutil.copytree(ADDON_DIR, dst_addon)

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
