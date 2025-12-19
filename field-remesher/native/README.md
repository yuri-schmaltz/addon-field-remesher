# Native (Engine) scaffold

Este diretório contém o esqueleto para compilar um módulo Python nativo (`instant_meshes_py`)
usando **pybind11** e um **core C++**.

## Importante
- O upstream (engine) **não** está incluído neste zip. A recomendação é adicionar como submodule:
  `native/third_party/instant-meshes/`.
- Você deve garantir a conformidade de licenças em `LICENSES/`.

## Fluxo recomendado
1) Adicionar upstream como submodule/fork em `native/third_party/instant-meshes/`
2) Refatorar/expôr um alvo `instant_meshes_core` (biblioteca sem UI)
3) Implementar `src/im_wrapper.cpp` chamando o core
4) Compilar com CMake e copiar o binário resultante para:
   `addon/field_remesher/binaries/<platform>/`

## Build (exemplo)
```bash
mkdir -p native/build
cd native/build
cmake ..
cmake --build . --config Release
```

O script `scripts/build_native.py` é um ponto de partida para automação.
