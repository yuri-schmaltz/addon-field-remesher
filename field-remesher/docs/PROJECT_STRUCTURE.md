# Estrutura do projeto

```
field-remesher/
  addon/
    field_remesher/
      __init__.py
      preferences.py
      properties.py
      ui.py
      backend/
        __init__.py
        quadriflow_backend.py
        instant_backend.py
      ops/
        remesh.py
      util/
        context.py
        transfer.py
      binaries/
        <platform>/   # binários opcionais do módulo nativo
  native/
    README.md
    CMakeLists.txt
    src/
      bindings.cpp
      im_wrapper.cpp
      im_wrapper.h
    third_party/
      instant-meshes/  # submodule/fork (não incluído)
  scripts/
    package_addon.py
    build_native.py
  .github/
    workflows/ci.yml
    ISSUE_TEMPLATE/
```
