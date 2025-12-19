# Field Remesher (Instant-like) — Blender Add-on

[![CI](https://github.com/yuri-schmaltz/addon-field-remesher/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/yuri-schmaltz/addon-field-remesher/actions/workflows/ci.yml)

Add-on para Blender (3.6 LTS+ e 4.x) que entrega retopologia quad “field-aligned” **estilo Instant Meshes**,
com **fallback imediato** via Quadriflow e um **backend nativo opcional** (engine) para paridade avançada.

## Status
- ✅ Fallback Quadriflow: funcional (MVP)
- 🧩 Engine nativo: estrutura pronta (stub). Requer implementar/compilar bindings e core.
- ✅ Roadmap e backlog (GitHub) incluídos em `ROADMAP.md` e `docs/github_backlog.csv`

## Estrutura do repositório
- `addon/` — código do add-on (instalável no Blender)
- `native/` — esqueleto para bindings (pybind11) + core (submodule / fork do upstream)
- `scripts/` — empacotamento e build do módulo nativo
- `.github/` — templates de issues e workflow básico
- `docs/` — especificação, compatibilidade, backlog importável, etc.

## Instalação (fallback)
1. No Blender: `Edit > Preferences > Add-ons > Install...`
2. Selecione o **zip do add-on** gerado por `scripts/package_addon.py` (ou compacte a pasta `addon/`).
3. Ative o add-on: **Field Remesher (Instant-like)**.
4. Painel: `View3D > Sidebar (N) > Field Remesher`.

## Gerar zip instalável do add-on
No terminal (Python 3.x):
```bash
python scripts/package_addon.py
```
Saída: `dist/field_remesher_addon.zip`

## Backend Engine nativo (opcional)
A estrutura está em `native/`. Para ativar o backend INSTANT:
1) implemente o core (ou traga o upstream via submodule/fork),
2) compile o módulo `instant_meshes_py`,
3) copie o binário para `addon/field_remesher/binaries/<platform>/`,
4) selecione backend **AUTO** ou **INSTANT** nas preferências do add-on.

Veja: `native/README.md`.

## Licenças
- Código do add-on: `LICENSE` (GPL-3.0-or-later recomendado para Blender)
- Terceiros: `LICENSES/` (inclua upstream do engine quando adicionar)

